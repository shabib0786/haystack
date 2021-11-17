import redis
import json
from rest_api.constants import REDIS_HOST
from rest_api.constants import REDIS_PORT
from rest_api.constants import REDIS_PASSWORD

class RedisConnection:

     def __init__(self):
        self.redis_client = redis.Redis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD)
        
     def save(self, room_id, data : dict):
         self.redis_client.set(room_id, json.dumps(data))

     def get(self, room_id):
         return json.loads(self.redis_client.get(room_id))




