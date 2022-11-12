import random

import requests, json

linkToSongBenz = 'https://open.spotify.com/track/6BXyD6UUPizpRpA7iOi99r?si=763d7b5f510341ec'

linkToSong500ps = 'https://open.spotify.com/track/4UOXo3xWnxYdTf3sFyRaUG?si=3319f103a1624d04'

authToken = 'secret_mI3KSI70AFcnknpBfPPphKHxVU5IzaLVFLfUb2UtlTD'

databaseId = '5b980b3264f5410fbf3829ce5d7e6f40'

headersShit = {
    "Authorization": "Bearer" + authToken,
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def readDatabase(databaseId):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.post(readUrl, headers={
        "Authorization": f"Bearer {authToken}",
        "Notion-Version": "2022-06-28"
    })

    allNotionData = res.json()
    allMusic = []
    mapSong = allNotionData.get('results')
    for x in mapSong:
        entry = x.get('properties')
        mapList = entry.get('Map').get('multi_select')
        if mapList:
            mapName = mapList[0].get('name')
#            print(mapName)
            songWeight = entry.get('Weight').get('number')
#            print(songWeight)
            songName = entry.get('Song name').get('title')[0].get('plain_text')
#            print(songName)
            songLink = entry.get('Spotify link').get('rich_text')[0].get('plain_text')
#            print(songLink)
            allMusic.append(Song(songName, mapName, songWeight, songLink))
    return allMusic


def chooseMusic(mapName, allSongs):
    listOfSongs = []
    listofWeights = []
    for x in allSongs:
        if x.map == mapName:
            listOfSongs.append(x.link)
            listofWeights.append(x.weight)
    specialSongs = [linkToSongBenz, linkToSong500ps]
    if not listOfSongs:
        return random.choices(specialSongs, weights=(70, 30), k = 1)
    songLink = random.choices(listOfSongs, listofWeights, k=1)
#    print(songLink)
    specialSongs.append(songLink)
    return random.choices(specialSongs, weights=(7, 3, 90))


class Song:
    def __init__(self, name, map, weight, link):
        self.name = name
        self.map = map
        self.weight = weight
        self.link = link



print(chooseMusic('Tick Tock Clock', readDatabase(databaseId)))