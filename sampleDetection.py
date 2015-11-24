import positIndex, string, re


punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))

lyrics = positIndex.tokenizeFile('test_songs.txt')
my_stopwords = positIndex.remove_stopwords()
my_docs = positIndex.create_docword_list(lyrics, my_stopwords)
positIndex = positIndex.create_posit(my_docs)

query = 'Straight up now'

formatted_query = punct.split(query.lower())
formatted_query = [w for w in formatted_query if w not in my_stopwords]
print formatted_query


def getCombinedLists(query, positIndex):
	for word in query:
		# get the documents that the first word is located in 
		# for every document following, search through all documents in the 

straight_locations = positIndex[formatted_query[0]]
up_locations = positIndex[formatted_query[1]]
print straight_locations
print up_locations


