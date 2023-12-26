import common
import requests
import base64
from copy_script import Copier
from repository import RepositoryFactory


# Helpers


def make_acess_token_request(auth_code: str):
    req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + common.SPOTIFY_ACESS_TOKEN_ADDRESS
    req_headers = {"content-type": "application/x-www-form-urlencoded",
                   "Authorization": "Basic " + base64.b64encode((common.SPOTIFY_CLIENT_ID + ":" + common.SPOTIFY_CLIENT_SECRET).encode("ascii")).decode('ascii')}

    body_params = {"grant_type": "authorization_code",
                   "code": auth_code,
                   "redirect_uri": common.REDIRECT_URI}

    response = requests.post(req_url, headers=req_headers, data=body_params)

    return response


def start_copy(access_token, refresh_token):
    user_id, display_name = common.get_currentuser_spotifyid_displayname(
        access_token)

    repo = RepositoryFactory.create_repository()
    user = repo.get_user(user_id)
    if user == None:
        repo.write_user(user_id, refresh_token, None)

    copier = Copier(user_id, display_name + "_archive_playlist")
    copier.copy_discoverweekly_to_archive()


def request_access_token(auth_code, error):
    if (error != None):
        return error

    res = make_acess_token_request(auth_code)
    refresh_token = res.json()["refresh_token"]

    access_token = common.refresh_access_token(refresh_token)
    return access_token, refresh_token

# Endpoint


def lambda_handler(event, context):
    # get the auth code from the spotify auth server
    auth_code = event.code
    error = event.error
    access_token, refresh_token = request_access_token(auth_code, error)
    return start_copy(access_token, refresh_token)
