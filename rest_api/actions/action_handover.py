from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.constants import CONTENT_TYPE
from rest_api.constants import APPLICATION_JSON
from rest_api.constants import SESSION_ID
from rest_api.constants import ACTION
from rest_api.constants import HANDOVER
from rest_api.constants import ACTION_DATA
from rest_api.constants import TARGET_DEPARTMENT
from rest_api.constants import LIVE_CHAT_1
from rest_api.properties.read_config import *
import json
import requests

class ActionHandover(Action):

    def __init__(self, request: OmniChannelRequest):
        self.request = request

    def run(self):
        headers = { CONTENT_TYPE : APPLICATION_JSON }
        sender_id = self.request.sender

        data = json.dumps({ ACTION : HANDOVER, SESSION_ID : sender_id, ACTION_DATA : {
                          TARGET_DEPARTMENT : LIVE_CHAT_1 }})

        urls_dict = get_config_urls()
        print(urls_dict)
        response = requests.post(urls_dict['incoming_msg_url'], headers=headers, data=data)
        return []