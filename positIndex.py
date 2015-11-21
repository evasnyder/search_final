from __future__ import division
import re, string, math, random
from porter2 import stem

import crawler


punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))
k = 2

# Split up each document by line break and remove any access white spaces
def tokenizeFile(file_name):
	lyrics = open(file_name, 'r')
	lyrics_text = lyrics.read()
	lyrics.close()

	sentences_lyrics = lyrics_text.split('\n')
	sentences_lyrics.remove('')
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

lyrics = tokenizeFile('test_lyrics.txt')
my_stopwords = remove_stopwords()