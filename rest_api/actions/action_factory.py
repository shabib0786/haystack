from redis import Redis
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.actions.action_atq import ActionAtq
from rest_api.actions.action_faq import ActionFAQ
from rest_api.actions.action_handover import ActionHandover
from rest_api.actions.action_call_back import ActionCallback
from rest_api.util.redis_util import set_context_as_callback, check_context_callback
from rest_api.constants import CALLBACK

class ActionFactory:
    def create_action(self, action_name,  request: OmniChannelRequest):

        if request.message == CALLBACK or check_context_callback(request.sender):
            if request.message == CALLBACK:
                set_context_as_callback(request.sender)
            return ActionCallback(request)

        elif request.message == 'handover':
            return ActionHandover(request)

        elif action_name == 'faq':
            return ActionFAQ(request)

        elif action_name == 'atq':
            return ActionAtq(request)