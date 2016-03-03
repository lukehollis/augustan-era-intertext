import pymongo
import json

def mongo(dbname):
	client = pymongo.MongoClient('localhost', 27017, maxPoolSize=None)
	db = client[dbname]

	return db
