
import pickle
import requests
from libinit import reader_, requestHeaderGenerator_
from os.path import join, dirname
from bs4 import BeautifulSoup, SoupStrainer

class Tracks:
    def __init__(self):
        self.baseUrl = "http://billboardtop100of.com/"
        self.overallTrackDict = {}
        self.yearRange = range(1969, 2020)
        self.reader = reader_
        self.rhg = requestHeaderGenerator_
        self.songs = self.reader.readSongs()

    def _getSoup(self, url):
        try:
            response = requests.get(url, headers = self.rhg.getRandomRequestHeader())
        except Exception as err:
            print(f"Error: {err}")
            return False
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "lxml")
            print(f"OK! Url: {url}")
            return soup
        else:
            print(f'Something went wrong. Got the following response code: {response.status_code}')
            return None

    def _parse(self, soup):
        songTable = soup.findAll("tr")
        trackList = []
        for songRow in songTable:
            cols = songRow.findAll("td")
            soloTrackDict = {
                "position" : cols[0].get_text(),
                "artist"   : cols[1].get_text(),
                "track"    : cols[2].get_text()
            }
            trackList.append(soloTrackDict)
        return trackList

    def _buildUrl(self, year):
        return f"{self.baseUrl}{year}-2/"

    def crawl(self, year):
        res = 0
        url = self._buildUrl(year)
        print("Downloading songs for: %s" %year)
        soup = self._getSoup(url)
        if soup != None:
            res = {str(year): self._parse(soup)}
        return res

    def crawlRange(self, skipList):
        for year in self.yearRange:
            if year in skipList:
                print("skipped: %s" %year)
                continue
            self.songs.update(self.crawl(year))
            self.reader.storeSongs(self.songs)
            print(">> Stored: %s!" %year)
            print("-- done --")


# tracks = Tracks()
# tracks.crawlRange()
# input()
