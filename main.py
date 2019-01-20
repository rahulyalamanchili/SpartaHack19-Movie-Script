import os
import json
import shutil
from google_images_download import google_images_download
from urllib.request import Request, urlopen
import urllib.parse
from bs4 import BeautifulSoup, element

response = google_images_download.googleimagesdownload()   # class instantiation

def main():
    text_file = open("test.txt", "r")
    ans_file = open("jsons.txt", "w")
    test = []
    for element in text_file:
        element = element.strip()
        test.append(element)
    # print(test)
    for query in test:
        jsonObj = JSONFormer(query)
        ans_file.write(str(jsonObj))
        print()
    print('Done.')

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
        ix = entry.find('(')
        if (ix != -1):
            entry = entry[:ix-1]
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


def JSONFormer(query):
    valuesDict = {}

    valuesDict["poster_filename"] = imageGrab(query) # use a python library to download the image
    valuesDict["trailer_url"] = beautifulSoupYouTube(query) # use a html scraper to find link

    base_link = 'http://www.omdbapi.com/?apikey=3898c71e' # use an API for all the text info
    link = query.replace(" ", "+")
    url = base_link + '&t=' + link
    html = urllib.request.urlopen(url)
    data = json.loads(html.read())
    if('Error' in data):
        return

    valuesDict["name"] = data['Title']
    valuesDict["release_year"] = int(data['Year'])
    valuesDict["mpaa"] = data['Rated']
    valuesDict["plot"] = data['Plot']
    valuesDict["imdb"] = float(data['imdbRating'])


    valString = data['Runtime']
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
        if(len(moneyString) != 0):
            valuesDict["box_office"] = int(moneyString)
        else:
            valuesDict["box_office"] = 0

    json_data = json.dumps(valuesDict)
    return json_data
    # print(json_data)
    # print('working...')


def imageGrab(query):
    searchTerm = query + ' Poster'
    arguments = {"keywords": searchTerm, "limit": 1, "size": '>2MP',
                 "print_urls": True}  # creating list of arguments
    pathDict = response.download(arguments)  # passing the arguments to the function
    path = pathDict[searchTerm]

    filePath = path[0]
    fileName = query.replace(" ", "") # Remove white spaces from query
    try:
        os.rename(filePath, (os.getcwd()+'\\Posters\\' + fileName + '.jpg')) # Move the file to appropriate directory
    except FileNotFoundError:
        return ''

    shutil.rmtree(os.getcwd()+'\\downloads') # Delete the original directory
    return fileName + '.jpg'


main()

