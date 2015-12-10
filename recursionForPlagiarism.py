import dBDelegate, tfidf, re, string
from bson.objectid import ObjectId
from collections import Counter

# appropriate_punctuation = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'

def getIntersectingPositionalIndex(db, query):
	intersected_positional_list = dict()
	previous_word = ''
	for word in query:
		intersected_positional_list[word] = {}
		positional_list = dBDelegate.getPositionalIndexForWord(word)


		if len(intersected_positional_list) > 1:
			common_docs = set(intersected_positional_list[previous_word].keys()).intersection(positional_list.keys())
			removals = set(intersected_positional_list[previous_word].keys()).difference(positional_list.keys())

			for document in common_docs:
				intersected_positional_list[word][document] = positional_list[document]
			for removal in removals:
				for word_key in intersected_positional_list:
					if removal in intersected_positional_list[word_key]:
						del intersected_positional_list[word_key][removal]
		else:
			intersected_positional_list[word] = positional_list

		previous_word = word
	return intersected_positional_list[query[0]].keys()
	# return intersected_positional_list

def detectSample(current_index, query, document_id):
	# [20, 40, 67] hello
	current_positional_list = positional_index[query[0]]['document_dict'][document_id]

	# get the next index of the next word to see if it exists and then if it comes right after the current index
	next_index = current_positional_list.index(current_index+1) if current_index+1 in current_positional_list else None

	if next_index != None:
		# if you've looked through the entire query and made it to this point: it samples the query
		if len(query) == 1:
			return True
		else:
			# else call the detect sample again while looking at the next query index
			return detectSample(current_index+1, query[1:], document_id)
	else:
		return False


# relevant_positional_index: dictionary of all of the positions for all of the docs we're going to be searching
# relevant_positional_index: "word: 1{20, 40, 67}, 2{33,55,77} word2: 2{44,55,66}"

# possible_document_matches: documents that contain every word in the query that you then want to search through
# possible_document_matches: just a list of documents = [1,2,5...n] 
def compareLists(query, relevant_positional_index, possible_document_matches):
	global positional_index
	positional_index = relevant_positional_index

	# songs that contain the sample from the query passed by the user
	sampled_songs = list()

	# Searching through all of the documents with every word in the query to see if the words come one after another
	for document in possible_document_matches:
			# word: 1{20, 40, 67} == gives you [20, 40, 67]
			# print positional_index[query[0]]
			for position in positional_index[query[0]]['document_dict'][document]:
				# calling a recursive method to see if the song actually contains the query
				song_contains_query = detectSample(position, query[1:], document)

				# if the song does contain the query, add the document name to a list
				if song_contains_query:
					sampled_songs.append(document)

	for t in sampled_songs:
		print dBDelegate.getSongURL(db, t)
	# print sampled_songs				
	return sampled_songs

def createPositionalIndex(db, query):
	# take away duplicates
	query = set(query)
	relevant_positional_index = {}
	for word in query:
		relevant_positional_index[word] = db.word_index.find_one({"word": word})

	# print relevant_positional_index
	return relevant_positional_index

def createPositionalIndex(db, query):
	# take away duplicates
	query = set(query)
	relevant_positional_index = {}
	for word in query:
		relevant_positional_index[word] = db.word_index.find_one({"word": word})

	# print relevant_positional_index
	return relevant_positional_index
	
db = dBDelegate.getDBConnection()
query = ["what", "you", "eat", "don't", "make", "me", "shit"]

relevant_positional_index = createPositionalIndex(db, query)

songs_that_contain_all_query_words = getIntersectingPositionalIndex(db, ["what", "you", "eat", "don't", "make", "me", "shit"])

compareLists(query, relevant_positional_index, songs_that_contain_all_query_words)

my_stopwords = tfidf.remove_stopwords()
my_songs = tfidf.create_song_list(songs_that_contain_all_query_words, my_stopwords)
my_songtf = tfidf.create_songtf_dict(my_songs)
my_querytf = tfidf.create_querytf_list(query, my_stopwords)
my_collection_length = len(my_songs)
my_avg_songlength = tfidf.get_avg_songlength(my_songs)

tfidf.output_similarities(my_songs, my_querytf, my_songtf, my_collection_length, my_avg_songlength)






