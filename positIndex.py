from __future__ import division
import re, string, math, random
from collections import defaultdict
import json

import crawler


punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))
k = 2

# Split up each document by line break and remove any access white spaces
def tokenizeFile(file_name):
	lyrics = open(file_name, 'r')
	lyrics_text = lyrics.read()
	lyrics.close()

	sentences_lyrics = lyrics_text.split('\n')
 	# sentences_lyrics.remove('')
	return sentences_lyrics

def tokenizeSample(sample):
	sentences_sample = sample.split('\n')
	sentences_sample.remove('')
	return sentences_sample

def remove_stopwords(): 
	stopwords_file = open('stopwords.txt', 'r')
	stopwords = stopwords_file.read()
	stopwords = stopwords.split('\n')
	stopwords_file.close()
	return stopwords
# Creat the list of document words formatted and split correctly
def create_docword_list(doc_list, stopwords):
	docword_list = list()
	# for every document in our collection
	for doc in doc_list:
		# lower case everything
		formatted_doc = punct.split(doc.lower())
		formatted_doc = [w for w in formatted_doc if w not in stopwords]

		# save the number as the first thing
		formatted_doc = formatted_doc[1:]

		# remove any extra whitespace
		if '' in formatted_doc:
			formatted_doc.remove('')
		# add the formated document to the final list of document
		docword_list.append(formatted_doc)
	return docword_list

def create_posit(split_doc):
	posit_index = {}
	posit_counter = 0
	song_counter = 0
	for song in split_doc:
		# reset the positional counter back to zero when you go to the next song
		posit_counter = 0
		for word in song:
			# if the word is already in the positional index 
			if word in posit_index: 
				# locations_of_words = {}
				locations_of_words = posit_index[word]
				#print locations_of_words
					
				# the word is appearing twice in the same song...
				if song_counter in locations_of_words:
					# print 'index alreadyyy ' + str(posit_index) + str(word)

					test = [locations_of_words[song_counter]]
					print 'LIST LIST TEST TEST ' + str(test)
					test.append(posit_counter)
					locations_of_words[song_counter] = test
					print test





				# if we're looking at a new song add the positional a new song list
				else:
					test = list() 
					test.append(posit_counter)
					# print 'new song bitches' + str(test)
					locations_of_words[song_counter] = posit_counter
				
				# if we have the same word in the same document...
				# else: 
					# add the positional to the list already there
					# test = {}
					# test = locations_of_words[song_counter]
					# print 'test test test ' + str(test)
					# test += posit_counter
					# test.insert(len(test), posit_counter)
					# test.append(posit_counter)
					# print test
					# locations_of_words[song_counter] = locations_of_words[song_counter] + (posit_counter)
					# print 'same word in same song...' + str(test)
					#song[song_counter] = song[song_counter] + [posit_counter]
					# test.append(posit_counter)
					# song[song_counter] = test
				
				# posit_index[word] = locations_of_words

			# if the word is not in the positional index yet
			else:
				locations_of_words = {}
				locations_of_words[song_counter] = posit_counter
				posit_index[word] = locations_of_words
			posit_counter += 1
		song_counter += 1
	print posit_index


lyrics = tokenizeFile('test_songs.txt')
print lyrics
my_stopwords = remove_stopwords()
my_docs = create_docword_list(lyrics, my_stopwords)
print my_docs
create_posit(my_docs)