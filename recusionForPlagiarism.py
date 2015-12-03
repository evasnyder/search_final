positional_lists_for_document = {}

def detect_sample(previous_index, query, document_id):
	global positional_lists_for_document
	current_positional_list = positional_lists_for_document[query[0]][document_id]
	speculative_index = 
	next_index = current_positional_list.index(previous_index+1) if q in current_positional_list else None

	if previous_index+1 == next_index:
		if len(query) == 1:
			return True
		else:
			return detect_sample(next_index, query[1:])
	else:
		return False

def compareLists(query, relevant_positional_index, possible_document_matches):
	global positional_index
	positional_index = relevant_positional_index
	sampled_songs = list()
	# Tokenize query
	for document in possible_document_matches:
			for position in positional_index[query[0]][document['_id']]:
				song_contains_query = detect_sample(position, query, document['_id'])
				if song_contains_query:
					sampled_songs.append(document)
					break

	return sampled_songs
