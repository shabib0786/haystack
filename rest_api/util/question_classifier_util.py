
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.python.keras.models import load_model
import numpy as np
import logging
from haystack.document_store.faiss import FAISSDocumentStore
from haystack.retriever.dense import EmbeddingRetriever, DensePassageRetriever
from haystack.reader import FARMReader
from haystack.pipeline import ExtractiveQAPipeline
from haystack.generator.transformers import Seq2SeqGenerator
from haystack.pipeline import GenerativeQAPipeline
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from rest_api.constants import CONTEXT, WRONG_RESPONSE

# Initializing below objects for ATQ
logging.info("Initializing elastic document store for atq....")
document_store_atq = ElasticsearchDocumentStore(host="documentstore", username="", password="",index="nsl_support_document_atq",embedding_dim=768) 

# retriever_atq = EmbeddingRetriever(document_store=document_store_atq, embedding_model="deepset/sentence_bert", use_gpu=True)
logging.info("retriever_atq creation ends " )
retriever_atq = DensePassageRetriever(document_store=document_store_atq, 
                    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                    use_gpu = False)

reader_atq = FARMReader(model_name_or_path="deepset/roberta-base-squad2")
logging.info("reader_atq creation ends " )
pipe_atq = ExtractiveQAPipeline(reader_atq, retriever_atq)
logging.info("pipe creation for atq ends " )

document_store_generator = FAISSDocumentStore(vector_dim=128, faiss_index_factory_str="Flat")
embedding_retriever = EmbeddingRetriever(document_store=document_store_generator,
                               embedding_model="yjernite/retribert-base-uncased",
                               model_format="retribert")
generator = Seq2SeqGenerator(model_name_or_path="yjernite/bart_eli5", min_length=50)
generator_pipeline = GenerativeQAPipeline(generator, embedding_retriever)

class QuestionClassifier:
    def __init__(self,classes,model,tokenizer,label_encoder):
        self.classes = classes
        self.classifier = model
        self.tokenizer = tokenizer
        self.label_encoder = label_encoder

    def get_intent(self,text):
        self.text = [text]
        self.test_keras = self.tokenizer.texts_to_sequences(self.text)
        self.test_keras_sequence = pad_sequences(self.test_keras, maxlen=16, padding='post')
        self.pred = self.classifier.predict(self.test_keras_sequence)
        return label_encoder.inverse_transform(np.argmax(self.pred,1))[0]


class QuestionClassifierUtil:
    def __init__(self) -> None:
        self.nlu = QuestionClassifier(classes,model,tokenizer,label_encoder)
        self.question_type =  0

    def generate_answer(self, query):
        self.question_type = self.nlu.get_intent(query)
        if self.question_type == 0:
            logging.info('Category: Generative\n')
            search = generator_pipeline.run(query = query, params={"Retriever": {"top_k": 10}})
            self.redis_util.set_key_in_redis(self.request.sender, CONTEXT, WRONG_RESPONSE)
            return [{"recipient_id": self.request.sender , "text" : search['answers'][0]}, {"recipient_id": self.request.sender,"text":"Was it helpful?", "buttons":[{"title":"no","payload":"no"}]}]
            

        else:
            logging.info('Category: Non-Generative')
            search = pipe_atq.run(query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 1}})
            if len(search["answers"]) > 0 and search["answers"][0]['score'] > 0.75:
                text = search["answers"][0]["answer"]
                return [{"recipient_id": self.request.sender , "text" : text}]
        
            else:
                return [{"recipient_id": self.request.sender , "text" : "Going to transfer"}, {"recipient_id": self.request.sender,"text":"I did not find anything in Knowledge base... Select your prefered choice:","buttons":[{"title":"callback","payload":"callback"},{"title":"Transfer to an agent","payload":"handover"},{"title":"Create a ticket","payload":"jira"}]}]
            
        
            


model = load_model('/app/rest_api/util/models/factoidVsNonFactoid.h5')

with open('/app/rest_api/util/utils/classes.pkl','rb') as file:
  classes = pickle.load(file)

with open('/app/rest_api/util/utils/tokenizer.pkl','rb') as file:
  tokenizer = pickle.load(file)

with open('/app/rest_api/util/utils/label_encoder.pkl','rb') as file:
  label_encoder = pickle.load(file)
