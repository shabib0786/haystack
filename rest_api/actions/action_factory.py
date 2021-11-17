from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.actions.action_atq import ActionAtq
from rest_api.actions.action_faq import ActionFAQ
from rest_api.actions.action_handover import ActionHandover
from rest_api.actions.action_call_back import ActionCallback

class ActionFactory:
    def create_action(self, action_name,  request: OmniChannelRequest):
        if request.message == 'handover':
            return ActionHandover(request)
        
        elif request.message == 'callback':
            return ActionCallback(request)

        elif action_name == 'faq':
            return ActionFAQ(request)

        elif action_name == 'atq':
            return ActionAtq(request)