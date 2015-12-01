from __future__ import division
import re, string, math, random
from collections import defaultdict
import json

import crawler
import itertools


punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))
bracket_regex = re.compile('\[.*\]')

# Split up each document by line break and remove any access white spaces
def tokenizeText(lyrics_text):

	# replace bracketed text with blanks
	lyrics = re.sub(bracket_regex, '', lyrics_text)
	# splits text and lowercases
	lyrics = punct.split(lyrics.lower())

 	while '' in lyrics:
		lyrics.remove('')
	
	return lyrics

def getStopwords(): 
	stopwords_file = open('stopwords.txt', 'r')
	stopwords = stopwords_file.read()
	stopwords = stopwords.split('\n')
	stopwords_file.close()
	return stopwords

# Creat the list of document words formatted and split correctly
def createDocwordList(doc_list, stopwords):
	docword_list = list()
	# for every document in our collection
	for doc in doc_list:
		formatted_doc = tokenizeText(doc)
		docword_list.append(formatted_doc)
	return docword_list

def createPositionalIndex(song, song_id):
	posit_index = {}
	posit_counter = 0
	
	for word in song:
		# if the word is already in the positional index 
		if word in posit_index: 
			# the word is appearing twice in the same song...
			posit_index[word].append(posit_counter)
		# if the word is not in the positional index yet
		else:
			posit_index[word] = [posit_counter]
		posit_counter += 1
	return posit_index

<<<<<<< HEAD
lyrics = open("test_songs.txt", 'r')
lyrics_text = lyrics.read()
lyrics.close()
=======
def lazyTests():
	lyrics = open("bracket_test.txt", 'r')
	lyrics_text = lyrics.read()
	lyrics.close()

	toked = createDocwordList([lyrics_text], getStopwords())
	print createPositionalIndex(toked[0], "420blazeit")
>>>>>>> origin/master

lazyTests()