from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest

class ActionCallback(Action):
    def __init__(self, request: OmniChannelRequest):
        self.request = request

    def run(self):
        pass