from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from haystack.retriever.dense import EmbeddingRetriever
from haystack.pipeline import FAQPipeline
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore

document_store = ElasticsearchDocumentStore(host="elasticsearch", username="", password="",
                                            index="nsl_support_document",
                                            embedding_field="question_emb",
                                            embedding_dim=384,
                                            similarity='cosine')
retriever = EmbeddingRetriever(document_store=document_store, embedding_model="sentence-transformers/all-MiniLM-L6-v2", use_gpu=False)
pipe1 = FAQPipeline(retriever=retriever)

class ActionFAQ(Action):
    def __init__(self, request: OmniChannelRequest):
        self.request = request

    def run(self):
        search = pipe1.run(query=self.request.message)
        if len(search["answers"]) > 0:
            text = search["answers"][0]["answer"]
            image = search["answers"][0]["meta"]["image"]
            confidence = search["answers"][0]["score"]
            if confidence!=0 and confidence > 0.85:
                return [{"recipient_id": self.request.sender , "text" : text , "image": image}]
            else:
                return [{"recipient_id": self.request.sender , "text" : "Going to transfer"}, {"recipient_id": self.request.sender,"text":"I did not find anything in Knowledge base... Select your prefered choice:","buttons":[{"title":"callback","payload":"callback"},{"title":"handover to support","payload":"handover"},{"title":"Raising a jira ticket","payload":"jira"}]}]
            