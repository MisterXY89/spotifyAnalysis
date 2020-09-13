
import pickle
import lyricwikia
from PyLyrics import *
from libinit import reader_

class Lyrics:
    def __init__(self):
        self.baseUrl = "http://billboardtop100of.com/"
        self.storeFile = '../../files/songs.pkl' # join(dirname(__file__),
        self.reader = reader_
        self.tracks = self.reader.readSongs()
        self.yearRangePreDef = range(1969, 2020)
        self.errorDict = {}
        self.linesep = ";"

    def loadTracks(self):
        fileStream = open(self.storeFile, "rb")
        loadedTracks = pickle.load(fileStream)
        fileStream.close()
        return loadedTracks

    def getLyricsForSong(self, song, artist):
        print("artist: %s | song: %s" %(artist, song))
        lyrics = lyricwikia.get_lyrics(artist, song, self.linesep)
        return lyrics


    def getLyrics(self, song, artist):
        lyrics = PyLyrics.getLyrics(artist, song)
        print(lyrics)
        return lyrics

    def getLyricsForYear(self, year):
        yearList = self.tracks[str(year)]
        tmpErrorList = []
        for el in yearList:
            print(str(el["position"]) + ".")
            i = yearList.index(el)
            artist = el["artist"]
            song = el["track"]
            try:
                yearList[i]["lyrics"] = self.getLyricsForSong(artist, song)
            except:
                try:
                    print("= FAILED")
                    print("Atempt 2")
                     # exclude features
                    artist = artist.split("feat")[0]
                    artist = artist.split("–")[0]
                    artist = artist.replace("!", "i")
                    artist = artist.split("and")[0]
                    artist = artist.replace("’", "'")
                    song = song.replace("’", "'")
                    song = song.replace("…", "")
                    song = song.split("/")[0]
                    song = song.split("(")[0]
                    song = song.replace("**K", "uck")
                    yearList[i]["lyrics"] = self.getLyricsForSong(artist, song)
                except Exception as e:
                    print("= FAILED")
                    print("Atempt 3")
                    artist = "the " + artist
                    try:
                        yearList[i]["lyrics"] = self.getLyricsForSong(artist, song)
                    except:
                        print("ERROR!")
                        tmpErrorList.append(el)

        self.errorDict[str(year)] = tmpErrorList


    def _storeLyrics(self, obj):
        pickle.dump( obj, open( self.storeFile, "wb" ) )
        print("stored!")

    def addLyrics(self, year, position, lyrics):
        songs = self.reader.readSongs()
        songsForYear = songs[str(year)]
        song = songsForYear[position-1]
        song.lyrics = lyrics
        self.reader.storeSongs(songs)

    def getLyricsRange(self, skipList, yearRange=None):
        if yearRange == None:
            yearRange = self.yearRangePreDef
        for year in yearRange:
            if year in skipList:
                continue
            print("year: " + str(year))
            self.getLyricsForYear(year)
        self.reader.storeSongs(self.tracks)
        print("No lyrics could be found for:")
        print(self.errorDict)
        print(30*"-")
        print("Please add them by hand via the addLyrics(year, position, lyrics) method")


# lyrics = Lyrics()
# lyrics.getLyricsRange()
# input()
