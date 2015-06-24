# REFUNITE-Code-Challenge
A simple search engine that improves its results by learning from past user behaviour (previous search queries and profile views)
Create a 'people you may know' feature. Next to each recommended profile, indicate the reason for being selected

Technology
----------
WebService - developed using the awesome Flask, found here http://flask.pocoo.org/

Python 2.7 & > - http://www.python.org 

Redis for python ( scaling and what not ) - sudo pip install redis, found here https://pypi.python.org/pypi/redis

Redis Server - Ubuntu, use apt-get install redis

Sample Test
------------
elinks -dump http://localhost:5000/refunite/api/v1/search/Lily%20Charlson

Response
----------
{"status": "Lily Charlson was not found", "message": "Did you mean {} ?","time_taken_to_respond": "0.30 sec"}

