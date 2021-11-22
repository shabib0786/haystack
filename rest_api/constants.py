RECIPIENT_ID = 'recipient_id'
TEXT = 'text'
CONTENT_TYPE = 'Content-type'
APPLICATION_JSON = 'application/json'
SESSION_ID = 'sessionId'
ACTION = 'action'
HANDOVER = 'handover'
ACTION_DATA = 'actionData'
TARGET_DEPARTMENT = 'targetDepartment'
LIVE_CHAT_1 = 'Livechat1'
REDIS_HOST = 'chatbot-data-master'
REDIS_PORT = 6379
REDIS_PASSWORD = 'redis123'
REDIS_ERROR = 'error'
CONTEXT = "context"
CALLBACK = "callback"
MOBILE_NO = "mobile_number"
YES = "YES"
NO = "NO"

GREET_MESSAGE = "Hello, Please ask your questions."

NAME = 'name'
EMAIL = 'email'

YANTR = 'yantr'

ROCKET_CHAT_SERVER_URL = 'http://chatbot-rocketchat:3000'

ABUSIVE_WORD_RESPONSE = 'Please refrain from using abusive language. How may I help you ?'

ENTER_MOBILE_NO = "Enter Your mobile number "
INVALID_MOBILE_NO = "Number is invalid. Please enter a valid mobile number: "
CALL_WITHIN_BUSINESS_HOURS = "We will call you back on your mobile number within 4 business hours. Is it possible to take the call? "
ASK_TIME_SLOT = "Please specify a time convenient to you within 9am to 6pm Mon-Fri"
VERIFY_MOBILE_NO = "Please Varify the mobile number."
UPDATE_MOBILE_NO = "Do you want to update your mobile number ?"
CALLBACK_STATE = "state"

CALLBACK_STATE_0 = 0 # get user input
CALLBACK_STATE_1 = 1 # get mobile number
CALLBACK_STATE_3 = 3 # valid mobile number
CALLBACK_STATE_4 = 4 # mobileNumberPresentInContext 
CALLBACK_STATE_5 = 5 # get time slot
CALLBACK_STATE_6 = 6 # done..Success fully
CALLBACK_STATE_7 = 7 # ask queqtion for update mobile number
