from rest_api.connection.redis_connect import RedisConnection
from rest_api.constants import REDIS_ERROR
import logging

class RedisUtil:

    def __init__(self):
        self.redis1 = RedisConnection()

    def set_key_in_redis(self, room_id: str, redis_key: str, redis_value: str):
        logging.info(f"Setting key : {redis_key} in redis")
        data = self.redis1.get(room_id)
        if REDIS_ERROR in data:
            data = { redis_key : redis_value}
        else:
            data[redis_key] = redis_value
        self.redis1.save(room_id, data)
        logging.info(f"Successfully saved key : {redis_key} in  redis")
    
    def get_value_from_redis(self, room_id: str, redis_key: str):
        logging.info(f"Getting value for -> key: {redis_key} from redis")
        data = self.redis1.get(room_id)
        if REDIS_ERROR not in data and redis_key in data:
            logging.info(f"Value found for -> key: {redis_key} in redis is {data[redis_key]}")
            return data[redis_key]
        logging.info(f"No value found for -> key: {redis_key} in redis")
        return None

    def remove_key_from_redis(self, room_id: str, redis_key: str):
        logging.info(f"Removing key: {redis_key} from redis")
        data = self.redis1.get(room_id)
        if redis_key in data :
            del data[redis_key]
            self.redis1.save(room_id, data)
        logging.info("Successfully removed key : {redis_key} from redis")






       

  