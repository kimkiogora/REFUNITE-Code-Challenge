#This is a smaple script to test RCache Library
#Author <kimkiogora@gmail.com>

from RedisLib import RCache
import json
import pickle
global redis
redis = RCache('localhost', 6379)

listx = {
    '1':'Test',
    '2':'Test'
}

pickled_object = pickle.dumps(listx)

#redis.push('test', pickled_object);

#redis_cache_list = pickle.loads(redis.pop('people_friend_list'))
#redis_cache_list = pickle.loads(redis.pop('test'))

#print redis_cache_list.keys()

redis_cache_list = pickle.loads(redis.pop('people_list'))

listd = []
for i in redis_cache_list:
    if "Samantha" in i:
        listd.append(i)
print listd
