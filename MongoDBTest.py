from pymongo import MongoClient
from datetime import datetime


def get_db_connection():
	return MongoClient().lyrics_database

def add_song(db, url, artist, title):
	song_cursor = db.songs.find({"url": url})
	if song_cursor.count() == 0:
		result = db.songs.insert_one({'url' : url, 'artist' : artist, 'title' : title})
		return result
	else:
		print "Song with url " + url + " already exists"
		return

def add_positional_index(db, positional_index, song_id):

	song_key = "document_dict." + song_id

	for word, documents in positional_index.iteritems():

		doc = db.lyrics_database.find({"word": word})[0]
		document_id = doc["_id"]
		
		test_db.update_one({"_id" : document_id}, {'$addToSet' : {song_key : {'$each' : position_data} } } )
		test_db.update_one({"_id" : document_id}, {'$push' : {song_key : { '$each' : [], '$sort' : 1} } } )