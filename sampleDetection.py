import positIndex, string, re


punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))

lyrics = positIndex.tokenizeFile('test_songs.txt')
my_stopwords = positIndex.get_stopwords()
my_docs = positIndex.create_docword_list(lyrics, my_stopwords)
positIndex = positIndex.create_posit(my_docs)

query = 'Straight up now'

formatted_query = punct.split(query.lower())
formatted_query = [w for w in formatted_query if w not in my_stopwords]
print formatted_query

query_word_list = {}
positional_list = {}


def getLists(query, positIndex):
	smallest_value = 9999999999;
	wordInLeastDocuments = " ";

	docsToCheck = []

	for word in query:
		print positIndex[word]
		currentNumKeys = len(positIndex[word].keys())
		print "How Many Documents: " + str(len(positIndex[word].keys()))

		if currentNumKeys < smallest_value:
			smallest_value = currentNumKeys
			wordInLeastDocuments = word

   	print "Word in the least amount of docs: " + str(wordInLeastDocuments) + ' ' +  str(smallest_value)
   	print positIndex[wordInLeastDocuments].keys()

   	for doc in positIndex[wordInLeastDocuments].keys():
   		for word in query: 
   			if doc not in positIndex[word].keys():
   				break
   			if doc not in docsToCheck:
   				docsToCheck.append(doc)
   	print 'docs to check: ' + str(docsToCheck)

getLists(formatted_query, positIndex)

# straight_locations = positIndex[formatted_query[0]]
# up_locations = positIndex[formatted_query[1]]
# getCombinedLists(formatted_query, positIndex)


