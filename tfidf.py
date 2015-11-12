from __future__ import division
import re, string, math, random
from porter2 import stem


punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))
k = 2

# Split up each document by line break and remove any access white spaces
def tokenize(file_name):
	d = open(file_name, 'r')
	d_text = d.read()
	d.close()

	sentences_d = d_text.split('\n')
	sentences_d.remove('')
	return sentences_d

def remove_stopwords(): 
	stopwords_file = open('stopwords.txt', 'r')
	stopwords = stopwords_file.read()
	stopwords = stopwords.split('\n')
	stopwords_file.close()
	return stopwords

# create a list of query term frequencies per word
def create_querytf_list(query_list, stopwords):
	querytf_list = list()
	for query in query_list:
		# lowercase every query word
		formatted_query = punct.split(query.lower())
		formatted_query = [w for w in formatted_query if w not in stopwords]
		# formatted_query = [stem(w) for w in formatted_query]
		# truncate number from query
		formatted_query = formatted_query[1:]
		querytf_dict = dict()
		# create a list of unique query words
		unique_words = set(formatted_query)
		#remove whitespace
		if '' in unique_words:
			unique_words.remove('')
		#generate tf counts for each unique word in query
		for unique_word in unique_words:
			# if the query we're looking out has the unique word, calculate the number of times it appears
			querytf_dict[unique_word] = formatted_query.count(unique_word)
		querytf_list.append(querytf_dict)
	return querytf_list

# Creat the list of document words formatted and split correctly
def create_docword_list(doc_list, stopwords):
	docword_list = list()
	# for every document in our collection
	for doc in doc_list:
		# lower case everything
		formatted_doc = punct.split(doc.lower())
		formatted_doc = [w for w in formatted_doc if w not in stopwords]
		# formatted_doc = [stem(w) for w in formatted_doc]

		# save the number as the first thing
		formatted_doc = formatted_doc[1:]

		# remove any extra whitespace
		if '' in formatted_doc:
			formatted_doc.remove('')
		# add the formated document to the final list of document
		docword_list.append(formatted_doc)
	return docword_list

# create a list of document words with the frequency of each word 
def create_documenttf_dict(doc_list):
	doctf_dict = dict()
	for doc in doc_list:
		# for each unique word
		for word in set(doc):
			# if we've already seen that word in the document, increment the counter
			if word in doctf_dict:
				doctf_dict[word] += 1
			# else add it to the dict. and set it equal to 1
			else:
				doctf_dict[word] = 1
	return doctf_dict

# get the everage document length for our collection
def get_avg_doclength(documents, collection_length):
	sum = 0
	for doc in documents:
		sum += len(doc)
	return (sum/collection_length)

def output_similarities(documents, querytf_list, documenttf, collection_length, avg_doclength):
	f = open('best.top', 'w')
	# for every query in the list of query term frequencies
	for query_index, query in enumerate(querytf_list):
		# for every document 
		for doc_index, doc in enumerate(documents):
			similarity = 0
			# for the word in the query frequency list 
			for query_word, querytf in query.items():
				# raw term freq. is the number of times the word is in the document you're looking at
				raw_tf = doc.count(query_word)
				# if the query word is in the collection and it is in the document we're looking at
				if (query_word in documenttf) and (raw_tf > 0):
					# calculate the tfidf score for it 
					similarity += (querytf * (raw_tf)/(raw_tf + (k * len(doc)/avg_doclength))) * math.log10(collection_length/documenttf[query_word])
			# write to the file
			f.write(str(query_index + 1) + ' 0 ' + str(doc_index + 1) + ' 0 ' + str(similarity) + ' 0\n')
	f.close()


my_queries = tokenize('qrys.txt')
my_documents = tokenize('docs.txt')
my_stopwords = remove_stopwords()
my_docs = create_docword_list(my_documents, my_stopwords)
my_documenttf = create_documenttf_dict(my_docs)
my_querytf = create_querytf_list(my_queries, my_stopwords)
my_collection_length = len(my_docs)
my_avg_doclength = get_avg_doclength(my_docs, my_collection_length)

output_similarities(my_docs, my_querytf, my_documenttf, my_collection_length, my_avg_doclength)