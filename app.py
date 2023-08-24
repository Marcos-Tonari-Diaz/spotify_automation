import requests
import common
import acess_token
import secrets
import string
from flask import Flask, redirect, request, session, abort, url_for
from urllib import parse
import base64

from common import FileRepository
from copy_script import Copier

app = Flask("spotify_automation")

ALPHABET = string.ascii_letters + string.digits
REDIRECT_URI = "{}:{}/{}".format(common.APP_BASE_ADRESS,
                                 str(common.APP_PORT), 'acess-token')

# Helpers


def make_acess_token_request(auth_code: str):
    req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + common.SPOTIFY_ACESS_TOKEN_ADDRESS
    req_headers = {"content-type": "application/x-www-form-urlencoded",
                   "Authorization": "Basic " + base64.b64encode((common.SPOTIFY_CLIENT_ID + ":" + common.SPOTIFY_CLIENT_SECRET).encode("ascii")).decode('ascii')}

    body_params = {"grant_type": "authorization_code",
                   "code": auth_code,
                   "redirect_uri": REDIRECT_URI}

    response = requests.post(req_url, headers=req_headers, data=body_params)

    return response


# Endpoints

@app.route("/authorize-user")
def request_user_auth():
    # store the request state on the client side to protect against XSRF
    state_secret = ''.join(secrets.choice(ALPHABET) for i in range(16))
    session["state_secret"] = state_secret

    req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + "/authorize"

    req_params = {"client_id": common.SPOTIFY_CLIENT_ID,
                  "response_type": "code",
                  "scope": common.REQUEST_USER_AUTH_SCOPE,
                  "redirect_uri": REDIRECT_URI,
                  "state": state_secret}

    req_url_with_params = req_url + "?" + parse.urlencode(req_params)
    return redirect(req_url_with_params)


@app.route("/acess-token")
def request_access_token():
    # get the auth code from the spotify auth server
    state = request.args.get("state")
    auth_code = request.args.get("code")
    error = request.args.get("error")

    if (state != session["state_secret"]):
        abort(401)

    if (error != None):
        return error

    res = make_acess_token_request(auth_code)
    token_repo = FileRepository.instance("refresh_token.txt", "token")
    token_repo.write_object_to_file(
        res.json()["refresh_token"])
    copier = Copier()
    copier.copy_discoverweekly_to_archive()
    return "<p>Completed.</p>"


if __name__ == "__main__":
    # secret to use sessions
    app.secret_key = secrets.token_hex().encode()
    app.run(debug=True, port=common.APP_PORT, host=common.APP_HOST)
