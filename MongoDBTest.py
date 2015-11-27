from pymongo import MongoClient
from datetime import datetime


def get_db_connection():

	return MongoClient().lyrics_database

#  Takes a database, a song url, a song artist, and a song title 
#  from our crawler or serialized data and attempts a MongoDB insertion.
#  Returns an ID for the song insert (attempt).
def add_song(db, url, artist, title):

	song_check = db.songs.find({"url": url})

	if db.songs.find({"url": url}).count() == 0:
		result = db.songs.insert_one({'url' : url, 'artist' : artist, 'title' : title})
		return result
	else:
		print "Song with url " + url + " already exists"
		return

#  Takes a database, a positional index of ONE song, and that specific 
#  song's id from the .songs Collection. Finds the index in the database for each word passed to it in, 
#  inserts the positional data for that word from the doc calling the method with the song id as a key.
def add_positional_index(db, positional_index, song_id):

	song_key = "document_dict." + song_id

	for word, documents in positional_index.iteritems():

		doc = db.lyrics_database.find({"word": word})[0]
		document_id = doc["_id"]
		
		test_db.update_one({"_id" : document_id}, {'$addToSet' : {song_key : {'$each' : position_data} } } )
		#  Makes sure the positional elements within each song's entry in each word are in order
		test_db.update_one({"_id" : document_id}, {'$push' : {song_key : { '$each' : [], '$sort' : 1} } } )

#  Tests should live here
def lazy_tests():
	songs_db = MongoClient().test
	add_song(songs_db, "google.com", "Internet", "Your Privacy (Is A Joke To Us)")
	add_song(songs_db, "google.com", "Internet", "Your Privacy (Is A Joke To Us)")
	cursor = songs_db.songs.find()

	for doc in cursor:
		print doc