__author__ = 'kim kiogora <kimkiogora@gmail.com>'

from flask import Flask
import json
from RedisLib import RCache
import urllib2
import sys
import time
import itertools

app = Flask(__name__)

# Define the local JSON retrieval URL
global data_url
data_url = "http://localhost/people.json"

# Create a persistent connection to redis
global redis
redis = RCache('localhost', 6379)


@app.route("/")
def index():
    return "Usage: Flask Search Sample"

"Find all related people a person may know"
def suggested_friends(global_friend_list, related_friends):
    relations = []
    for m in related_friends:
        if m in global_friend_list.keys():
            relations.append(global_friend_list[m])

    return relations

@app.route("/refunite/api/v1/search/<name>", methods=['GET'])
def search(name):
    global response
    response = {}
    if name is None or len(name) == 0:
        data = {
            'status': '500',
            'message': 'Provide a name to search'
        }
        response = data
    else:
        "Do stuff"
        data = {
            'status': 'success',
            'person': name,
            'message': 'Not found',
            'friends': {},
            'people_you_may_know': 'Not found',
        }
        "Process data here"
        start_time = time.time()
        user_data = redis.pop(name, 'people_list')
        if user_data is None:
            "Data not in redis, may be the first time search is being done" \
                "Iterate, local json url, http://localhost/people.json"
            try:
                url_conn = urllib2.urlopen(data_url)
                json_raw = url_conn.read()
                json_object = json.loads(json_raw)
                resp = json_object

                "Work on the data here" \
                    "Filter, map-reduce then return appropriate response"
                person_list = []
                global_friends_list = {}

                for person in resp['result']:
                    person_is = person['name']
                    friends = person['friends']
                    person_list.append(person_is)
                    fl = []
                    for v in friends:
                        fl.append(v['name'])
                    global_friends_list[person_is] = fl

                "Push to redis for cache"
                # redis.push('people_list', person_list)
                # redis.push('people_friend_list', global_friends_list)

                for j, k in enumerate(person_list):
                    if k == name:
                        "identify people 'this' person may know"
                        persons_friends = global_friends_list[name]

                        global pymk
                        pymk = suggested_friends(global_friends_list, persons_friends)

                        response = {
                            'person': '%s ' % name,
                            'status': 'success',
                            #'friends': persons_friends,
                            'people_you_may_know': pymk,
                        }
                        break

                if len(response) <= 0:
                    "reverse search, that is from bottom up[ friends of friends ]"\
                        "get all the people, this persons friends are friends with"
                    other_p = []
                    for v in global_friends_list.keys():
                        if name in global_friends_list[v]:
                            sugg_list = global_friends_list[v]
                            if name in sugg_list: sugg_list.remove(name)
                            other_p.append(sugg_list)

                    response['message'] = '%s found' % name
                    response['people_you_may_know'] = other_p
            except:
                response = {'error': '' % sys.exc_info()[0]}
        else:
            response = user_data
        end = time.time()
        delta = end - start_time

        response['time_taken_to_respond'] = "%.2f sec" % delta
    return json.dumps(response)


"Instantiate the application"
if __name__ == "__main__":
    app.run(debug=True)
