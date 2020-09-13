# https://github.com/vanortg/Flask-Spotify-Auth

import base64, json, requests
import urllib.parse


class FlaskSpotifyAuth(object):
    def __init__(self):
        self.SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
        self.SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token'
        self.RESPONSE_TYPE = 'code'
        self.HEADER = 'application/x-www-form-urlencoded'
        self.REFRESH_TOKEN = ''

    def getAuth(self, client_id, redirect_uri, scope):
        # scope = "&".join(scope.split(" "))
        data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(self.SPOTIFY_URL_AUTH, client_id, redirect_uri, scope)
        print(data)
        return data

    def getToken(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": 'authorization_code', # origin: authorization_code
            "code" : str(code),
            "redirect_uri": redirect_uri #,
        }

        auth_str = bytes('{}:{}'.format(client_id, client_secret), 'utf-8')
        b64_auth_str = base64.b64encode(auth_str).decode('utf-8')

        headers = {
            "Content-Type" : self.HEADER,
            'Accept':'application/json',
            "Authorization" : "Basic {}".format(b64_auth_str)
        }

        # encoded = base64.b64encode(("{}:{}".format(client_id, client_secret)).encode("utf-8"))

        post = requests.post(self.SPOTIFY_URL_TOKEN, data=body, headers=headers)
        print(post.text)
        return self.handleToken(json.loads(post.text))

    def handleToken(self, response):
        auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
        self.REFRESH_TOKEN = response["refresh_token"]
        return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

    def refreshAuth(self):
        body = {
            "grant_type" : "refresh_token",
            "refresh_token" : self.REFRESH_TOKEN
        }

        post_refresh = requests.post(self.SPOTIFY_URL_TOKEN, data=body, headers=self.HEADER)
        p_back = json.dumps(post_refresh.text)

        return self.handleToken(p_back)
