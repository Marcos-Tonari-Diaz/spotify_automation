import requests
import common
import acess_token
import secrets
import string
from flask import Flask, redirect, request, session, abort, url_for
from urllib import parse
import base64

app = Flask("spotify_automation")

ALPHABET = string.ascii_letters + string.digits
REDIRECT_URI = "{}:{}/{}".format(common.APP_BASE_ADRESS,
                                 str(common.APP_PORT), 'callback')


def make_acess_token_request(auth_code: str):
    req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + common.SPOTIFY_ACESS_TOKEN_ADDRESS
    req_headers = {"content-type": "application/x-www-form-urlencoded",
                   "Authorization": "Basic " + base64.b64encode((common.SPOTIFY_CLIENT_ID + ":" + common.SPOTIFY_CLIENT_SECRET).encode("ascii")).decode('ascii')}

    body_params = {"grant_type": "authorization_code",
                   "code": auth_code,
                   "redirect_uri": REDIRECT_URI}

    response = requests.post(req_url, headers=req_headers, data=body_params)

    return response


@app.route("/login")
def request_user_auth():
    SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"

    # store the request state on the client side to protect against XSRF
    state_secret = ''.join(secrets.choice(ALPHABET) for i in range(16))
    session["state_secret"] = state_secret

    req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + "/authorize"

    req_params = {"client_id": common.SPOTIFY_CLIENT_ID,
                  "response_type": "code",
                  "scope": SCOPE,
                  "redirect_uri": REDIRECT_URI,
                  "state": state_secret}

    req_url_with_params = req_url + "?" + parse.urlencode(req_params)
    return redirect(req_url_with_params)


@app.route("/callback")
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
    session["access_token"] = res.json()["access_token"]
    # return res.json()
    return redirect(url_for('get_playlists'))


@app.route("/playlists")
def get_playlists():
    req_url = common.SPOTIFY_API_BASE_ADRESS + \
        common.SPOTIFY_MY_PLAYLISTS_ADDRESS
    req_headers = {"Authorization": "Bearer " + session["access_token"]}
    res = requests.get(req_url, headers=req_headers)
    return res.json()


if __name__ == "__main__":
    # secret to use sessions
    app.secret_key = secrets.token_hex().encode()
    app.run(debug=True, port=common.APP_PORT, host=common.APP_HOST)
