__author__ = 'kim kiogora <kimkiogora@gmail.com>'
import redis

class RCache:
    # Define a constructor
    def __init__(self, host, port):
        self.redis_obj = redis.StrictRedis(host=host, port=port, db=0)

    # Set the element in the stack
    def push(self, key, data):
        self.redis_obj.set(key,data)

    # Get the element saved in stack
    def pop(self, key, plist):
        data = self.redis_obj.get(plist)
        return data
