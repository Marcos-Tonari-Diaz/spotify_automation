import common
from urllib import parse
import json


# Helpers


def redirect_response(redirect_url):
    response = dict()
    response["statusCode"] = 302
    response["body"] = json.dumps(dict())  # empty
    response["headers"] = {"Location": redirect_url}
    return response


def request_user_auth():
    state_secret = 'dummy_state'

    req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + "/authorize"

    req_params = {"client_id": common.SPOTIFY_CLIENT_ID,
                  "response_type": "code",
                  "scope": common.REQUEST_USER_AUTH_SCOPE,
                  "redirect_uri": common.REDIRECT_URI,
                  "state": state_secret}

    req_url_with_params = req_url + "?" + parse.urlencode(req_params)
    return redirect_response(req_url_with_params)

# Endpoint


def lambda_handler(event, context):
    return request_user_auth()
