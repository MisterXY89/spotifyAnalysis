
from songSentiment import Sentiment
from libinit import reader_


# Though positive sentiment is derived with the compound score >= 0.05,
# we always have an option to determine the positive, negative & neutrality
# of the sentence, by changing these scores

class Analysis:
    def __init__(self):
        self.songs = reader_.readSongs()
        self.sent = Sentiment()

    def analyse(self, year):
        """ string year """
        songsForYear = self.songs[str(year)]
        for song in songsForYear:
            self.sent.songSent(song)


ana = Analysis()
ana.analyse(2011)
