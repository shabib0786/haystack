from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.constants import ENTER_MOBILE_NO
from rest_api.constants import INVALID_MOBILE_NO
from rest_api.constants import CALL_WITHIN_BUSINESS_HOURS
from rest_api.constants import ASK_TIME_SLOT
from rest_api.constants import CALLBACK_STATE_0
from rest_api.constants import CALLBACK_STATE_1
from rest_api.constants import CALLBACK_STATE_3
from rest_api.constants import CALLBACK_STATE_5
from rest_api.constants import CALLBACK_STATE_6
from rest_api.constants import RECIPIENT_ID
from rest_api.constants import TEXT
from rest_api.constants import YES, NO
from rest_api.util.redis_util import get_callback_state, set_callback_state, set_mobile_no, unset_context_callback
from rest_api.util.callback_util import validateNumber

class ActionCallback(Action):
    def __init__(self, request: OmniChannelRequest):
        self.request = request

    def run(self):
        present_state = get_callback_state(self.request.sender)
        if present_state == CALLBACK_STATE_1 :
            isValidNumber = validateNumber(self.request.message)  #Validate mobile number     
            if isValidNumber is None :
                set_callback_state(self.request.sender, CALLBACK_STATE_1)
                return [{RECIPIENT_ID: self.request.sender , TEXT : INVALID_MOBILE_NO}]         
            else:  #Valid mobile number
                set_callback_state(self.request.sender, CALLBACK_STATE_3)
                set_mobile_no(self.request.sender, isValidNumber.group())
                return [{RECIPIENT_ID: self.request.sender , TEXT : CALL_WITHIN_BUSINESS_HOURS}]
        elif present_state == CALLBACK_STATE_6:
            unset_context_callback(self.request.sender)
            return [{RECIPIENT_ID: self.request.sender , TEXT : "Thankyou."}]
        elif present_state == CALLBACK_STATE_0:
            set_callback_state(self.request.sender, CALLBACK_STATE_1)
            return [{RECIPIENT_ID: self.request.sender , TEXT : ENTER_MOBILE_NO}]
        elif present_state == CALLBACK_STATE_5:
            set_callback_state(self.request.sender, CALLBACK_STATE_6)
            unset_context_callback(self.request.sender)
            return [{RECIPIENT_ID: self.request.sender , TEXT : "Thankyou."}]
        elif present_state == CALLBACK_STATE_3:
            message = self.request.message
            message = message.upper()
            if message == YES:
                set_callback_state(self.request.sender, CALLBACK_STATE_6)
                unset_context_callback(self.request.sender)
                return [{RECIPIENT_ID: self.request.sender , TEXT : "Thankyou."}]
            elif message == NO:
                set_callback_state(self.request.sender, CALLBACK_STATE_5)
                return [{RECIPIENT_ID: self.request.sender , TEXT : ASK_TIME_SLOT}]


   