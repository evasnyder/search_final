import sys, GeniusScraper, dBDelegate, positionalIndex
from datetime import datetime

def main(self):
	var = raw_input("Please enter lyrics you'd like to search for: ")
	client = MongoClient()
	db = client.test

	# search through lyrics in the inverse doucument database that have the first word of the query


#def initialize(self):

def test_main(base, cap):

	artist_list = GeniusScraper.scrapeLyricsByArtist(base, cap)
	if artist_list != None:
		for song_list in artist_list:
			for song in song_list:
				db = dBDelegate.getDBConnection()
				song_lyrics = positionalIndex.tokenizeText(song.lyrics)
				song_id = dBDelegate.addSongMetadata(db, song.url, song.artist, song.title)

				song_positional = positionalIndex.createPositionalIndex(song_lyrics)
				dBDelegate.addPositionalIndex(db, song_positional, song_id)

def addTestLyrics(urls):
	db = dBDelegate.getDBConnection()

	for url in urls:
		song = GeniusScraper.scrapeSongByURL(url)

		song_lyrics = positionalIndex.tokenizeText(song.lyrics)
		lyrics = positionalIndex.tokenizeLyrics(song.lyrics)
		song_id = dBDelegate.addSongMetadata(db, song.url, song.artist, song.title)

		song_positional = positionalIndex.createPositionalIndex(song_lyrics)
		dBDelegate.addPositionalIndex(db, song_positional, song_id)


test_main(20,31)
addTestLyrics(["http://genius.com/Jay-z-heart-of-the-city-aint-no-love-lyrics", "http://genius.com/J-cole-forbidden-fruit-lyrics"])