from pymongo import MongoClient
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'nba'
COLLECTION_NAME = 'nba'
FIELDS = {"_id" : False,"GAME_ID" : True,"MATCHUP" : True,"LOCATION" : True,"W" : True,"FINAL_MARGIN" : True,"SHOT_NUMBER" : True,"PERIOD" : True,"GAME_CLOCK" : True,"SHOT_CLOCK" : True,"DRIBBLES" : True,"TOUCH_TIME" : True,"SHOT_DIST" : True,"PTS_TYPE" : True,"SHOT_RESULT" : True,"CLOSEST_DEFENDER" : True,"CLOSEST_DEFENDER_PLAYER_ID" : True,"CLOSE_DEF_DIST" : True,"FGM" : True,"PTS" : True,"PLAYER_ID" : True}
client=MongoClient()
db = client["nba"]
collection = db["nba"]
projects = collection.find()

for i in xrange(30):
	print projects[i]