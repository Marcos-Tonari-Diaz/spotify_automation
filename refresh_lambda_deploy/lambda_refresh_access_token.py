import common
import requests
import base64
from copy_script import Copier
from repository import RepositoryFactory
import logging


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
    logging.info("user flow done. playlist will be update weekly")
    body = '<html><body><h1> Copy Sucess </h1></body></html>'
    return common.make_http_response(body, 200, is_html=True)


def request_access_token(auth_code):
    logging.info("request_acess_token")
    res = make_acess_token_request(auth_code)
    print(res)
    refresh_token = res.json().get("refresh_token")
    if refresh_token == None:
        raise common.BadResponseException(common.make_http_response(
            "refresh_token not in response: "+str(res), 400), res)

    res = common.refresh_access_token(refresh_token)
    access_token = res.json().get("access_token")
    if access_token == None:
        raise common.BadResponseException(common.make_http_response(
            "access_token not in response: "+str(res), 400), res)

    return access_token, refresh_token

# Endpoint


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel("INFO")
    # get the auth code from the spotify auth server
    params = event.get('queryStringParameters')
    if params == None:
        return common.make_http_response("query params not in event: "+str(event), 400)
    auth_code = params.get('code')
    if auth_code == None:
        return common.make_http_response("auth_code not in query string:"+str(params), 400)

    try:
        access_token, refresh_token = request_access_token(auth_code)
        logging.info("start copy")
        return start_copy(access_token, refresh_token)
    except common.BadResponseException as ex:
        return str(ex)
