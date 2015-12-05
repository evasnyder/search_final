from pymongo import MongoClient
from geniusScraper import Song
from datetime import datetime
from bson.objectid import ObjectId

def getDBConnection():

	return MongoClient().lyrics_database

#  Takes a database, a song url, a song artist, and a song title 
#  from our crawler or serialized data and attempts a MongoDB insertion.
#  Returns an ID for the song insert (attempt).
def addSongMetadata(db, url, artist, title):
	song_check = db.songs.find({"url": url})

	song_exists_check = db.songs.find_one({"url": url})
	if song_exists_check == None:
		result = db.songs.insert_one({'url' : url, 'artist' : artist, 'title' : title})
		return result.inserted_id
	else:
		# print "Song with url " + url + " already exists"
		return song_exists_check["_id"]

def getSongID(db, url):
	return db.songs.find_one({"url": url})

def getSongURL(db, id):
	return db.songs.find_one({'_id': ObjectId(id)})["url"]

def getPositionalIndexForWord(word):
	return db.word_index.find_one({"word" :word})["document_dict"]


#  Takes a database, a positional index of ONE song, and that specific 
#  song's id from the .songs Collection. Finds the index in the database for each word passed to it in, 
#  inserts the positional data for that word from the doc calling the method with the song id as a key.
def addPositionalIndex(db, positional_index, song_id):

	song_key = "document_dict." + str(song_id)

	for word, positions in positional_index.iteritems():
		
		db.word_index.update({"word" :word}, {'$addToSet' : {song_key : {'$each' : positions} } }, upsert = True )
		#  Makes sure the positional elements within each song's entry in each word are in order
		db.word_index.update({"word" : word}, {'$push' : {song_key : { '$each' : [], '$sort' : 1} } } )


#  Tests should live here
def lazyTests():
	songs_db = getDBConnection()
	#addSongMetadata(songs_db, "google.com", "Internet", "Your Privacy (Is A Joke To Us)")
	cursor = songs_db.word_index.find()

	for doc in cursor:
		print doc

db = getDBConnection()
# print getSongID(db, "http://genius.com/Jay-z-heart-of-the-city-aint-no-love-lyrics")
# print getSongID(db, "http://genius.com/J-cole-forbidden-fruit-lyrics")



#lazyTests()