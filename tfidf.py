from __future__ import division
import re, string, math, random
import dBDelegate
from bson.objectid import ObjectId
from collections import Counter

import crawler

appropriate_punctuation = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'
punct = re.compile(r'[\s{}]+'.format(re.escape(appropriate_punctuation)))
k = 2
db = dBDelegate.getDBConnection()

def remove_stopwords(): 
	stopwords_file = open('stopwords.txt', 'r')
	stopwords = stopwords_file.read()
	stopwords = stopwords.split('\n')
	stopwords_file.close()
	return stopwords

# create a list of query term frequencies per word
# presumes it's already tokenized
def create_querytf_list(tokenized_query, stopwords):
	querytf_dict = dict()
	# create a list of unique query words
	unique_words = set(tokenized_query)
	#remove whitespace
	if '' in unique_words:
		unique_words.remove('')
	#generate tf counts for each unique word in query
	for unique_word in unique_words:
	# if the query we're looking out has the unique word, calculate the number of times it appears
		querytf_dict[unique_word] = tokenized_query.count(unique_word)

	return querytf_dict

# Create the list of document words formatted and split correctly
def create_song_dict(songs, stopwords):
	song_dict = dict()

	for objectid in songs:
		song = db.word_index.find_one({"_id":ObjectId(objectid)})
		lyrics = song["lyrics"]
		lyrics = punct.split(lyrics.lower())
		#  lyrics = [w for w in lyrics if w not in stopwords]

		# remove any extra whitespace
		if '' in lyrics:
			lyrics.remove('')
		# add the formated document to the final list of document
		song_dict[song['url']] = lyrics

	return song_dict

# create a list of document words with the frequency of each word 
def create_songtf_dict(song_dict):
	songtf_dict = dict()
	for song in song_dict.items():
		# for each unique word
		for word in set(song[1]):
			# if we've already seen that word in the document, increment the counter
			if word in songtf_dict:
				songtf_dict[word] += 1
			# else add it to the dict. and set it equal to 1
			else:
				songtf_dict[word] = 1
	return songtf_dict

# get the everage document length for our collection
def get_avg_songlength(song_dict):
	sum_lyrics = 0
	for song in song_dict.items():
		sum_lyrics += len(song[1])

	print sum_lyrics/len(song_dict)
	return sum_lyrics/len(song_dict)


def output_similarities(song_dict, querytf_list, songtf, collection_length, avg_songlength):
	f = open('tfidf_samples.txt', 'w')
	# for every query in the list of query term frequencies
	# for query_index, query in enumerate(querytf_list):
	# 	# for every document 
	for song_url, song in song_dict.iteritems():
		similarity = 0
		# for the word in the query frequency list 
		for query_word, querytf in querytf_list.iteritems():
			# raw term freq. is the number of times the word is in the document you're looking at
			raw_tf = song.count(query_word)
			# if the query word is in the collection and it is in the document we're looking at
			if (query_word in songtf) and (raw_tf > 0):
				# calculate the tfidf score for it 
				similarity += (querytf * (raw_tf)/(raw_tf + (k * len(song)/avg_songlength))) * math.log10(collection_length/songtf[query_word])
		# write to the file
		f.write(str(song_url) + ' 0 ' + str(similarity) + ' 0\n')
	f.close()


def calculateTfidf(query, positional_index, song, avg_songlength, collection_length, weight):
	f = open('tfidf_samples.txt', 'w')
	print song
	# for song in list_of_matching_documents:
	similarity = 0
	for word in set(query):
		querytf = query.count(word)
		raw_tf = len(positional_index[word]['document_dict'][song])
		songtf = len(positional_index[word]['document_dict'])
		similarity += (querytf * (raw_tf)/(raw_tf + (k * len(song)/avg_songlength))) * math.log10(collection_length/songtf)
	
	print weight
	print dBDelegate.getSongURL(db, song)
	print (str(song) + ' 0 ' + str(similarity + weight) + ' 0\n')
	f.write(str(song) + ' 0 ' + str(similarity + weight) + ' 0\n')
	f.close()







