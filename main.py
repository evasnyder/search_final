import sys, tfidf, geniusScraper, dBDelegate, positionalIndex
from datetime import datetime

def main(self):
	var = raw_input("Please enter lyrics you'd like to search for: ")
	client = MongoClient()
	db = client.test

	# search through lyrics in the inverse doucument database that have the first word of the query


#def initialize(self):

def test_main(from, to):

	artist_list = geniusScraper.scrapeLyricsByArtist(1, 2)
	if artist_list != None:
			for song_list in artist_list:
				for song in song_list:
					db = dBDelegate.getDBConnection()
					song_lyrics = positionalIndex.tokenizeText(song.lyrics)
					song_id = dBDelegate.addSongMetadata(db, song.url, song.artist, song.title)

					song_positional = positionalIndex.createPositionalIndex(song_lyrics, song_id)
					dBDelegate.addPositionalIndex(db, song_positional, song_id)

					