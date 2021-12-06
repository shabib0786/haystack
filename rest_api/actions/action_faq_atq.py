from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from haystack.retriever.dense import EmbeddingRetriever
from haystack.pipeline import FAQPipeline
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from rest_api.util.response_util import OmniChannelResponseUtil
from haystack.retriever.dense import EmbeddingRetriever
from rest_api.util.redis_util import RedisUtil
from rest_api.util.question_classifier_util import QuestionClassifierUtil
import numpy as np
import logging
from rest_api.constants import CONTEXT, WRONG_RESPONSE


#Initialization for FAQ
document_store_faq = ElasticsearchDocumentStore(host="documentstore", username="", password="",
                                            index="nsl_support_document",
                                            embedding_field="question_emb",
                                            embedding_dim=384,
                                            similarity='cosine')
retriever_faq = EmbeddingRetriever(document_store=document_store_faq, embedding_model="sentence-transformers/all-MiniLM-L6-v2", use_gpu=False)
pipe_faq = FAQPipeline(retriever=retriever_faq)

atq = QuestionClassifierUtil()


class ActionFaqAndAtq(Action):
    def __init__(self, request: OmniChannelRequest):
        self.request = request
        self.redis_util = RedisUtil()
        
    
    def run(self):
        if self.redis_util.get_value_from_redis(self.request.sender, CONTEXT) == WRONG_RESPONSE and self.request.message=="no":
            self.redis_util.remove_key_from_redis(self.request.sender, CONTEXT)
            return [{"recipient_id": self.request.sender,"text":"Select your prefered choice:","buttons":[{"title":"callback","payload":"callback"},{"title":"Transfer to an agent","payload":"handover"},{"title":"Create a ticket","payload":"jira"}]}]
        
        elif self.redis_util.get_value_from_redis(self.request.sender, CONTEXT) == WRONG_RESPONSE:
            self.redis_util.remove_key_from_redis(self.request.sender, CONTEXT)

        search = pipe_faq.run(query=self.request.message)
        if len(search["answers"]) > 0:
            text = search["answers"][0]["answer"]
            image = search["answers"][0]["meta"]["image"]
            video = search["answers"][0]["meta"]["video"]
            confidence_faq = search["answers"][0]["score"]
            logging.info(f'======TEXT : {text}, IMAGE : {image}, VIDEO : {video}=============')
            if confidence_faq!=0 and confidence_faq > 0.85: 
                return OmniChannelResponseUtil.get_response(text, image, video, self.request.sender)
        
        return  atq.generate_answer(self.request.message)
        #prediction = self.generate_answer(self.request.message)               
        # prediction = pipe_atq.run(query = self.request.message, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 1}})