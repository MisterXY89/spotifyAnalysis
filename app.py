from gevent import monkey
monkey.patch_all()

import os
import sys
import json
import time
import spotipy
# from gevent import monkey
from functools import wraps
from flask_socketio import SocketIO
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from libinit import *

# altLyrics_
# sentimentAnalyzer_

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = spotifyConfig_.FLASK_SECRET


# set timezone:
os.environ['TZ'] = 'Europe/Berlin'
time.tzset()

last_origin = ""
tries = 0

signOfTheTimes = "spotify:track:5Ohxk2dO5COHF1krpoPigN"

blueGradient = "blueGradient"
greenGradient = "greenGradient"

def auth(level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # global last_origin
            # last_origin = origin
            if level == "spotify":
                if spotifyAuthStartup_.getAccessToken() == []:
                    return redirect(url_for('spotifyLogin'))
            elif level == "default":
                print("default - page loaded")
            else:
                return redirect(url_for('notAllowed'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route("/not-allowed")
def notAllowed():
    return render_template("notAllowed.html")


@app.route("/analyse", methods=["GET"])
def analyseGet():
    userId = session["userId"]
    pages = spotifyData.SpotifyData(session["spotifyAccessToken"]).getUserPlaylists(userId)
    return render_template("analyse.html", showPlaylists=True, pagination=True, pages=pages)


@app.route("/songAnalyse", methods=["POST"])
def songAnalysePost():
    if "trackURI" in request.form:
        uri = request.form["trackURI"]
        trackInfo = spotifyData.SpotifyData(session["spotifyAccessToken"]).getSongInfo(uri)
        trackName = trackInfo["trackName"]
        artistName = trackInfo["artistName"]
        if "analyseLyrics" in request.form and bool(request.form["analyseLyrics"]):
            lyrics = lyrics_.getLyricsForSong(trackName, artistName)
            if lyrics:
                lyrics = altLyrics_.prepLyricsForSave(lyrics)
                sent = sentimentAnalyzer_.songSent({
                    "track": trackName,
                    "artist": artistName,
                    "lyrics": lyrics
                })
        valence = spotifyData.SpotifyData(session["spotifyAccessToken"]).getBasicValence([uri])
        print(valence)

    return redirect(url_for("songAnalyseOutput", sentiment=sent, valence=valence, trackInfo=trackInfo))

@app.route("/songAnalyse", methods=["GET"])
def songAnalyse():
    return render_template("songAnalyse.html")


@app.route("/songAnalyseOutput")
def songAnalyseOutput():
    args = request.args
    if "sentiment" in args:
        sentiment = args["sentiment"]
        sentiment = sentiment.replace("\'", "\"")
        sentiment = json.loads(sentiment)
    else:
        sentiment = False
    if "trackInfo" in request.args:
        trackInfo = args["trackInfo"]
        trackInfo = trackInfo.replace("\'", "\"")
        trackInfo = json.loads(trackInfo)
    else:
        trackInfo = {}
    if "valence" in args:
        valence = args["valence"]
    else:
        valence = False
    emotion = "Error: Valence unset - try again please."
    if valence:
        if float(valence) > 0.4:
            emotion = "happy"
        else:
            emotion = "sad"
    if sentiment:
        if float(sentiment["compound"]) > 0:
            emotion+= " & happy lyrics"
        else:
            emotion+= " & sad/negative lyrics"
        return render_template("result.html", valence=valence, type="track", sentiment=sentiment, name=trackInfo["trackName"], artist=trackInfo["artistName"], emotion=emotion, imgUrl=trackInfo["imgUrl"], isTrack=True)
    # return jsonify({
    #     "sentimentData": sentiment,
    #     "valence": valence
    # })


@app.route("/searchSong", methods=["POST"])
def searchSong():
    userId = session["userId"]
    status = "Error: unknown :/"
    result = []
    if "query" in request.json:
        query = str(request.json["query"])
        result = spotifyData.SpotifyData(session["spotifyAccessToken"]).search(query)
        # print(result)
        status = "200"
    else:
        status = "Error: Missing parameter"
    return jsonify({
        "status": status,
        "result": result
    })


@app.route("/analyse", methods=["POST"])
# @auth("spotify", "analyse")
def analyse():
    name = ""
    # sd = spotifyData.SpotifyData(session["spotifyAccessToken"])
    if "playlistURI" in request.form:
        uri = str(request.form["playlistURI"])
        if "open.spotify" in uri:
            uriList = uri.split("/")
            uri = "spotify:" + uriList[3] + ":" + uriList[4].split("?")[0]
        type = uri.split(":")[1]
        if type == "track":
            valence = spotifyData.SpotifyData(session["spotifyAccessToken"]).getBasicValence(uri)
            name = spotifyData.SpotifyData(session["spotifyAccessToken"]).getTrackName(uri)
        else:
            print("valence TRY: ")
            # sot = spotifyData.SpotifyData(session["spotifyAccessToken"]).getTrackName(signOfTheTimes)
            # print(sot)
            valence = spotifyData.SpotifyData(session["spotifyAccessToken"]).getBasicPlaylistValence(uri)
            name = spotifyData.SpotifyData(session["spotifyAccessToken"]).getPlaylistName(uri)

    elif "trackIds" in request.json:
        valence = spotifyData.SpotifyData(session["spotifyAccessToken"]).getBasicValence(request.json["trackIds"])
        type = "top songs playlist"
        name = "top songs"
    else:
        print("REQ: %s" %request.json)
        # return redirect(url_for("notAllowed"))

    return redirect(url_for("result", valence=valence, type=type, name=name))

@app.route("/overview")
def overview():
    login = None
    if "login" in request.args:
        login = bool(request.args["login"])
    return render_template("overview.html", login=login)


@app.route("/result")
def result():
    valence = float(request.args["valence"])
    type = str(request.args["type"])
    name = str(request.args["name"])
    emotion = "sad"
    cssClass = blueGradient
    userId = session["userId"]
    pages = spotifyData.SpotifyData(session["spotifyAccessToken"]).getUserPlaylists(userId)
    if valence > 0.52:
        cssClass = greenGradient
        emotion = "happy"
    if valence <= 0.52 and valence >= 0.48:
        emotion = "mixed"

    return render_template("result.html", type=type, valence=valence, cssClass=cssClass, emotion=emotion, name=name, showPlaylists=True, pages=pages, pagination=True)


@app.route("/login")
def spotifyLogin():
    response = spotifyAuthStartup_.getUser()
    print("LOGIN RESPONSE: %s" %response)
    return redirect(response)


@app.route('/callback/')
def callback():
    spotifyAuthStartup_.getUserToken(request.args['code'])
    return redirect(url_for("authSuccess"))


@app.route("/auth-success")
def authSuccess():
    global last_origin
    global tries
    token = spotifyAuthStartup_.getAccessToken()
    if tries > 2:
        return redirect(url_for("index"))
    if len(token) == 0:
        tries += 1
        return redirect(url_for("spotifyLogin"))
    print(token)
    session["spotifyAccessToken"] = token[0]
    sp = spotipy.Spotify(auth=token[0])
    user = sp.current_user()
    # 'images': [{'height': None, 'url': 'https://i.scdn.co/image/ab6775700000ee850a12830ad9804c3d5daf5e2a', 'width': None}],
    # 'product': 'premium', 'type': 'user', 'uri': 'spotify:user:misterxy89'}
    session["username"] = user["display_name"]
    session["country"] = user["country"]
    session["userId"] = user["id"]
    print("--------- AUTH SUCCESS ---------")
    print(token[0])
    print(last_origin)
    return redirect(url_for("overview", login=True))

def extract(item):
    if "val" in item:
        item["track"]["val"] = item["val"]
    return item["track"]


@app.route("/getSongs", methods=["POST"])
def getSongs():
    # print(f"NEW REQ: {request.args}")
    data = request.json
    offset = 0
    type = "sad"
    reqSongs = []
    playlistLength = 15
    songCollectionLimit = 500
    excludeInstrumentals = True
    if "type" in data:
        type = str(data["type"])
    if "offset" in data:
        offset = str(data["offset"])
    if "playlistLength" in data:
        playlistLength = int(data["playlistLength"])
    if "songCollectionLimit" in data:
        songCollectionLimit = int(data["songCollectionLimit"])
    if "excludeInstrumentals" in data:
        excludeInstrumentals = str(data["excludeInstrumentals"])
        if excludeInstrumentals == "on" or excludeInstrumentals:
            excludeInstrumentals = True
        else:
            excludeInstrumentals = False

    print(type)
    print(offset)
    print(playlistLength)
    print(songCollectionLimit)
    print(excludeInstrumentals)

    sp = spotifyData.SpotifyData(session["spotifyAccessToken"])
    print("getting tracks")
    tracks = sp.getUserTracks(songCollectionLimit, excludeInstrumentals, type, offset)
    # if type == "happy":
    #     reqSongs = sorted(tracks, key=lambda k: k['val'])[::-1][:playlistLength]
    # else:
    #     reqSongs = sorted(tracks, key=lambda k: k['val'])[:playlistLength]
    return jsonify({
        "songs": tracks,
        "type": type
    })


@app.route("/getSongDisplay", methods=["POST"])
def getSongDisplay():
    data = request.json
    songs = []
    if "songs" in data:
        songs = data["songs"]
    # print(songs)
    return render_template("includes/songDisplay.html", songs=list(map(extract, songs)))


@app.route("/happy")
def happySongs():
    return render_template("songValencePlaylist.html", type="happy")


@app.route("/sad")
def sadSongs():
    return render_template("songValencePlaylist.html", type="sad")

# user_playlists

@app.route("/createPlaylist")
@auth("spotify")
def createPlaylist():
    description = ""
    if not "name" in request.args:
        name = "A Spotify insights playlist"
    else:
        name = request.args["name"]
    sp = spotipy.Spotify(auth=spotifyAuthStartup_.getAccessToken()[0])
    res = sp.user_playlist_create(session["userId"], name, public=True, description=description)
    return jsonify({
        "uri" : res["uri"],
        "url" : res["external_urls"]["spotify"]
    })

@app.route("/addTracksToPlaylist", methods=['POST'])
@auth("spotify")
def addTracksToPlaylist():
    data = request.json
    playlistURI = data["playlistURI"]
    playlistId = playlistURI.split(":")[2]
    trackIds = data["trackIds"]
    sp = spotipy.Spotify(auth=spotifyAuthStartup_.getAccessToken()[0])
    sp.user_playlist_add_tracks(session["userId"], playlistId, trackIds, position=None)
    return "yo"


@app.route("/topsongs")
@auth("spotify")
def topSongs():
    sp = spotipy.Spotify(auth=spotifyAuthStartup_.getAccessToken()[0])
    # short_term, medium_term, long_term
    if not "time_range" in request.args:
        time_range = "short_term"
    else:
        time_range = request.args["time_range"]

    if time_range == "short_term":
        timespan = "the last 30 days"
    elif time_range == "medium_term":
        timespan = "the previous 6 months"
    else:
        timespan = "your spotify life time"

    if not "limit" in request.args:
        limit = 10
    else:
        limit = request.args["limit"]

    results = sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)
    return render_template("topSongs.html", songs=results["items"], timespan=timespan)


@app.route("/")
# @auth("default", "index")
def index():
    global last_origin
    last_origin = "index"
    return render_template("index.html", cssClass="default")


if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # socketio.run(app, host='localhost', port=port)
    app.run(host='0.0.0.0') # , port=5000, debug=True, threaded=False)
