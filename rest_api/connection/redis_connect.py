import redis
import json
from rest_api.constants import REDIS_HOST
from rest_api.constants import REDIS_PORT
from rest_api.constants import REDIS_PASSWORD
from rest_api.constants import REDIS_ERROR

class RedisConnection:

     def __init__(self):
        self.redis_client = redis.Redis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD)
        
     def save(self, room_id, data : dict):
         self.redis_client.set(name = room_id, value =  json.dumps(data), ex = 3600)

     def delete(self, room_id):
         self.redis_client.delete(room_id)

     def get(self, room_id):
         if self.redis_client.get(room_id) != None:
            return json.loads(self.redis_client.get(room_id))
         else: 
            return { REDIS_ERROR : "Key is not present in redis."}




