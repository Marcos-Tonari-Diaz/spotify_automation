import os
import spotify_secrets
import json

APP_PORT = 8080
APP_BASE_ADRESS = "http://localhost"
APP_HOST = "localhost"

SPOTIFY_API_BASE_ADRESS = "https://api.spotify.com/v1"
SPOTIFY_ACCOUNT_BASE_ADDRESS = "https://accounts.spotify.com"
# SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
# SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_CURRENT_USER_ADDRESS = "/me"
SPOTIFY_USERS_ADDRESS = "/users"
SPOTIFY_CLIENT_ID = spotify_secrets.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = spotify_secrets.SPOTIFY_CLIENT_SECRET
SPOTIFY_ACESS_TOKEN_ADDRESS = "/api/token"
SPOTIFY_PLAYLISTS_ADDRESS = "/playlists"
SPOTIFY_MY_PLAYLISTS_ADDRESS = SPOTIFY_CURRENT_USER_ADDRESS + SPOTIFY_PLAYLISTS_ADDRESS
SPOTIFY_SEARCH_ADDRESS = "/search"


def SPOTIFY_USER_PLAYLISTS_ADDRESS(
    user_id): return SPOTIFY_API_BASE_ADRESS + SPOTIFY_USERS_ADDRESS + "/" + user_id + SPOTIFY_PLAYLISTS_ADDRESS


def SPOTIFY_PLAYLISTS_TRACKS_ADDRESS(
    playlist_id): return SPOTIFY_API_BASE_ADRESS + SPOTIFY_PLAYLISTS_ADDRESS + "/" + playlist_id + "/tracks"


class FileTokenRepository:
    def __init__(self):
        self.access_token_file = 'refresh_token.txt'
        self.refresh_token = self.read_refresh_token_from_file()

    def read_refresh_token_from_file(self):
        with open(self.access_token_file, 'r') as file:
            token = json.load(file)
        return token["token"]

    def get_refresh_token(self):
        return self.refresh_token

    def write_refresh_token_to_file(self, token):
        with open(self.access_token_file, 'x') as file:
            json.dump({"token": token}, file)
