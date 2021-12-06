RECIPIENT_ID = 'recipient_id'
TEXT = 'text'
BUTTON = 'buttons'
CONTENT_TYPE = 'Content-type'
APPLICATION_JSON = 'application/json'
SESSION_ID = 'sessionId'
ACTION = 'action'
HANDOVER = 'handover'
JIRA = "jira"
ACTION_DATA = 'actionData'
TARGET_DEPARTMENT = 'targetDepartment'
LIVE_CHAT_1 = 'Livechat1'
REDIS_HOST = 'chatbot-cache-master'
REDIS_PORT = 6379
REDIS_PASSWORD = 'redis123'
REDIS_ERROR = 'error'
CONTEXT = "context"
CALLBACK = "callback"
MOBILE_NO = "mobile_number"
DESCRIPTION_JIRA = "description_jira"
YES = "YES"
NO = "NO"
FAQ = "faq"

GREET_MESSAGE = "Hello, Please ask your questions."

NAME = 'name'
EMAIL = 'email'

YANTR = 'yantr'

ROCKET_CHAT_SERVER_URL = 'http://chatserver:3000'

ROCKET_CHAT_EKS_SERVICE_URL = 'http://chatserver:3000/api/v1/channels.messages?roomId='

JIRA_SERVER_URL = 'https://fractalenterprises.atlassian.net'

JIRA_USER = ''
JIRA_TOKEN = ''


ABUSIVE_WORD_RESPONSE = 'Please refrain from using abusive language. How may I help you ?'
ENTER_MOBILE_NO = "Please specify the phone number that will be available."
INVALID_MOBILE_NO = "Number is invalid. Please enter a valid mobile number: "
CALL_WITHIN_BUSINESS_HOURS = "We will call you back on your mobile number within 4 business hours. Is it possible to take the call? "
ASK_TIME_SLOT = "Please specify a time convenient to you within 9am to 6pm Mon-Fri"
VERIFY_MOBILE_NO = "Please Verify your mobile number."
UPDATE_MOBILE_NO = "Do you want to update your mobile number?"
CURRENT_STATE = "state"
THANK_YOU_CALLBACK = "Thank you for contacting us. This chat will end now."
THANK_YOU_CALLBACK_AFTER_SLOT = "Thank you for specifying the time. We will call you within half hour of the specified time on the mobile number listed. This chat will end now."
JIRA_DESCRIPTION = "Please provide the description"
WRONG_RESPONSE = "Wrong response"


CALLBACK_STATE_0 = 0 # get user input
CALLBACK_STATE_1 = 1 # get mobile number
CALLBACK_STATE_3 = 3 # valid mobile number
CALLBACK_STATE_4 = 4 # mobileNumberPresentInContext 
CALLBACK_STATE_5 = 5 # get time slot
CALLBACK_STATE_6 = 6 # done..Success fully
CALLBACK_STATE_7 = 7 # ask queqtion for update mobile number


JIRA_STATE_0 = 0
JIRA_STATE_1 = 1