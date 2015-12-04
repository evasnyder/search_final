positional_lists_for_document ={
	"pizzas" : { "doc1" : [1,2,3,4,5,6,7,8], "doc2": [3,6,8,9,10,15], "doc3": [4,5,8,12,66], "doc4": [1,2,3,4,10]},
	"are": {"doc1" : [9,27,88,100], "doc2": [4,5,11,18], "doc4": [5, 11]},
	"dope": {"doc1" : [10], "doc3": [6, 11, 13, 68], "doc4": [6]}
}


def detectSample(current_index, query, document_id):
	# get the current list of positions that you're looking through
	current_positional_list = positional_index[query[0]][document_id]

	# get the next index of the next word to see if it exists and then if it comes right after the current index
	next_index = current_positional_list.index(current_index+1) if current_index+1 in current_positional_list else None

	if next_index != None:
		# if you've looked through the entire query and made it to this point: it samples the query
		if len(query) == 1:
			return True
		else:
			# else call the detect sample again while looking at the next query index
			return detectSample(current_index+1, query[1:], document_id)
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

	# Searching through all of the documents with every word in the query to see if the words come one after another
	for document in possible_document_matches:
			# word: 1{20, 40, 67} ==== gives you [20, 40, 67]
			for position in positional_index[query[0]][document]:
				# calling a recursive method to see if the song actually contains the query
				song_contains_query = detectSample(position, query[1:], document)

				# if the song does contain the query, add the document name to a list
				if song_contains_query:
					sampled_songs.append(document)

	return sampled_songs

print compareLists(["pizzas", "are", "dope"], positional_lists_for_document, ["doc1", "doc4"])
