import positionalIndex, string, re


punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))

lyrics = positionalIndex.tokenizeFile('test_songs.txt')
my_stopwords = positionalIndex.get_stopwords()
my_docs = positionalIndex.create_docword_list(lyrics, my_stopwords)
posititional_Index = positionalIndex.create_posit(my_docs)

query = 'Straight up now'

formatted_query = punct.split(query.lower())
formatted_query = [w for w in formatted_query if w not in my_stopwords]
print formatted_query

query_word_list = {}
positional_list = {}

docsToCheck = []


def getLists(query, posititional_Index):
	smallest_value = 9999999999;
	wordInLeastDocuments = " ";

	for word in query:
		print posititional_Index[word]
		currentNumKeys = len(posititional_Index[word].keys())
		print "How Many Documents: " + str(len(posititional_Index[word].keys()))

		if currentNumKeys < smallest_value:
			smallest_value = currentNumKeys
			wordInLeastDocuments = word

   	print "Word in the least amount of docs: " + str(wordInLeastDocuments) + ' ' +  str(smallest_value)
   	print posititional_Index[wordInLeastDocuments].keys()

   	for doc in posititional_Index[wordInLeastDocuments].keys():
   		for word in query: 
   			if doc not in posititional_Index[word].keys():
   				break
   			if doc not in docsToCheck:
   				docsToCheck.append(doc)
   	print 'docs to check: ' + str(docsToCheck)


def compareLists(query, posititional_Index, docsToCheck):
	index_1 = 0 
	index_2 = 0

	for doc in docsToCheck:
		for word in query:
			print posititional_Index[word][doc]
			
	# compare the lists of positional indexes in the documents that have all of the query words within them 


getLists(formatted_query, posititional_Index)
compareLists(formatted_query, posititional_Index, docsToCheck)


