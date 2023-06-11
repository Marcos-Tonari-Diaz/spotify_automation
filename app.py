import requests
import common
import acess_token
import secrets
import string
from flask import Flask, redirect
from urllib import parse

app = Flask("spotify_automation")

@app.route("/login")
def request_user_auth():
    alphabet = string.ascii_letters + string.digits
    SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"
    redirect_uri = "{}:{}/{}".format(common.APP_BASE_ADRESS,str(common.APP_PORT),'callback')

    req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + "/authorize"
    req_params = {"client_id": common.SPOTIFY_CLIENT_ID,
                  "response_type": "code",
                  "scope": SCOPE,
                  "redirect_uri": redirect_uri,
                  "state": ''.join(secrets.choice(alphabet) for i in range(16))}

    return redirect(req_url + "?" + parse.urlencode(req_params))

@app.route("/callback")
def request_access_token():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True, port=common.APP_PORT, host="localhost")

# get my user id
# this doesnt work, we first need to use the oauth authotization flow so my user grants my app authorization
# then my app gets another token


# def get_user_id():
#     req_url = common.API_BASE_ADRESS+"/me"
#     req_headers = {'Authorization': 'Bearer ' + acess_token.get_access_token()}
#     return requests.get(common.API_BASE_ADRESS+"/me", headers=req_headers).json()


#print(get_user_id())
