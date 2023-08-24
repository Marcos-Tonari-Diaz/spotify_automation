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
REQUEST_USER_AUTH_SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"


def SPOTIFY_USER_PLAYLISTS_ADDRESS(
    user_id): return SPOTIFY_API_BASE_ADRESS + SPOTIFY_USERS_ADDRESS + "/" + user_id + SPOTIFY_PLAYLISTS_ADDRESS


def SPOTIFY_PLAYLISTS_TRACKS_ADDRESS(
    playlist_id): return SPOTIFY_API_BASE_ADRESS + SPOTIFY_PLAYLISTS_ADDRESS + "/" + playlist_id + "/tracks"


class FileRepository:
    _instance = None

    @classmethod
    def instance(cls, file_name, stored_object_name):
        if cls._instance == None:
            cls._instance = FileRepository(file_name, stored_object_name)
        return cls._instance

    def __init__(self, file_name, stored_object_name):
        self.access_token_file = file_name
        self.stored_object_name = stored_object_name
        if os.path.isfile(self.access_token_file):
            self.refresh_token = self.get_object_from_file()
        else:
            file = open(self.access_token_file, "w")
            file.close()

    def get_object_from_file(self):
        with open(self.access_token_file, 'r') as file:
            token = json.load(file)
        return token[self.stored_object_name]

    def get_object(self):
        return self.refresh_token

    def write_object_to_file(self, token):
        with open(self.access_token_file, 'w') as file:
            json.dump({self.stored_object_name: token}, file)
