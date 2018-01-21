import pymongo
import json

def mongo(dbname):
	client = pymongo.MongoClient('localhost', 27017, max_pool_size=None)
	db = client[dbname]

	return db
