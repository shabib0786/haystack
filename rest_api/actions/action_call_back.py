from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.connection.redis_connect import RedisConnection

class ActionCallback(Action):
    def __init__(self, request: OmniChannelRequest):
        self.request = request

    def run(self):
        redis1 = RedisConnection()
        data = {"context" : "callback"}
        redis1.save(self.request.sender, data)
            