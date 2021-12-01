from rest_api.actions.action import Action
from rest_api.controller.omnichannel_request import OmniChannelRequest
from rest_api.constants import ENTER_MOBILE_NO
from rest_api.constants import INVALID_MOBILE_NO
from rest_api.constants import CALL_WITHIN_BUSINESS_HOURS
from rest_api.constants import ASK_TIME_SLOT
from rest_api.constants import CALLBACK_STATE_0, CURRENT_STATE
from rest_api.constants import CALLBACK_STATE_1, CONTEXT
from rest_api.constants import CALLBACK_STATE_3
from rest_api.constants import CALLBACK_STATE_5
from rest_api.constants import CALLBACK_STATE_6, CALLBACK_STATE_4
from rest_api.constants import MOBILE_NO, THANK_YOU_CALLBACK_AFTER_SLOT, THANK_YOU_CALLBACK
from rest_api.constants import VERIFY_MOBILE_NO
from rest_api.constants import RECIPIENT_ID
from rest_api.constants import TEXT, BUTTON
from rest_api.constants import YES, NO
from rest_api.util.redis_util import RedisUtil
from rest_api.util.callback_util import validateNumber
from rest_api.util.rocket_chat_util import send_chat_from_chat_server


class ActionCallback(Action):
    def __init__(self, request: OmniChannelRequest):
        self.request = request
        self.redis_util = RedisUtil()

    def run(self):
        present_state = self.redis_util.get_value_from_redis(self.request.sender, CURRENT_STATE)
        if present_state == CALLBACK_STATE_1 :
            isValidNumber = validateNumber(self.request.message)  #Validate mobile number     
            if isValidNumber is None :
                self.redis_util.set_key_in_redis(self.request.sender, CURRENT_STATE, CALLBACK_STATE_1)
                return [{RECIPIENT_ID: self.request.sender , TEXT : INVALID_MOBILE_NO}]         
            else:  #Valid mobile number
                self.redis_util.set_key_in_redis(self.request.sender, CURRENT_STATE, CALLBACK_STATE_3)
                self.redis_util.set_key_in_redis(self.request.sender, MOBILE_NO, isValidNumber.group())
                return [{RECIPIENT_ID: self.request.sender , TEXT : CALL_WITHIN_BUSINESS_HOURS, BUTTON:[{"title":"yes","payload":"yes"},{"title":"no","payload":"no"}]}]

        elif present_state == CALLBACK_STATE_0:
            mobile_no = self.redis_util.get_value_from_redis(self.request.sender, MOBILE_NO)
            if mobile_no == None:
                self.redis_util.set_key_in_redis(self.request.sender, CURRENT_STATE ,CALLBACK_STATE_1)
                return [{RECIPIENT_ID: self.request.sender , TEXT : ENTER_MOBILE_NO}]
            else:
                text = VERIFY_MOBILE_NO + mobile_no
                self.redis_util.set_key_in_redis(self.request.sender, CURRENT_STATE, CALLBACK_STATE_4)
                return [{RECIPIENT_ID: self.request.sender , TEXT : text}]

        elif present_state == CALLBACK_STATE_4:
            message = self.request.message
            message = message.upper()
            if message == YES:
                self.redis_util.set_key_in_redis(self.request.sender, CURRENT_STATE, CALLBACK_STATE_3)
                return [{RECIPIENT_ID: self.request.sender , TEXT : CALL_WITHIN_BUSINESS_HOURS, BUTTON:[{"title":"yes","payload":"yes"},{"title":"no","payload":"no"}]}]
            else:
                self.redis_util.set_key_in_redis(self.request.sender, CURRENT_STATE, CALLBACK_STATE_1)
                return [{RECIPIENT_ID: self.request.sender , TEXT : ENTER_MOBILE_NO}]

        elif present_state == CALLBACK_STATE_5:
            send_chat_from_chat_server(self.request.sender)
            self.redis_util.remove_key_from_redis(self.request.sender, CONTEXT)
            self.redis_util.remove_key_from_redis(self.request.sender, CURRENT_STATE)
            return [{RECIPIENT_ID: self.request.sender , TEXT : THANK_YOU_CALLBACK_AFTER_SLOT}]

        elif present_state == CALLBACK_STATE_3:
            message = self.request.message
            message = message.upper()
            if message == YES:
                send_chat_from_chat_server(self.request.sender)
                self.redis_util.remove_key_from_redis(self.request.sender, CONTEXT)
                self.redis_util.remove_key_from_redis(self.request.sender, CURRENT_STATE)
                return [{RECIPIENT_ID: self.request.sender , TEXT : THANK_YOU_CALLBACK}]
            elif message == NO:
                self.redis_util.set_key_in_redis(self.request.sender, CURRENT_STATE, CALLBACK_STATE_5)
                return [{RECIPIENT_ID: self.request.sender , TEXT : ASK_TIME_SLOT}]


   