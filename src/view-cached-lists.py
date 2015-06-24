# Author Kim Kiogora <kimkiogora@gmail.com>
from RedisLib import RCache
import pickle

global redis
redis = RCache('localhost', 6379)

people_list = redis.pop('people_list')
if people_list is not None:
    people = pickle.loads(people_list)
    print people

global_friends_list = redis.pop('people_friend_list')
if global_friends_list is not None:
    global_friends = pickle.loads(global_friends_list)
    print global_friends
    
people_suggested = redis.pop('suggestion_list')
if people_suggested is not None:
    suggestion_list = pickle.loads(people_suggested)
    print suggestion_list
