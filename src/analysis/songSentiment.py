
import nltk
from libinit import preper_
from nltk.tokenize import word_tokenize
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Sentiment():
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.preper = preper_

    def _singleSent(self, sentence):
        ss = self.sia.polarity_scores(sentence)
        tempSentDict = {}
        for k in ss:
            # print('{0}: {1}, '.format(k, ss[k]), end="")
            tempSentDict.update({k:ss[k]})
        return tempSentDict

    def _getSentList(self, lylist):
        """ lylist = self.preper.prepSongLyrics(element['lyrics']) """
        sentList = []
        for elt in lylist:
            sentDictForElt = self._singleSent(elt)
            sentList.append(sentDictForElt)
        return sentList

    def _overallSongSent(self, sentlist):
        pos = neg = neu = compound = count = 0
        for el in sentlist:
            pos += el["pos"]
            neg += el["neg"]
            neu += el["neu"]
            compound += el["compound"]
            count += 1

        oSent = {
            "pos"       : (pos/count),
            "neg"       : (neg/count),
            "neu"       : (neu/count),
            "compound"  : (compound/count)
        }
        return oSent

    def _getPosNeg(self, compound):
        if compound >= 0.05:
            return "POSITIVE"
        return "NEGATIVE"

    def songSent(self, song):
        print("### Sentiment analysis for: %s by %s ###" %(song["track"], song["artist"]))
        lylist = self.preper.prepSongLyrics(song["lyrics"])
        sentList = self._getSentList(lylist)
        oSent = self._overallSongSent(sentList)
        # pn = self._getPosNeg(oSent["compound"])
        # print(">>> %s" %pn)
        return oSent
