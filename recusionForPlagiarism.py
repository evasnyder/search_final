positional_lists_for_document ={
	"pizzas" : { "doc1" : [1,2,3,4,5,6,7,8], "doc2": [3,6,8,9,10,15], "doc3": [4,5,8,12,66], "doc4": [1,2,3,4,10]},
	"are": {"doc1" : [9,27,88,100], "doc2": [4,5,11,18], "doc4": [5, 11]},
	"dope": {"doc1" : [10], "doc3": [6, 11, 13, 68], "doc4": [6]}
}


def detect_sample(current_index, query, document_id):
	print "*********** NEW DETECT SAMPLE ***********"
	print "Query: " + str(query)
	# global positional_lists_for_document

	# [20, 40, 67]
	current_positional_list = positional_index[query[0]][document_id]
	print "Current Positional List: " + str(current_positional_list)

	next_index = current_positional_list.index(current_index+1) if current_index+1 in current_positional_list else None

	print "Next Index: " + str(next_index)
	print len(query)

	if next_index != None:
		if len(query) == 1:
			print "we doneeee"
			return True
		else:
			print "We're inside the else!!!"
			print query[1:]
			return detect_sample(current_index+1, query[1:], document_id)
	else:
		return False


# relevant_positional_index: dictionary of all of the positions for all of the docs we're going to be searching
# relevant_positional_index: "word: 1{20, 40, 67}, 2{33,55,77} word2: 2{44,55,66}"

# possible_document_matches: documents that contain every word in the query that you then want to search through
# possible_document_matches: just a list of documents = [1,2,5...n] 
def compareLists(query, relevant_positional_index, possible_document_matches):
	global positional_index
	positional_index = relevant_positional_index

	# songs that contain the sample from the query passed by the user
	sampled_songs = list()

	# Tokenize query
	for document in possible_document_matches:
			print "Document: " + str(document)
			# word: 1{20, 40, 67} ==== gives you [20, 40, 67]
			for position in positional_index[query[0]][document]:
				print "Position we're checking: " + str(position)
				song_contains_query = detect_sample(position, query[1:], document)
				print "Song contains query: " + str(song_contains_query)
				if song_contains_query:
					print "song contains the query"
					sampled_songs.append(document)

	return sampled_songs

print compareLists(["pizzas", "are", "dope"], positional_lists_for_document, ["doc1", "doc4"])
