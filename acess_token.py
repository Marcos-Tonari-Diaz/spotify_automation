import requests
import common
import os


# def get_access_token():
#     req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + "/api/token"
#     req_headers = {'content-type': 'application/x-www-form-urlencoded'}
#     req_params = {"grant_type": "client_credentials",
#                   "client_id": os.environ['SPOTIFY_CLIENT_ID'], "client_secret": os.environ['SPOTIFY_CLIENT_SECRET']}

#     response = requests.post(req_url, headers=req_headers, params=req_params)

#     return response.json()["access_token"]


# print(get_access_token())
