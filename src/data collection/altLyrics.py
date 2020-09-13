
from libinit import reader_
from lyricsmaster import Genius, LyricWiki, AzLyrics, Lyrics007, MusixMatch, TorController

class LyricsCollection:
    def __init__(self):
        self.allSongs = reader_.readSongs()
        self.provider = Lyrics007()
        self.error = []


    def cleanSong(self, song):
        return "".join([char for char in song if char.isalpha() and char == " "])


    # replace all line breaks with ;
    def prepLyricsForSave(self, lyrics):
        return " ".join([word.replace("\n",";") for word in lyrics.split(" ")])


    def lyricsForSong(self, title, artist):
        success = False
        searchSong = title
        artist = artist
        # searchSongClean = self.cleanSong(searchSong)
        # print(f"{searchSongClean=}")
        lyricsResult = self.provider.get_lyrics(artist, song=searchSong)
        print(f"{lyricsResult=}")
        for album in lyricsResult.albums:
            for song in album.songs:
                if(self.cleanSong(song.title) == searchSongClean):
                    lyrics = self.prepLyricsForSave(song.lyrics)
                    success = True
                    print("FOUND: %s" %song.title)
                    return lyrics
        if not success:
            print("ERROR: %s" %searchSong)
            self.error.append(searchSong)
        return False


    def lyricsForYear(self, year):
        for trackElt in self.allSongs[str(year)]:
            self.lyricsForSong(trackElt)
        print("For the following tracks, no lyrics could be found!")
        print(self.error)
