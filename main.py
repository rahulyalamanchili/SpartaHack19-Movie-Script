import os
import shutil
from google_images_download import google_images_download
from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup

response = google_images_download.googleimagesdownload()   # class instantiation

def main():
    query = 'The Fast And The Furious 2001'
    filePath = imageTest(query)
    fileName = query.replace(" ", "") # Remove white spaces from query
    os.rename(filePath, (os.getcwd()+'\\Posters\\' + fileName + '.jpg')) # Move the file to appropriate directory
    shutil.rmtree(os.getcwd()+'\\downloads') # Delete the orginal directory
    print('Done')

def beautifulSoupTest(query):
    # Conversion from URL into Python Object Tree using urllib and BeautifulSoup
    service_url = 'https://www.google.com/search'

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


def imageTest(query):
    searchTerm = query + ' Poster'
    arguments = {"keywords": searchTerm, "limit": 1, "size": '>2MP',
                 "print_urls": True}  # creating list of arguments
    pathDict = response.download(arguments)  # passing the arguments to the function
    path = pathDict[searchTerm]
    return path[0]

main()

