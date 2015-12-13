from __future__ import division
import re, string, math, random
import dBDelegate
from bson.objectid import ObjectId
from collections import Counter
from itertools import islice
import itertools
import collections

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

def calculateTfidf(query, positional_index, song, avg_songlength, collection_length, weight, tfidf_vlaues):
	f = open('tfidf_samples.txt', 'a')
	# for song in list_of_matching_documents:
	similarity = 0
	for word in set(query):
		querytf = query.count(word)
		raw_tf = len(positional_index[word]['document_dict'][song])
		songtf = len(positional_index[word]['document_dict'])
		similarity += (querytf * (raw_tf)/(raw_tf + (k * len(song)/avg_songlength))) * math.log10(collection_length/songtf)
	# print (str(song) + ' 0 ' + str(similarity + weight) + ' 0\n')
	tfidf_vlaues[song] = similarity + weight
	f.write(str(song) + ' ' + str(similarity + weight) + '\n')
	f.close()

	return tfidf_vlaues

def sortTfidfValues(tfidf_values):
	sorted_tfidf = sorted(tfidf_values.items(), key=lambda x: x[0])
	sorted_tfidf.reverse()

	top_10_values = itertools.islice(sorted_tfidf, 0, 10)
	for song, tfidf in top_10_values:
		print dBDelegate.getSongURL(db, song), tfidf










