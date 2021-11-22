from rest_api.actions.action_greet import ActionGreet
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.actions.action_atq import ActionAtq
from rest_api.actions.action_faq import ActionFAQ
from rest_api.actions.action_handover import ActionHandover
from rest_api.actions.action_call_back import ActionCallback
from rest_api.util.redis_util import RedisUtil
from rest_api.constants import CALLBACK, CALLBACK_STATE_0, CONTEXT, CURRENT_STATE, HANDOVER, JIRA, JIRA_STATE_0
from rest_api.actions.action_jira import ActionJira


class ActionFactory:

    def __init__(self):
        self.redis_util = RedisUtil()

    def create_action(self, action_name,  request: OmniChannelRequest):

        if request.message.upper() in ['HELLO', 'HI', 'HEY', 'H', "HII", "HEY DUDE"]:
            return ActionGreet(request)

        if request.message == CALLBACK or self.redis_util.get_value_from_redis(request.sender, CONTEXT) == CALLBACK:
            if request.message == CALLBACK:
                self.redis_util.set_key_in_redis(request.sender, CONTEXT, CALLBACK)
                self.redis_util.set_key_in_redis(request.sender, CURRENT_STATE, CALLBACK_STATE_0)
            return ActionCallback(request)
        
        elif request.message == JIRA or self.redis_util.get_value_from_redis(request.sender, CONTEXT) == JIRA:
            if request.message == JIRA:
                self.redis_util.set_key_in_redis(request.sender, CONTEXT, JIRA)
                self.redis_util.set_key_in_redis(request.sender, CURRENT_STATE, JIRA_STATE_0)
            return ActionJira(request)

        elif request.message == HANDOVER:
            return ActionHandover(request)

        elif action_name == 'faq':
            return ActionFAQ(request)

        elif action_name == 'atq':
            return ActionAtq(request)

        