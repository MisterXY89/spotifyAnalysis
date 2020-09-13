
import json
from getLyrics import *
from getTop100songs import *
from libinit import reader_
# does not work properly
# from azlyrics.azlyrics import *

from altLyrics import LyricsCollection
from getLyrics import Lyrics

# lc = LyricsCollection()
# lc.lyricsForYear(1969)

# get the tracks
# tracks = Tracks()
# tracks.crawlRange([2011])

# now get the Lyrics
# range = range(1989, 1990)
# lyrics = Lyrics()
# lyrics.getLyricsRange([2011], yearRange = range)

JSON_FILE: str = "../../files/billbord_data_weekly_"

def loadData(year):
    with open(JSON_FILE + str(year) + ".json", "r") as readFile:
        jsonData = json.load(readFile)
        return jsonData[str(year)]

def storeData(data, year):
    with open(JSON_FILE + str(year) + ".json", "w") as writeFile:
        json.dump(data, writeFile)


# for y in list(range(1969, 2020)):
#     content = loadData(y)

def prepSongAndArtist(song, artist):
    song = song.split("/")[0]
    artist = artist.split("/")[0]
    artist = artist.split("feat")[0]
    artist = artist.split("and")[0]
    return song, artist

already: list = []

n = 0
year = 1969
content = loadData(year)
altLyrics = LyricsCollection()
mainLyrics = Lyrics()
errors = 0
for week in content:
    if n > 300:
        break
    for el in content[week]:
    # el = content[week][0]
        title = el["title"]
        artist = el["artist"]

        if title + "." + artist in already:
            continue
        # l = altLyrics.lyricsForSong(title, artist)
        m2 = False
        try:
            m = mainLyrics.getLyricsForSong(artist, title)
        except Exception as e1:
            try:
                l = altLyrics.lyricsForSong(title, artist)
                print(l)
                m = l
            except Exception as e2:
                print("Failed")
                m = False
                errors += 1
        already.append(title + "." + artist)
        if m:
            print(m)
            n += 1
        else:
            print("\n" + 30*"*" + "\n")
        el["lyrics"] = m
    storeData(content, year)


print(errors)
