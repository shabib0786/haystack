from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from haystack.retriever.dense import EmbeddingRetriever, DensePassageRetriever
from haystack.pipeline import FAQPipeline
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.reader import FARMReader
from haystack.pipeline import ExtractiveQAPipeline

import logging

#Initialization for FAQ
document_store_faq = ElasticsearchDocumentStore(host="documentstore", username="", password="",
                                            index="nsl_support_document",
                                            embedding_field="question_emb",
                                            embedding_dim=384,
                                            similarity='cosine')
retriever_faq = EmbeddingRetriever(document_store=document_store_faq, embedding_model="sentence-transformers/all-MiniLM-L6-v2", use_gpu=False)
pipe_faq = FAQPipeline(retriever=retriever_faq)

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



class ActionFaqAndAtq(Action):
    def __init__(self, request: OmniChannelRequest):
        self.request = request

    def run(self):
        search = pipe_faq.run(query=self.request.message)
        if len(search["answers"]) > 0:
            text = search["answers"][0]["answer"]
            image = search["answers"][0]["meta"]["image"]
            # video = search["answers"][0]["meta"]["video"]
            confidence_faq = search["answers"][0]["score"]
            if confidence_faq!=0 and confidence_faq > 0.85: # , {"recipient_id": "", "custom" : { "attachment" : { "type":"video", "payload":{ "src": video } }} }
                return [{"recipient_id": self.request.sender , "image": image}, {"recipient_id": self.request.sender , "text" : text}]
        
        prediction = pipe_atq.run(query = self.request.message, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 1}})
        if len(prediction["answers"]) > 0 and prediction["answers"][0]['score'] > 0.1:
            text = prediction["answers"][0]["answer"]
            return [{"recipient_id": self.request.sender , "text" : text}]
        else:
            return [{"recipient_id": self.request.sender , "text" : "Going to transfer"}, {"recipient_id": self.request.sender,"text":"I did not find anything in Knowledge base... Select your prefered choice:","buttons":[{"title":"callback","payload":"callback"},{"title":"handover to support","payload":"handover"},{"title":"Raising a jira ticket","payload":"jira"}]}]
           