from flask import Flask
from flask import render_template
from flask import request
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

# MONGODB_HOST = 'localhost'
# MONGODB_PORT = 27017
# DBS_NAME = 'donorschoose'
# COLLECTION_NAME = 'projects'
# FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'date_posted': True, 'total_donations': True, '_id': False}

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'nba'
COLLECTION_NAME = 'nba'
client=MongoClient()
db = client["nba"]
collection = db["nba"]


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/playerchoose/projects")
def playerchoose_projects():
	# connection = Connection(MONGODB_HOST, MONGODB_PORT)
	# collection = connection[DBS_NAME][COLLECTION_NAME]
	# projects = collection.find(fields=FIELDS)
	# client=MongoClient()
	client=MongoClient()
	db = client[DBS_NAME]
	collection = db[COLLECTION_NAME]
	projects = collection.find({}, {'_id': False})
	json_projects = []
	for project in projects:
		json_projects.append(project)
	# for i in xrange(100):
	# 	json_projects.append(projects[i])
	json_projects = json.dumps(json_projects, default=json_util.default)
	client.close()
	return json_projects

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True)