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


def compareLists(query, positional_Index, docsToCheck):
	index_1 = 0 
	index_2 = 0

	for doc in docsToCheck:
		for word in query:
			# get the positioanl indexes lists for all of the words in the query for the given document number
			# save them somewhere so you can access them 

		# compare the lists of positional indexes in the documents that have all of the query words within them 

		# if index 2 and index 2 are in the same position in the document..
		# this would hopefully never happen
		if positional_index[word][doc][index_2] - positional_index[word][doc][index_1] == 0: 
			index_2 += 1
			index_1 += 1
			print "Index 1 and Index 2 have the same value"

		# if the words come continuous to eachother then we have a match! 
		else if positional_index[word][doc][index_2] - positional_index[word][doc][index_1] == 1: 
			# match!
			# record the match somewhere 
			# advance both indexes 
			index_2 += 1
			index_1 += 1

			# repeat again for however many words are in the query.....????
			print "We have a match!"
			
		else if positional_index[word][doc][index_2] - positional_index[word][doc][index_1] > 1: 
			index_1 =+ 1
			print "advance index 1 because 2 is a lot larger"

		else if positional_index[word][doc][index_1] - positional_index[word][doc][index_2] > 1:
			index_2 += 1
			# advance index 2 because index 1 is a lot larger 
			print "Advance index 2 because index 1 is a lot larger"

		# repeat for every word in the document.  Always doing it in pairs of two. 
		# if we have a match, we should advance vertically
		# or we just look at the data post processing and figure out if all words in the query come conescutively?



getLists(formatted_query, posititional_Index)
compareLists(formatted_query, posititional_Index, docsToCheck)


