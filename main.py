import json
from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup




def main():
    beautifulSoupTest()


def beautifulSoupTest():
    service_url = 'https://www.google.com/search'
    query = 'Good Will Hunting'
    params = {
        'query': query,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

main()

