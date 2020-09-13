
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class SpotifyConfig:
    def __init__(self):
        self.CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.FLASK_SECRET = os.getenv("FLASK_SECRET")
