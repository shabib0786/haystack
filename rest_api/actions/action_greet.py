from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.util.redis_util import RedisUtil
from rest_api.constants import GREET_MESSAGE, RECIPIENT_ID, TEXT
import logging


class ActionGreet(Action):
    def __init__(self, request: OmniChannelRequest):
        self.request = request
        self.redis_util = RedisUtil()

    def run(self):
        name = self.redis_util.get_name(self.request.sender)
        logging.info(f"Name fetched from redis is - {name}")
        if name != None:
            msg = "Hello "+ name +", Please ask your questions."
            return [{RECIPIENT_ID: self.request.sender , TEXT : msg}]    
        else:
            return [{RECIPIENT_ID: self.request.sender , TEXT : GREET_MESSAGE}]