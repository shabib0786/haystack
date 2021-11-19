from rest_api.actions.action_greet import ActionGreet
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.actions.action_atq import ActionAtq
from rest_api.actions.action_faq import ActionFAQ
from rest_api.actions.action_handover import ActionHandover
from rest_api.actions.action_call_back import ActionCallback
from rest_api.util.redis_util import RedisUtil
from rest_api.constants import CALLBACK, HANDOVER

class ActionFactory:

    def __init__(self):
        self.redis_util = RedisUtil()

    def create_action(self, action_name,  request: OmniChannelRequest):

        if request.message.upper() in ['HELLO', 'HI', 'HEY', 'H', "HII", "HEY DUDE"]:
            return ActionGreet(request)

        if request.message == CALLBACK or self.redis_util.check_context_callback(request.sender):
            if request.message == CALLBACK:
                self.redis_util.set_context_as_callback(request.sender)
            return ActionCallback(request)

        elif request.message == HANDOVER:
            return ActionHandover(request)

        elif action_name == 'faq':
            return ActionFAQ(request)

        elif action_name == 'atq':
            return ActionAtq(request)