import json
import urllib.request
import urllib.parse

def main():
    googleAPItest()

def googleAPItest():
    """Example of Python client calling Knowledge Graph Search API."""

    api_key = '.AIzaSyB2yq7Wo-OpoA4ZOT60JcbK1B2cv9Lyg5E'
    query = 'Taylor Swift'
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    print (url)
    # response = json.loads(urllib.request.urlopen(url).read())
    # for element in response['itemListElement']:
    #     print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')


main()

