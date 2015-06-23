__author__ = 'kim kiogora <kimkiogora@gmail.com>'

from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def index():
  return "Usage: Elastic Search Sample"

@app.route("/refunite/api/v1/search/<name>", methods=['GET'])
def search(name):
  pass
