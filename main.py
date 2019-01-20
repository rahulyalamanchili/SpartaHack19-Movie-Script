import os
import json
import shutil
from google_images_download import google_images_download
from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup, element

response = google_images_download.googleimagesdownload()   # class instantiation

def main():
    query = 'The Dark Knight'
    # filePath = imageTest(query)
    # fileName = query.replace(" ", "") # Remove white spaces from query
    # os.rename(filePath, (os.getcwd()+'\\Posters\\' + fileName + '.jpg')) # Move the file to appropriate directory
    # shutil.rmtree(os.getcwd()+'\\downloads') # Delete the original directory
    beautifulSoupTest(query)
    # APITest(query)

def giveMeSoup(query):
    # Conversion from URL into Python Object Tree using urllib and BeautifulSoup
    service_url = 'https://www.youtube.com/results?search_query='
    link = query.replace(" ", "+")
    url = service_url + link + "trailer"
    # print(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    return BeautifulSoup(html, 'html.parser')

def collectText(element, textList):
    for child in element.contents:
        if 'Tag' in str(type(child)):
            collectText(child, textList)
        else:
            textList.append(str(child))


def giveMeList(largeString):
    terms = largeString.split(',')
    termList = []
    for entry in terms:
        entry = entry.strip()
        termList.append(entry)
    return termList



def beautifulSoupYouTube(query):

    # Take the HTML tree and find the portion containing relevant info
    soup = giveMeSoup(query)
    # print(soup.prettify())

    first = soup.find("div", class_="yt-lockup-thumbnail contains-addto")
    tagList = first.contents
    children = tagList[0].contents
    attrDict = tagList[0].attrs
    link = attrDict['href']
    url = 'https://www.youtube.com' + link
    return url


def APITest(query):
    valuesDict = {}

    base_link = 'http://www.omdbapi.com/?apikey=3898c71e'
    link = query.replace(" ", "+")
    url = base_link + '&t=' + link
    html = urllib.request.urlopen(url)
    data = json.loads(html.read())

    valuesDict["name"] = data['Title']
    valuesDict["release_year"] = int(data['Year'])
    valuesDict["mpaa"] = data['Rated']
    valuesDict["plot"] = data['Plot']
    valuesDict["imdb"] = float(data['imdbRating'])


    valString = data['Runtime']
    # valString = '152 min'
    timeString = ''
    for char in valString:
        if char.isdigit():
            timeString = timeString + char
    valuesDict["duration"] = int(timeString)

    valuesDict["genres"] = giveMeList(data['Genre'])
    valuesDict["directors"] = giveMeList(data['Director'])

    longList = giveMeList(data['Writer'])
    valuesDict["writers"] = longList[:2]

    longList = giveMeList(data['Actors'])
    valuesDict["actors"] = longList[:5]

    ratingsList = data['Ratings']
    tomatoDict = ratingsList[1]
    percent = tomatoDict['Value']
    percent = percent[:-1] # remove '%' sign
    valuesDict["rotten_tomatoes"] = int(percent)

    valString = data['BoxOffice']
    moneyString = ''
    for char in valString:
        if char.isdigit():
            moneyString = moneyString + char
    valuesDict["box_office"] = int(moneyString)


    print(valuesDict)



def imageTest(query):
    searchTerm = query + ' Poster'
    arguments = {"keywords": searchTerm, "limit": 1, "size": '>2MP',
                 "print_urls": True}  # creating list of arguments
    pathDict = response.download(arguments)  # passing the arguments to the function
    path = pathDict[searchTerm]
    return path[0]


main()

