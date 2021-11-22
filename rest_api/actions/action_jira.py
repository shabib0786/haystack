from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.util.redis_util import RedisUtil
from jira import JIRA
from rest_api.constants import JIRA_STATE_0, JIRA_STATE_1, JIRA_DESCRIPTION, CURRENT_STATE, DESCRIPTION_JIRA, CONTEXT
from rest_api.constants import RECIPIENT_ID, JIRA_SERVER_URL, JIRA_USER, JIRA_TOKEN
from rest_api.constants import TEXT

class ActionJira(Action):

    def __init__(self, request: OmniChannelRequest):
        self.request = request
        self.redis_util = RedisUtil()

    def run(self):
    
        present_state = self.redis_util.get_value_from_redis(self.request.sender, CURRENT_STATE)
        if present_state == JIRA_STATE_0 :
            self.redis_util.set_key_in_redis(self.request.sender, CURRENT_STATE,  JIRA_STATE_1)
            return [{RECIPIENT_ID: self.request.sender , TEXT : JIRA_DESCRIPTION}]
        else:
            self.redis_util.set_key_in_redis(self.request.sender, DESCRIPTION_JIRA, self.request.message)
            self.redis_util.remove_key_from_redis(self.request.sender, CONTEXT)
            self.redis_util.remove_key_from_redis(self.request.sender, CURRENT_STATE)
            auth_jira = JIRA(server = JIRA_SERVER_URL,
                            basic_auth=(JIRA_USER, JIRA_TOKEN))

            description = self.redis_util.get_value_from_redis(self.request.sender, DESCRIPTION_JIRA)            
            auth_jira.create_issue(
                project='10009', summary='Issue from a customer from Chatbot', description=description, issuetype={'name': 'Bug'})

            return[{RECIPIENT_ID: self.request.sender , TEXT : "We have noted your issue. You will receive the ticket number and appropriate notifications about the status of the ticket on your specified email id. Thanks for contacting us. This chat will end now"}]