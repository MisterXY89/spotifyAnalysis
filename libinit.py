

import importlib.util

def loadFile(moduleName, fileloc):
    spec = importlib.util.spec_from_file_location(moduleName, fileloc)
    classHandle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(classHandle)
    return classHandle

DIR = "src/"

dataHelper = loadFile("module.dataHelper", DIR + "helper/dataHelper.py")
reader_ = dataHelper.Reader()

dataHelper = loadFile("module.dataHelper", DIR + "helper/dataHelper.py")
reader_ = dataHelper.Reader()
preper_ = dataHelper.Preper()

requestAssistant = loadFile("module.requestAssistant", DIR + "helper/requestAssistant.py")
requestHeaderGenerator_ = requestAssistant.RequestHeaderGenerator()

settings = loadFile("module.Settings", DIR + "helper/settings.py")
spotifyConfig_ = settings.SpotifyConfig()

spotifyData = loadFile("module.SpotifyData", DIR + "spotify/spotifyDataGetter.py")

altLyrics = loadFile("module.altLyrics", DIR + "data collection/altLyrics.py")
altLyrics_ = altLyrics.LyricsCollection()

lyrics = loadFile("module.Lyrics", DIR + "data collection/getLyrics.py")
lyrics_ = lyrics.Lyrics()


sentimentAnalyzer = loadFile("module.sentimentAnalyzer", DIR + "analysis/songSentiment.py")
sentimentAnalyzer_ = sentimentAnalyzer.Sentiment()

requestAssistant = loadFile("module.requestAssistant", DIR + "helper/requestAssistant.py")
requestHeaderGenerator_ = requestAssistant.RequestHeaderGenerator()

spotifyAuthFlask = loadFile("module.flaskSpotifyAuth", DIR + "spotify/flaskSpotifyAuth.py")
spotifyAuthFlask_ = spotifyAuthFlask.FlaskSpotifyAuth()

SCOPES = "user-library-read playlist-modify-public playlist-modify-private playlist-read-collaborative user-read-private playlist-read-private user-top-read user-read-recently-played"
spotifyAuthStartup = loadFile("module.startup", DIR + "spotify/startup.py")
spotifyAuthStartup_ = spotifyAuthStartup.SpotifyAuthStartup(SCOPES)
