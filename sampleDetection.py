import positIndex


lyrics = positIndex.tokenizeFile('test_songs.txt')
my_stopwords = positIndex.remove_stopwords()
my_docs = positIndex.create_docword_list(lyrics, my_stopwords)
positIndex.create_posit(my_docs)

query = 'Straight up now'


