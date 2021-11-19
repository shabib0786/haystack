from rocketchat_API.rocketchat import RocketChat
from rest_api.constants import YANTR
from rest_api.constants import ROCKET_CHAT_SERVER_URL
from rest_api.util.redis_util import RedisUtil
import logging


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
    redis_util.set_name_and_email_in_redis(sender_id, name, email) # This line will set name and email in redis cache