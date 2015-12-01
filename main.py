import sys, tfidf, geniusScraper, dBDelegate, positionalIndex
from datetime import datetime

def main(self):
	var = raw_input("Please enter lyrics you'd like to search for: ")
	client = MongoClient()
	db = client.test

	# search through lyrics in the inverse doucument database that have the first word of the query


#def initialize(self):

def test_main(from, to):

	artist_list = GeniusScraper.scrape_lyrics_by_artist(1, 2)
	if artist_list != None:
			for song_list in artist_list:
				for song in song_list:
					db = db_delegate.get_db_connection()
					song_id = db_delegate.add_song_metadata(db, song.url, song.artist, song.title)
					