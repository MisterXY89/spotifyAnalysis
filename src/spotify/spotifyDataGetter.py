
import sys
import spotipy
from libinit import spotifyConfig_
from spotipy.oauth2 import SpotifyClientCredentials

# playlistID_input = str(sys.argv[1])

# print(playlistID_input)
# pl_id = 'spotify:playlist:7wqyxlWLk9WTqnXDNWUnBh'
# pl_id = "spotify:playlist:44Pm5pKc2QNnCi5gK08JDT"
# pl_id = "spotify:playlist:5RJ4O08r96qrRI3tbzGtwb"


# tempo,
# key,
# minor/major,
# danceability,
# valence( positive if higher )
#
class SpotifyData:
    """docstring for SpotifyData."""

    def __init__(self, token):
        self.spotipy = spotipy.Spotify(auth=token)

    def getTracksFromPlaylist(self, playlistID):
        response = self.spotipy.playlist_tracks(playlistID, offset=0, fields='items.track.id,items.track.name, items.track.artists, total')
        return response["items"]

    def getTracksFeatures(self, trackList):
        return self.spotipy.audio_features(trackList)


    def buildTrackList(self, playlistTracksResponse):
        idList = []
        for item in playlistTracksResponse:
            try:
                idList.append(item["track"]["id"])
            except Exception as e:
                continue
        return idList

    def basicOverallValence(self, features):
        # TODO: add median
        return sum([item["valence"] for item in features])/len(features)

    def getBasicValence(self, idList):
        """
        < 0.3 really sad
        > 0.6 happy
        """
        return self.basicOverallValence(self.getTracksFeatures(idList))

    def getBasicPlaylistValence(self, playlistID):
        return self.getBasicValence(self.buildTrackList(self.getTracksFromPlaylist(playlistID)))

    def getTrackName(self, uri):
        return self.getSongInfo["trackName"]

    def getSongInfo(self, uri):
        info = self.spotipy.track(uri)
        return {
            "trackName": info["name"],
            "artistName": info["artists"][0]["name"],
            "albumName": info["album"]["name"],
            "imgUrl": info["album"]["images"][1]["url"]
        }

    def _makePages(self, pls):
        pages = []
        pageLength = 25
        for x in range(0,len(pls)-1, pageLength):
            pages.append({
                "nr": int(x/pageLength)+1,
                "playlists": pls[x:x+pageLength]
                })
        return pages

    def getUserPlaylists(self, user, offset=0, makePages=True):
        playlists = self.spotipy.user_playlists(user, offset=offset)
        allPlaylists = []
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                allPlaylists.append(playlist)
            if playlists['next']:
                playlists = self.spotipy.next(playlists)
            else:
                playlists = None
        if makePages:
            return self._makePages(allPlaylists)
        return allPlaylists

    def getFeatures(self, id):
        features = self.spotipy.audio_features([id])[0]
        return features

    def getUserTracks(self, songCollectionLimit, excludeInstrumentals, type, offset):
        songCollectionCounter = 0
        tracks = self.spotipy.current_user_saved_tracks()
        allTracks = []
        while tracks:
            for i, track in enumerate(tracks['items']):
                if songCollectionCounter >= songCollectionLimit:
                    return allTracks
                features = self.getFeatures(track["track"]["id"])
                if excludeInstrumentals and features["instrumentalness"] < 0.5 or not excludeInstrumentals:
                    if type == "sad":
                        if features["valence"] < 0.5:
                            track["val"] = features["valence"]
                            allTracks.append(track)
                    else:
                        if features["valence"] > 0.5:
                            track["val"] = features["valence"]
                            allTracks.append(track)

                songCollectionCounter += 1
            if tracks['next']:
                tracks = self.spotipy.next(tracks)
            else:
                tracks = None
        return allTracks

    def getPlaylistName(self, uri):
        id = uri.split(":")[2]
        return self.spotipy.playlist(id)["name"]

    def search(self, query):
        return self.spotipy.search(q=query)["tracks"]["items"]
