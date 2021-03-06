__author__ = 'kim kiogora <kimkiogora@gmail.com>'

from flask import Flask
import json
from RedisLib import RCache
import urllib2
import sys
import time
import pickle

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


def suggested_friends(global_friend_list, related_friends):
    """
    Function to suggest friends ( people you may know )
    :param global_friend_list:
    :param related_friends:
    :return:list
    """
    relations = []
    for m in related_friends:
        if m in global_friend_list.keys():
            m_list = global_friend_list[m]
            for item in m_list:
                relations.append(item)
    return relations


def process_data(name, person_list, global_friends_list):
    """
    re-usable function to find friend suggestions
    :param name:
    :param person_list:
    :param global_friends_list:
    :return:set
    """
    final_response = {}
    for j, k in enumerate(person_list):
        if k == name:
            "identify people 'this' person may know"
            persons_friends = global_friends_list[name]
            global pymk
            pymk = suggested_friends(global_friends_list, persons_friends)
            resp = {
                'person': '%s ' % name,
                'status': 'success',
                'people_(s)he_may_know': pymk,
            }
            final_response = resp
            break

    if len(response) <= 0:
        "reverse search, that is from bottom up[ friends of friends ]" \
            "get all the people, this persons friends are friends with"
        other_p = []
        for v in global_friends_list.keys():
            if name in global_friends_list[v]:
                suggestion_list = global_friends_list[v]
                if name in suggestion_list: suggestion_list.remove(name)
                for item in suggestion_list:
                    other_p.append(item)
        final_response = other_p
    return final_response

def get_relation(global_friends_list, names):
    relation = []
    for name in names:
        for v in global_friends_list.keys():
            if name in global_friends_list[v]:
                if v not in relation:
                    relation.append(v)
    return relation

@app.route("/refunite/api/v1/search/<name>", methods=['GET'])
def search(name):
    global response
    response = {}
    "Process data here"
    start_time = time.time()

    "Locate the stack [containing people (s)he may know] for this person"
    people_suggested = redis.pop('suggestion_list')
    if people_suggested is not None:
        suggestion_list = pickle.loads(people_suggested)
        global_friends_list = pickle.loads(redis.pop('people_friend_list'))
        if name in suggestion_list.keys():
            response['person'] = '%s ' % name
            response['status'] = 'success'
            response['people_(s)he_may_know'] = suggestion_list[name]
            response['association'] = get_relation(global_friends_list,suggestion_list[name])
            end = time.time()
            delta = end - start_time
            response['time_taken_to_respond'] = "%.2f sec" % delta
            return json.dumps(response)

    user_data = redis.pop('people_list')
    if user_data is None:
        "Data not in redis, may be the first time search is being done" \
            "Iterate, local json url, http://localhost/people.json"
        try:
            url_conn = urllib2.urlopen(data_url)
            json_raw = url_conn.read()
            resp = json.loads(json_raw)

            "Work on the data here" \
                "Filter then return appropriate response"
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
            redis.push('people_list', pickle.dumps(person_list))
            redis.push('people_friend_list', pickle.dumps(global_friends_list))

            p_resp = process_data(name, person_list, global_friends_list)
            response['person'] = '%s ' % name
            response['status'] = 'success'
            response['people_(s)he_may_know'] = p_resp
            response['association'] = get_relation(global_friends_list,p_resp)
        except:
            response = {'error': '' % sys.exc_info()[0]}
    else:
        global_friends_list = pickle.loads(redis.pop('people_friend_list'))
        person_list = pickle.loads(user_data)
        p_resp = process_data(name, person_list, global_friends_list)

        did_you_mean = []
        if len(p_resp) <= 0:
            for i in person_list:
                if name.lower() in i.lower():
                    if i not in did_you_mean:
                        did_you_mean.append(i)
            response['person'] = '%s ' % name
            response['status'] = 'Nothing found'
            response['did_you_mean'] = did_you_mean
        else:
            "Push to redis stack, for faster lookup"
            people_suggested = redis.pop('suggestion_list')
            global new_suggestion_list
            new_suggestion_list = {}
            if people_suggested is not None:
                new_suggestion_list = pickle.loads(people_suggested)
                new_suggestion_list[name] = p_resp
            else:
                new_suggestion_list = {name: p_resp}
            redis.push('suggestion_list', pickle.dumps(new_suggestion_list))
            "Return response"
            response['person'] = '%s ' % name
            response['status'] = 'success'
            response['people_(s)he_may_know'] = p_resp
            response['association'] = get_relation(global_friends_list, p_resp)

    end = time.time()
    delta = end - start_time
    response['time_taken_to_respond'] = "%.2f sec" % delta
    return json.dumps(response)

"Instantiate the application"
if __name__ == "__main__":
    app.run(debug=True)
