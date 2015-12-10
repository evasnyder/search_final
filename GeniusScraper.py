import requests, urllib2, time, string, re, pymongo
from bs4 import BeautifulSoup
from time import clock

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
def geniusSearch(search_query):
    search_query = urllib2.quote(search_query)
    response = requests.get("https://api.genius.com/search?q=" + "search_query", headers=headers)
    return response.json()

# should be passed the artist ID we're searching for
def artistSearch(search_query, number_results = ''):
    print ("Sanity test: hearders = " + headers["Authorization"])
    if number_results != '':
        number_results = "?per_page=" + str(number_results)
    else:
        number_results = "?per_page=5000"

    if isinstance(search_query, int):
        request_url = "https://api.genius.com/artists/" + str(search_query) + "/songs" + number_results
        #   print request_url
        response = requests.get(request_url, headers=headers)
    else:
        return "Check input; int not passed for query"

    return response.json()


# should be passed a list of lyric page urls
def lyricHandler(url_list):
    song_list = list()
    for json in url_list:
        url = json['url']
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "lxml")
        artist = soup.find('span', class_='text_artist').text.strip()
        lyrics = soup.find('div', class_='lyrics').text.strip()
        song_title = soup.find('span', class_='text_title').text.strip()

        new_song = Song(song_title, artist, lyrics, url)
        song_list.append(new_song)
    if len(song_list) > 0:
        return song_list
    else:
        return None



# runner function for file; pass a base artist ID and the bounds artist ID
def scrapeLyricsByArtist(base, top_bound = None):
    artist_list = list()
    if top_bound != None:
        for i in range(base, top_bound):
            artist_test = artistSearch(i, 2000)
            if artist_test["meta"]["status"] != 404:
                artist_list.append(lyricHandler(artist_test["response"]["songs"]))
    else:
        artist_test = artistSearch(base, 4)
        if artist_test["meta"]["status"] != 404:
            artist_list.append(lyricHandler(artist_test["response"]["songs"]))
    if len(artist_list):
        return artist_list
    else:
        None

def scrapeSongByURL(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "lxml")

    artist = soup.find('span', class_='text_artist').text.strip()
    lyrics = soup.find('div', class_='lyrics').text.strip()
    song_title = soup.find('span', class_='text_title').text.strip()

    return Song(song_title, artist, lyrics, url)

def scrapeAnnotationsByURL(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "lxml")
    annotations = soup.find_all('a', class_ = '')
    for block in annotations:
        if 'data-id' in  block.attrs:
            print block.attrs['data-id']
    return soup.prettify()

scrapeAnnotationsByURL('http://genius.com/Kendrick-lamar-king-kunta-lyrics')
