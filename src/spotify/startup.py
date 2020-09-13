# https://github.com/vanortg/Flask-Spotify-Auth

from libinit import spotifyConfig_, spotifyAuthFlask_

class SpotifyAuthStartup:
    def __init__(self, scopes):
        self.SAF = spotifyAuthFlask_
        #Add your client ID
        self.CLIENT_ID = spotifyConfig_.CLIENT_ID
        #aDD YOUR CLIENT SECRET FROM SPOTIFY
        self.CLIENT_SECRET = spotifyConfig_.CLIENT_SECRET
        #Port and callback url can be changed or ledt to localhost:5000
        self.PORT = "5000"
        self.CALLBACK_URL = "http://localhost"
        self.CALLBACK_ROUTE = "callback/"
        self.REDIRECT_URI = "{}:{}/{}".format(self.CALLBACK_URL, self.PORT, self.CALLBACK_ROUTE)
        #Add needed scope from spotify user
        self.SCOPE = scopes
        #token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
        self.TOKEN_DATA = []
        # self.CALLBACK_URL = "https://ismymusicsad.herokuapp.com"
        # self.REDIRECT_URI = "{}/{}".format(self.CALLBACK_URL, self.CALLBACK_ROUTE)

    def getUser(self):
        print(self.REDIRECT_URI)
        return self.SAF.getAuth(self.CLIENT_ID, self.REDIRECT_URI, self.SCOPE)

    def getUserToken(self, code):
        self.TOKEN_DATA = self.SAF.getToken(code, self.CLIENT_ID, self.CLIENT_SECRET, "{}".format(self.REDIRECT_URI))

    def refreshToken(self, time):
        time.sleep(time)
        self.TOKEN_DATA = self.SAF.refreshAuth()

    def getAccessToken(self):
        return self.TOKEN_DATA
