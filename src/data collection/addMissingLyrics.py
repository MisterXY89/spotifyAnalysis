
import re
import urllib.request
from getLyrics import *
from bs4 import BeautifulSoup

ly = Lyrics()

baseUrl = "https://www.metrolyrics.com/"
# https://www.metrolyrics.com/ill-never-fall-in-love-again-lyrics-tom-jones.html

errors = {'1989':
[{'position': '8', 'artist': 'Milli Vanilli', 'track': 'Girl You Know Its True'}, {'position': '9', 'artist': 'Will To Power', 'track': 'Baby, I Love Your Way-Freebird'}, {'position': '15', 'artist': 'Warrant', 'track': 'Heavan'}, {'position': '24', 'artist': 'Simply Red', 'track': 'If You Don’t Know Be By Now'}, {'position': '26', 'artist': 'New Kids On The Block', 'track': 'I’ll Be Loving You (Forever)'}, {'position': '29', 'artist': 'Martika', 'track': 'Toy Solider'}, {'position': '30', 'artist': 'Paula Abdul', 'track': 'Forever Your Girl.'}, {'position': '47', 'artist': 'B-52’s', 'track': 'Love Shack'}, {'position': '63', 'artist': '.38 Special', 'track': 'Second Chances'}, {'position': '69', 'artist': 'Karyn White', 'track': 'Secret Rendesvous'}, {'position': '74', 'artist': 'Guns N’ Roses', 'track': 'Welcom To The Jungle'}, {'position': '83', 'artist': 'When In Rome', 'track': 'This Promise'}, {'position': '87', 'artist': 'Samantha Fox', 'track': 'Iwanna Have Some Fun'}, {'position': '94', 'artist': 'Deon Estus', 'track': 'Heavan Help Me'}, {'position': '98', 'artist': 'Ann Wilson and Robin Zander', 'track': 'Surrender To Me'}, {'position': '100', 'artist': 'Soul II Soul', 'track': 'Keep On Movin'}]}



def prep(txt):
    txt = "".join([char.lower() for char in list(txt) if char.isalpha() or char == " "])
    txt = re.sub("\s", "-", txt)
    return txt

def buildMetroUrl(el):
    return baseUrl + prep(el["track"]) + "-lyrics-" + prep(el["artist"]) + ".html"



def get_lyrics(artist, song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"

    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip()
        return lyrics
    except Exception as e:
        return "Exception occurred \n" +str(e)


# u = buildMetroUrl(errors["1969"][1])

# from musixmatch import Musixmatch

API_KEY = "ca69927cc4132fed9cef4b969f60c67e"
# musixmatch = Musixmatch(API_KEY)

def altGetLyricsFromError(year):
    year = str(year)
    elt = errors[year]
    for x in range(0, len(elt)):
        # res = musixmatch.track_search(q_artist=elt[x]["artist"], q_track=elt[x]["track"], page_size=10, page=1, s_track_rating='desc')
        # # res = json.load(res)
        # res = res["message"]["body"]["track_list"]
        # if len(res) > 0:
        #     res = res[0]["track"]
        #     if (res["has_lyrics"] == 1):
        #         # print(res)
        #         # track_id = res["track_id"]
        #         # l = musixmatch.track_lyrics_get(track_id)
        #         print(res["track_edit_url"])
        #     else:
        #         print("> has no lyrics")
        # else:
        #     print("Not found")
        l = get_lyrics(elt[x]["artist"], elt[x]["track"])
        l = re.sub("<br/>", ";", l)
        l = re.sub('\s+', ' ', l)
        # ly.addLyrics(year, elt[x]["position"], l)
        print(l)
        print(30*"--")


altGetLyricsFromError(1989)
input()


# musixmatch.track_search(q_artist=, q_track="", page_size=10, page=1, s_track_rating='desc')
# musixmatch.track_lyrics_get(15953433)
