import os
import shutil
from google_images_download import google_images_download
from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup, element

response = google_images_download.googleimagesdownload()   # class instantiation

def main():
    query = 'The Sound of Music'
    # filePath = imageTest(query)
    # fileName = query.replace(" ", "") # Remove white spaces from query
    # os.rename(filePath, (os.getcwd()+'\\Posters\\' + fileName + '.jpg')) # Move the file to appropriate directory
    # shutil.rmtree(os.getcwd()+'\\downloads') # Delete the original directory
    beautifulSoupTest(query)

def giveMeSoup(query):
    # Conversion from URL into Python Object Tree using urllib and BeautifulSoup
    service_url = 'https://www.google.com/search'
    params = {
        'query': query,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    return BeautifulSoup(html, 'html.parser')

def collectText(element, textList):
    for child in element.contents:
        if 'Tag' in str(type(child)):
            collectText(child, textList)
        else:
            textList.append(str(child))


def beautifulSoupTest(query):

    oneVal = ['release date', 'budget', 'box office', 'mpaa rating', 'duration', 'budget', 'box office']
    manyVal = ['genre','reviews','directors','main actors', 'writers']

    soup = giveMeSoup(query + ' ')
    results = soup.find(id = "rhs_block")
    CombinedData = results.contents
    children = CombinedData[0].contents
    kid = children[0].contents
    kidA = kid[0].contents

    textData = []
    collectText(kid[0], textData)
    for element in textData:
        print (element)



def imageTest(query):
    searchTerm = query + ' Poster'
    arguments = {"keywords": searchTerm, "limit": 1, "size": '>2MP',
                 "print_urls": True}  # creating list of arguments
    pathDict = response.download(arguments)  # passing the arguments to the function
    path = pathDict[searchTerm]
    return path[0]

main()

