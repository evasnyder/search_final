import requests, urllib2, time, string, re, pymongo
from bs4 import BeautifulSoup
from shutil import copy2
from time import clock
from os import makedirs

start_time = time.time()
artists_imported_count = 0

# required headers for API access to the Genius services
headers = {"User-Agent": "Eva eats leggings", "Accept": "application/json", "Host":"api.genius.com", "Authorization": "Bearer " + "eohZJiCmMiPQABiPsMeOr7MFtXeT48dqHq-B8kZdP-eJ6yG0_g-NbgidN3F24pFE"}
punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))

class Song:
    def __init__(self, title, artist, lyrics, url):
        self.title = title
        self.artist = artist
        self.lyrics = lyrics
        self.url = url


# returns 19 results - seems to always return the same set of poems
def genius_search(search_query):
    search_query = urllib2.quote(search_query)
    response = requests.get("https://api.genius.com/search?q=" + "search_query", headers=headers)
    return response.json()

# should be passed the artist ID we're searching for
def artist_search(search_query, number_results = ''):

    if number_results != '':
        number_results = "?per_page=" + str(number_results)
    else:
        number_results = "?per_page=5000"

    if isinstance(search_query, int):
        request_url = "https://api.genius.com/artists/" + str(search_query) + "/songs" + number_results
        print request_url
        response = requests.get(request_url, headers=headers)
    else:
        return "Check input; int not passed for query"

    return response.json()


# should be passed a list of lyric page urls
def lyric_handler(url_list):
    for json in url_list:
        url = json['url']
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "lxml")
        artist = soup.find('span', class_='text_artist').text.strip()
        lyrics = soup.find('div', class_='lyrics').text.strip()
        song_title = soup.find('span', class_='text_title').text.strip()

        new_song = Song(song_title, artist, lyrics, url)


# runner function for file; pass a base artist ID and the bounds artist ID
def scrap_lyrics_by_artist(base, top_bound = None):
    if top_bound != None:
        for i in range(base, top_bound):
            artist_test = artist_search(i, 2000)
            if artist_test["meta"]["status"] != 404:
                copy2('lyrics.json', 'backups')
                lyric_handler(artist_test["response"]["songs"])
    else:
        artist_test = artist_search(base, 2000)
        if artist_test["meta"]["status"] != 404:
            copy2('lyrics.json', 'backups')
            lyric_handler(artist_test["response"]["songs"])



#my_stopwords = remove_stopwords()
#last run: artist_id 5 thru 6, need a re-run
#scrap_lyrics_by_artist(55, 60)

print("--- %s seconds ---" % (time.time() - start_time))
print str(artists_imported_count) + ' artists imported'
