import sys, tfidf.py
from pymongo import MongoClient
from datetime import datetime

def main(self):
	var = raw_input("Please enter lyrics you'd like to search for: ")
	client = MongoClient()
	db = client.test

	# search through lyrics in the inverse doucument database that have the first word of the query

	cursor = db.restaurants.find({"grades.score": {"$gt": 30}})

	for document in cursor:
    	print(document)


def initialize(self):	


