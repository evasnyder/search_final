from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.test

cursor = db.restaurants.find({"grades.score": {"$gt": 30}})

for document in cursor:
    print(document)