from rocketchat_API.rocketchat import RocketChat
from rest_api.constants import CALLBACK, JIRA, MOBILE_NO, YANTR, DESCRIPTION_JIRA
from rest_api.constants import ROCKET_CHAT_SERVER_URL, NAME, EMAIL, ROCKET_CHAT_EKS_SERVICE_URL, CONTEXT
from rest_api.util.redis_util import RedisUtil
import requests
import logging
import smtplib


import json

def set_name_and_email(sender_id: str):
    logging.info("Getting name and email from rocket chat..")
    rocket_chat = RocketChat(YANTR, YANTR, server_url= ROCKET_CHAT_SERVER_URL)
    rocket_chat_response = json.loads(rocket_chat.rooms_info(sender_id).text)
    logging.info(f"Response received from rocket chat is - {rocket_chat_response}")
    token = rocket_chat_response['room']['v']['token']
    rocket_chat_response1 = json.loads(rocket_chat.livechat_get_visitor(token).text)
    logging.info(f"Second Response received from rocket chat is - {rocket_chat_response1}")
    name = rocket_chat_response1['visitor']['name']
    email = rocket_chat_response1['visitor']['visitorEmails'][0]['address']
    redis_util = RedisUtil()
    redis_util.set_key_in_redis(sender_id, NAME, name) # This line will set name  in redis cache
    redis_util.set_key_in_redis(sender_id, EMAIL, email) # This line will set email in redis cache

def send_chat_from_chat_server(room_id: str):
    headers = {'X-Auth-Token': '6_9hQREaj6PKv_s6Exa1PPK7yQKLn3aN9-uLZTrsAa5', 'X-User-Id': 'RAXgXTgLXfv5ARfrN'}
    url_with_roomId = ROCKET_CHAT_EKS_SERVICE_URL + room_id
    logging.info(f'URL is - {url_with_roomId}')
    response = requests.get(url_with_roomId, headers=headers)
    res = json.loads(response.text)
    logging.info(f'Response received in send - {res} -> {type(res)}')
    res1 = res["messages"]
    chat = []

    redis_util = RedisUtil()
    name = redis_util.get_value_from_redis(room_id, NAME)
    if name == None:
        name = "USER"
    j = 0
    for i in reversed(res1):
                if j<=1:
                    j=j+1
                elif i["u"]["username"] == "yantr":
                    str = "BOT: "+i["msg"]+"\n"
                    chat.append(str)
                else:
                    str = name + ": "+i["msg"]+"\n"
                    chat.append(str)
    strz = "The chat is: \n"
    for x in chat:
        strz = strz+x
    logging.info(f'THE CHAT IS - {strz}')
    send_email(room_id, strz)


def send_email(room_id: str, chat: str):
    sender = 'nsltestuser123@gmail.com'
    receivers = ["support@nslhub.com", "vinith.reddy@nslhub.com"]
    redis_util = RedisUtil()
    context = redis_util.get_value_from_redis(room_id, CONTEXT)
    phoneNumber = None
    SUBJECT = None
    if context == CALLBACK:
        phoneNumber = redis_util.get_value_from_redis(room_id, MOBILE_NO)
        SUBJECT = "Callback to {}".format(phoneNumber)
    elif context == JIRA:
        jira_desc = redis_util.get_value_from_redis(room_id, DESCRIPTION_JIRA)
        SUBJECT = "{}".format(jira_desc)
        
    message = 'Subject: {}\n\n{}'.format(SUBJECT, chat)
    message = message.encode('utf8')
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo
    # Authentication
    s.login("nsltestuser123@gmail.com", "tlnwjncqcgcwepqp")
    s.sendmail(sender, receivers, message)
    s.close()