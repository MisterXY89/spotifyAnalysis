
import spacy
import en_core_web_sm
import pickle

class Reader:
    def __init__(self):
        self.songs = 'files/songs_initial.pkl'
        self.json_file = "../../files/billbord_data_weekly_"

    def readSongs(self):
        return self._load(self.songs)

    def storeSongs(self, obj):
        self._store(self.songs, obj)

    def _store(self, file, obj):
        pickle.dump( obj, open( file, "wb" ) )
        print("stored!")

    def _load(self, file):
        fileStream = open(file, "rb")
        data = pickle.load(fileStream)
        fileStream.close()
        return data


    def jsonRead(self, year):
        try:
            with open(self.json_file + str(year) + ".json", "r") as readFile:
                jsonData = json.load(readFile)[year]
        except FileNotFoundError as e:
            jsonData = {}
        return jsonData

    def jsonStore(self, data, year):
        with open(self.json_file + str(year) + ".json", "w") as writeFile:
            json.dump(data, writeFile)


class Preper:
    def __init__(self):
        # self.nlp = spacy.load('en')
        self.nlp = en_core_web_sm.load()

    def prepSongLyrics(self, lyricsText):
        lyricsSplit = lyricsText.split(";")
        fun = lambda x: x != ""
        lyrics = [x for x in lyricsSplit if fun(x)]
        return lyrics

    # tokenize + lemmataize
    def preprocess(self, text):
        return [token.lemma_ for token in self.nlp(text)]

    # punct removal
    # returns tokenslist
    def removePunct(self, tokens):
        allowed = []
        return [word.lower() for word in tokens if word.isalpha() and word not in allowed]

    def getCleanTokens(self, text):
        return self.removePunct(self.preprocess(" ".join(self.prepSongLyrics(text))))

    def getDistinctWords(self, text):
        tokens = self.getCleanTokens(text)
        distinctTokens = []
        distonctCount = 0
        for token in tokens:
            if not token in distinctTokens:
                distonctCount += 1
                distinctTokens.append(token)
        return distonctCount, len(tokens), distinctTokens
