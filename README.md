# REFUNITE-Code-Challenge
A simple search engine that improves its results by learning from past user behaviour (previous search queries and profile views)
Create a 'people you may know' feature. Next to each recommended profile, indicate the reason for being selected

Design
--------
Think of a person, lets call him Kim. Kim has X,Y, Z to N friends. Each of Kim's friends follows the same pattern as well, having friends M,N,O to N. Its is therefore likely that Kim may know his/her friends friends. To put this in a logical way, consider the persons and their friends below,

Kim - [ X ,Y , Z ]

X - [ M,N,O ]

Y - [ I,J,K ]

Z - [ A,B,C ]

Therefore, Kim can be said to possibly know [M,N,O,I,J,K,A,B,C to N] through [ X,Y,Z to N]....
Why Python ? Data structures are easy to manipulate, for example merging lists with little effort, dynamic creationas well, speed, broadness (so many libraries). Redis improves the processing and response time. By cacheing redundant data we can effectively spend more time on data we do not have. 

The sample code for this is in the script, people-you-may-know.py

Technology
----------
WebService - developed using the awesome Flask, found here http://flask.pocoo.org/

Python 2.7 & > - http://www.python.org 

Redis for python ( scaling and what not ) - sudo pip install redis, found here https://pypi.python.org/pypi/redis

Redis Server - Ubuntu, use apt-get install redis

How to setup
------------
Install Flask by following instructions from their website. Next, install Redis Server and the redis component for Python ( using pip or any other alternative source). The packages are available from their website. Finally, download the zip for REFUNITE-Code-Challenge, extract it anywhere on your machine,navigate to the src folder and run index.py, for example python index.py. By default, flask will use port 5000. Use the below sample of names,...'Madeline Turner', 'Sophia Goldman', 'Allison Carey', 'Chloe Higgins', 'Zoe Cramer'

Example, in your browser,type http://localhost:5000/refunite/api/v1/search/Zoe Cramer

Sample Test
------------
elinks -dump http://localhost:5000/refunite/api/v1/search/Lily%20Charlson

Response
----------
Failure

{"status": "Nothing found", "person": "Peyton ", "did_you_mean": ["Peyton Goodman", "Peyton Vance", "Peyton Gilbert", "Peyton Hoggarth", "Peyton Wainwright", "Peyton Miller".....], "time_taken_to_respond": "0.14 sec"}


elinks -dump http://localhost:5000/refunite/api/v1/search/Peyton%20Hardman

Success

{"status": "success", "person": "Makayla Fulton ", "time_taken_to_respond": "0.12 sec", "association": ["Mia Gilmore", "Sophia WifKinson", "Layla Hailey", "Audrey Haig", "Brooklyn Youmans", "Bailey Wayne", "Lily Miller", "Abigail Thorndike", "Emma Hoggarth"], "people_(s)he_may_know": ["Zoey Oliver", "Ella Hoggarth", "Khloe Turner", "Sophia Mercer"]}

Association in this case, shows you how the person in the said search knows any other person
