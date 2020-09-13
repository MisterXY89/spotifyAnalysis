

import importlib.util

def loadFile(moduleName, fileloc):
    spec = importlib.util.spec_from_file_location(moduleName, fileloc)
    classHandle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(classHandle)
    return classHandle

dataHelper = loadFile("module.dataHelper", "../helper/dataHelper.py")
reader_ = dataHelper.Reader()

requestAssistant = loadFile("module.requestAssistant", "../helper/requestAssistant.py")
requestHeaderGenerator_ = requestAssistant.RequestHeaderGenerator()

settings = loadFile("module.Settings", "../helper/settings.py")
spotifyConfig_ = settings.SpotifyConfig()

spotifyAuthFlask = loadFile("module.flaskSpotifyAuth", "flaskSpotifyAuth.py")
spotifyAuthFlask_ = spotifyAuthFlask.FlaskSpotifyAuth()
