import os
import spotify_secrets

APP_PORT = 8080
APP_BASE_ADRESS = "http://localhost"
APP_HOST = "localhost"

SPOTIFY_API_BASE_ADRESS = "https://api.spotify.com/v1"
SPOTIFY_ACCOUNT_BASE_ADDRESS = "https://accounts.spotify.com"
# SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
# SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_CLIENT_ID = spotify_secrets.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = spotify_secrets.SPOTIFY_CLIENT_SECRET
SPOTIFY_ACESS_TOKEN_ADDRESS = "/api/token"
SPOTIFY_MY_PLAYLISTS_ADDRESS = "/me/playlists"
