from rest_api.connection.redis_connect import RedisConnection
import json
from rest_api.constants import CONTEXT
from rest_api.constants import CALLBACK
from rest_api.constants import CALLBACK_STATE
from rest_api.constants import CALLBACK_STATE_0
from rest_api.constants import MOBILE_NO
import logging

def set_context_as_callback(room_id: str):
    logging.info("Setting context in redis")
    redis1 = RedisConnection()
    data = {CONTEXT : CALLBACK, CALLBACK_STATE : CALLBACK_STATE_0}
    redis1.save(room_id, data)
    logging.info("Successfully set context in redis")

def unset_context_callback(room_id: str):
    logging.info("Unsetting context in redis")
    redis1 = RedisConnection()
    redis1.delete(room_id)
    logging.info("Successfully removed context in redis")

def check_context_callback(room_id: str) -> bool:
    logging.info("Checking context in redis")
    redis1 = RedisConnection()
    if redis1.get(room_id) != None:
        redis_data = redis1.get(room_id)
        if CONTEXT in redis_data and redis_data[CONTEXT] == CALLBACK :
            return True
    return False

def get_callback_state(room_id: str):
    redis1 = RedisConnection()
    if redis1.get(room_id) != None:
        redis_data = redis1.get(room_id)
        return redis_data[CALLBACK_STATE]
    
def set_callback_state(room_id: str, callback_state: str):
    redis1 = RedisConnection()
    if redis1.get(room_id) != None:
        redis_data = redis1.get(room_id)
        redis_data[CALLBACK_STATE] = callback_state
        redis1.save(room_id, redis_data)

def set_mobile_no(room_id: str, mobile_no: str):
    redis1 = RedisConnection()
    if redis1.get(room_id) != None:
        redis_data = redis1.get(room_id)
        redis_data[MOBILE_NO] = mobile_no
        redis1.save(room_id, redis_data)


    