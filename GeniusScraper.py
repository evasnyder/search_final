import requests, urllib2, time, string, re
from bs4 import BeautifulSoup
from shutil import copy2
from time import clock
from os import makedirs

start_time = time.time()
artists_imported_count = 0

# required headers for API access to the Genius services
headers = {"User-Agent": "Eva eats leggings", "Accept": "application/json", "Host":"api.genius.com", "Authorization": "Bearer " + "50Li8ZJ-fN7eCvpeFQTVfkS1ttoWnJMZKkXIxxqax9oBRCoNJ9xJvksqKEHNILCy"}
punct = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))

def remove_stopwords(): 
    stopwords_file = open('stopwords.txt', 'r')
    stopwords = stopwords_file.read()
    stopwords = stopwords.split('\n')
    stopwords_file.close()
    return stopwords

# returns 19 results
def genius_search(search_query):
    search_query = urllib2.quote(search_query)
    response = requests.get("https://api.genius.com/search?q=" + "search_query", headers=headers)
    return response.json()

# should be passed the artist ID we're searching for
def artist_search(search_query, number_results = ''):
    if number_results != '':
        number_results = "?per_page=" + str(number_results)
    if isinstance(search_query, int):
        request_url = "https://api.genius.com/artists/" + str(search_query) + "/songs" + number_results
        print request_url
        response = requests.get(request_url, headers=headers)
    return response.json()

# should be passed a list of lyric page urls
def lyric_handler(url_list):
    global artists_imported_count
    artists_imported_count += 1
    db_file = open('lyrics.json', 'a')
    for json in url_list:
        url = json['url']
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "lxml")
        artist = soup.find('span', class_='text_artist').text.strip()
        lyrics = soup.find('div', class_='lyrics').text.strip()
        song_title = soup.find('span', class_='text_title').text.strip()

        processed_lyrics = punct.split(lyrics.lower())
        processed_lyrics = [w for w in processed_lyrics if w not in stopwords]

        db_file.write(build_document_string(artist, song_title, processed_lyrics, url).encode('utf8') + '\n')
    db_file.close()

# formats scraped information for the json document
def build_document_string(artist, song, lyrics, url):
    return '{\"artist\": \"' + artist + '\", ' + '\"song\": \"' + song + '\", ' + '\"lyrics\": \"' + lyrics + '\", ' + '\"url\": \"' + url + '\"}'



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


my_stopwords = remove_stopwords()
#last run: artist_id 5 thru 6, need a re-run
scrap_lyrics_by_artist(55, 60)
print("--- %s seconds ---" % (time.time() - start_time))
print str(artists_imported_count) + ' artists imported'
