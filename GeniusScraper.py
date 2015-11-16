import requests, urllib2
from bs4 import BeautifulSoup

headers = {"User-Agent": "Weezy", "Accept": "application/json", "Host":"api.genius.com", "Authorization": "Bearer " + "50Li8ZJ-fN7eCvpeFQTVfkS1ttoWnJMZKkXIxxqax9oBRCoNJ9xJvksqKEHNILCy"}

def genius_search(search_query):
    search_query = urllib2.quote(search_query)
    response = requests.get("https://api.genius.com/search?q=" + "search_query", headers=headers)
    return response.json()

def artist_search(search_query, number_results = ''):
    if number_results != '':
        number_results = "?per_page=" + str(number_results)
    if isinstance(search_query, int):
        request_url = "https://api.genius.com/artists/" + str(search_query) + "/songs" + number_results
        print request_url
        response = requests.get(request_url, headers=headers)
    return response.json()

def lyric_handler(url_list):
    for json in url_list:
        url = json['result']['url']
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "lxml")

        date = soup.find('p', class_='release_date song_meta_item')
        if date is not None:
            date = soup.find('p', class_='release_date song_meta_item').text.strip()
        lyrics = soup.find('div', class_='lyrics').text.strip()

       # print 'Lyrics: ', lyrics
        print 'Date: ', date

me_json = genius_search("la di da di")

artist_test = artist_search(1, 2000)
print artist_test['response']['songs'][0]['primary_artist']['name']

#print 'Kendrick Lamar songs returned: ' + str(len(artist_test["response"]))

print len(artist_test['response']['songs'])

lyric_handler(me_json["response"]["hits"])
# test for printing some information about a result. Results come in batches of 19 elements from the Search request

