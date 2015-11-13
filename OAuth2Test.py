import requests, urllib2

headers = {"User-Agent": "Weezy", "Accept": "application/json", "Host":"api.genius.com", "Authorization": "Bearer " + "50Li8ZJ-fN7eCvpeFQTVfkS1ttoWnJMZKkXIxxqax9oBRCoNJ9xJvksqKEHNILCy"}

def genius_search(search_query):
    search_query = urllib2.quote(search_query)
    response = requests.get("https://api.genius.com/search?q=" + "search_query", headers=headers)
    return response.json()

def artist_search(search_query, number_results = ''):
    if number_results != '':
        number_results = "?per_page=" + str(number_results)
    if search_query.is_integer():
        response = requests.get("https://api.genius.com/artists/" + "search_query" + "/songs" + number_results, headers=headers)
    return response.json()

me_json = genius_search("I'm mad")

# test for printing some information about a result. Results come in batches of 19 elements from the Search request
print str(me_json["response"]["hits"][18]["result"]['title'])