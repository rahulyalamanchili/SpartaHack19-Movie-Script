import json
from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup




def main():
    beautifulSoupTest()


def beautifulSoupTest():
    # Conversion from URL into Python Object Tree using urllib and BeautifulSoup
    service_url = 'https://www.google.com/search'
    query = 'ShawShank Redemption'
    params = {
        'query': query,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all(class_="FSP1Dd") # Movie Title
    print(results[0].get_text())

    results = soup.find_all(class_="A1t5ne")
    print(results[0].get_text()) # Release Date
    print(results[2].get_text()) # Directors

    # "brYqc"

main()

