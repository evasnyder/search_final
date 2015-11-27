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
	for word, documents in positional_index.iteritems():
		word_cursor = db.songs.find({"word": word, "document_dict" : song_id})
		# gets document_dict for the word, iterates through each doc
		#for 
		#returned_doc = word_cursor[0].document_dict
		returned_doc_id = word_cursor[word]['_id']
		print returned_doc_id
		#for doc_number in documents.values:
			#db.update_one({"_id": returned_doc_id}, {'$addToSet': {"document_dict" : {song_id : { $each [doc_number]}}})

def lazy_test(db, word, song_id):
	word_cursor = db.i.find({"word": word})
	# gets document_dict for the word, iterates through each doc
	#for 
	#returned_doc = word_cursor[0].document_dict
	returned_doc_id = word_cursor[word]['_id']
	print returned_doc_id





our_db = get_db_connection()
'''
print add_song(our_db, 'http://genius.com/Paula-abdul-straight-up-lyrics', 'Paula Abdul', 'Straight Up')'''

cursor = our_db.test.find()
test_db = our_db.test
print cursor.count()
for doc in cursor:
	document_id = doc['_id']
	for song, position in doc["document_dict"].iteritems():
		song_key = "document_dict." + song
		#result = test_db.update({"_id" : document_id}, {'$addToSet' : {song_key : {'$each' : [-1, 800, 122], '$sort' : 1 } } } )
		test_db.update_one({"_id" : document_id}, {'$addToSet' : {song_key : {'$each' : [420]} } } )
		test_db.update_one({"_id" : document_id}, {'$push' : { song_key : { '$each' : [], '$sort' : 1} } })
		#print result
		print song, position

#our_db.test.insert_one({'document_dict' : {'no1': [2,3,4], 'no2':[1,4,10], 'no5':[10,15,16]}, 'word': 'eva'})
#our_db.test.insert_one({'document_dict' : {'no2': [4,7,8], 'no3':[1,2,3], 'no6':[106,156,166]}, 'word': 'longjohns'})
#our_db.test.insert_one({'document_dict' : {'aaa' : [1, 2, 3, 10]}, 'word' : 'leggings' })
#lazy_test(our_db, )