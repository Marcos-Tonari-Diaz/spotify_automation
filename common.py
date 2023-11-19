import os
import requests
import base64

APP_PORT = 8080
APP_BASE_ADRESS = "http://localhost"
APP_HOST = "localhost"

SPOTIFY_API_BASE_ADRESS = "https://api.spotify.com/v1"
SPOTIFY_ACCOUNT_BASE_ADDRESS = "https://accounts.spotify.com"
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_CURRENT_USER_ADDRESS = "/me"
SPOTIFY_USERS_ADDRESS = "/users"
SPOTIFY_ACESS_TOKEN_ADDRESS = "/api/token"
SPOTIFY_PLAYLISTS_ADDRESS = "/playlists"
SPOTIFY_MY_PLAYLISTS_ADDRESS = SPOTIFY_CURRENT_USER_ADDRESS + SPOTIFY_PLAYLISTS_ADDRESS
SPOTIFY_SEARCH_ADDRESS = "/search"
REQUEST_USER_AUTH_SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"

ENVIRONMENT_ENV_VARIABLE = "ENVIRONMENT"
LOCAL_ENVIRONMENT = "LOCAL"
DEPLOY_ENVIRONMENT = "DEPLOY"
ENVIRONMENT = os.environ[ENVIRONMENT_ENV_VARIABLE]

SPOTIFY_REFRESH_TOKEN_DB_KEY = "SpotifyAPIRefreshToken"
ARCHIVE_PLAYLIST_ID_DB_KEY = "ArchivePlaylistId"
SPOTIFY_USER_ID_DB_KEY = "UserSpotifyId"


def SPOTIFY_USER_PLAYLISTS_ADDRESS(
    user_id): return SPOTIFY_API_BASE_ADRESS + SPOTIFY_USERS_ADDRESS + "/" + user_id + SPOTIFY_PLAYLISTS_ADDRESS


def SPOTIFY_USER_PLAYLIST_ADDRESS(
    user_id, playlist_id): return SPOTIFY_API_BASE_ADRESS + SPOTIFY_USERS_ADDRESS + "/" + user_id + SPOTIFY_PLAYLISTS_ADDRESS + "/" + playlist_id


def SPOTIFY_PLAYLISTS_TRACKS_ADDRESS(
    playlist_id): return SPOTIFY_API_BASE_ADRESS + SPOTIFY_PLAYLISTS_ADDRESS + "/" + playlist_id + "/tracks"


def get_currentuser_spotifyid_displayname(access_token):
    req_url = SPOTIFY_API_BASE_ADRESS + \
        SPOTIFY_CURRENT_USER_ADDRESS
    req_headers = {"Authorization": "Bearer " +
                   access_token}
    res = requests.get(req_url, headers=req_headers)
    return res.json()["id"], res.json()["display_name"]


def refresh_access_token(refresh_token):
    req_url = SPOTIFY_ACCOUNT_BASE_ADDRESS + SPOTIFY_ACESS_TOKEN_ADDRESS
    req_headers = {"content-type": "application/x-www-form-urlencoded",
                   "Authorization": "Basic " + base64.b64encode((SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET).encode("ascii")).decode('ascii')}

    body_params = {"grant_type": "refresh_token",
                   "refresh_token": refresh_token}

    response = requests.post(
        req_url, headers=req_headers, data=body_params)

    return response.json()["access_token"]
