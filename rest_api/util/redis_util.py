from rest_api.connection.redis_connect import RedisConnection
import json
from rest_api.constants import CONTEXT
from rest_api.constants import CALLBACK
from rest_api.constants import CALLBACK_STATE
from rest_api.constants import CALLBACK_STATE_0
from rest_api.constants import MOBILE_NO
from rest_api.constants import NAME
from rest_api.constants import EMAIL
from rest_api.constants import REDIS_ERROR
import logging

class RedisUtil:

    def __init__(self):
        self.redis1 = RedisConnection()

    def set_context_as_callback(self, room_id: str):
        logging.info("Setting context in redis")
        data = self.redis1.get(room_id)
        if REDIS_ERROR in data:
            data = { CONTEXT : CALLBACK, CALLBACK_STATE : CALLBACK_STATE_0}
        else:
            data[CONTEXT]  = CALLBACK
            data[CALLBACK_STATE] = CALLBACK_STATE_0
        self.redis1.save(room_id, data)
        logging.info("Successfully set context in redis")

    def unset_context_callback(self, room_id: str):
        logging.info("Unsetting context in redis")
        data = self.redis1.get(room_id)
        if CONTEXT in data and CALLBACK_STATE in data:
            del data[CONTEXT]
            del data[CALLBACK_STATE]
        self.redis1.save(room_id, data)
        logging.info("Successfully removed context in redis")

    def check_context_callback(self, room_id: str) -> bool:
        logging.info("Checking context in redis")
        if self.redis1.get(room_id) != None:
            redis_data = self.redis1.get(room_id)
            if CONTEXT in redis_data and redis_data[CONTEXT] == CALLBACK :
                return True
        return False

    def get_callback_state(self, room_id: str):
        if self.redis1.get(room_id) != None:
            redis_data = self.redis1.get(room_id)
            return redis_data[CALLBACK_STATE]
    
    def get_name(self, room_id: str):
        redis_data = self.redis1.get(room_id)
        if REDIS_ERROR not in redis_data:
            if NAME in redis_data:
                return redis_data[NAME]
        return None 
    
        
    def set_callback_state(self, room_id: str, callback_state: str):
        if self.redis1.get(room_id) != None:
            redis_data = self.redis1.get(room_id)
            redis_data[CALLBACK_STATE] = callback_state
            self.redis1.save(room_id, redis_data)

    def set_mobile_no(self, room_id: str, mobile_no: str):
        if self.redis1.get(room_id) != None:
            redis_data = self.redis1.get(room_id)
            redis_data[MOBILE_NO] = mobile_no
            self.redis1.save(room_id, redis_data)

    def set_name_and_email_in_redis(self, room_id: str, name: str, email: str):
        logging.info(f"Setting name and email in redis - name : {name} and email : {email}")
        data = {NAME : name, EMAIL : email}
        self.redis1.save(room_id, data)

    # def get_name_and_email(room_id: str):
    #     if self.redis1.get(room_id) != None:
    #         redis_data = self.redis1.get(room_id)
    #         if NAME in redis_data and EMAIL in redis_data:
    #             return True
    #     return False

   
        
    
    