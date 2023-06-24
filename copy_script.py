
import common
import requests
import base64

# this


class TokenRepository:
    def __init__(self):
        self.access_token_file = 'refresh_token.txt'
        self.refresh_token = self.read_refresh_token_from_file()

    def read_refresh_token_from_file(self):
        file = open(self.access_token_file, 'r')
        self.refresh_token = file.readline()
        file.close()

    def get_access_token(self):
        return self.refresh_token


def make_refresh_acess_token_request(refresh_token: str):
    req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + common.SPOTIFY_ACESS_TOKEN_ADDRESS
    req_headers = {"content-type": "application/x-www-form-urlencoded",
                   "Authorization": "Basic " + base64.b64encode((common.SPOTIFY_CLIENT_ID + ":" + common.SPOTIFY_CLIENT_SECRET).encode("ascii")).decode('ascii')}

    body_params = {"grant_type": "authorization_code",
                   "refresh_token": refresh_token}

    response = requests.post(req_url, headers=req_headers, data=body_params)

    return response


def refresh_access_token():

    res = make_refresh_acess_token_request(refresh_token)
    # access_token = res.json()["access_token"]
    return res.json()["access_token"]


def get_discoverweekly_tracks():
    playlistid, tracks_url = search_playlist_by_name("discover+weekly")
    return get_discoverweekly_track_uris(tracks_url)


def get_current_user_spotifyid_request(access_token):
    req_url = common.SPOTIFY_API_BASE_ADRESS + \
        common.SPOTIFY_CURRENT_USER_ADDRESS
    req_headers = {"Authorization": "Bearer " + access_token}
    res = requests.get(req_url, headers=req_headers)
    return res.json()["id"]


def get_playlists(access_token):
    req_url = common.SPOTIFY_API_BASE_ADRESS + \
        common.SPOTIFY_MY_PLAYLISTS_ADDRESS
    req_headers = {"Authorization": "Bearer " + access_token}
    res = requests.get(req_url, headers=req_headers)
    return res.json()


def search_playlist_by_name(access_token, name):
    req_url = common.SPOTIFY_API_BASE_ADRESS + \
        common.SPOTIFY_SEARCH_ADDRESS
    req_headers = {"Authorization": "Bearer " + access_token}
    req_params = {"q": name,
                  "type": "playlist"}
    res = requests.get(req_url, headers=req_headers, params=req_params)
    discoverweekly_playlist = res.json()["playlists"]["items"][0]
    playlistid = discoverweekly_playlist["id"]
    tracks_link = discoverweekly_playlist["tracks"]["href"]
    # session["discoverweekly_id"] = playlistid
    # session["discoverweekly_tracks_url"] = tracks_link
    return (playlistid, tracks_link)
    # return redirect(url_for('get_discoverweekly_tracks'))


def get_discoverweekly_track_uris(access_token, tracks_url):
    req_headers = {"Authorization": "Bearer " + access_token}
    # res = requests.get(
    #     session["discoverweekly_tracks_url"], headers=req_headers)
    res = requests.get(
        tracks_url, headers=req_headers)
    tracks = res.json()["items"]
    track_uris = [track["track"]["uri"] for track in tracks]
    return track_uris
    # return res.json()


def create_test_archive_playlist(access_token, playlist_name):
    req_url = common.SPOTIFY_USER_PLAYLISTS_ADDRESS(session["spotifyid"])
    req_headers = {"Authorization": "Bearer " + access_token}
    req_body = {"name": playlist_name, "description": "test"}
    res = requests.post(req_url, headers=req_headers, json=req_body)
    return res.json()["id"]


def make_copy_tracks_request(access_token, track_uris, target_playlist):
    req_url = common.SPOTIFY_PLAYLISTS_TRACKS_ADDRESS(target_playlist)
    req_headers = {"Authorization": "Bearer " + acess_token}
    req_body = {"uris": track_uris}
    res = requests.post(req_url, headers=req_headers, json=req_body)


def copy_discoverweekly_to_archive():
    acess_token = refresh_access_token()
    get_current_user_spotifyid()
    archive_playlist_id = create_test_archive_playlist("test_archive2")
    # archive_playlist_id, _ = search_playlist_by_name("test+archive1")
    # if (archive_playlist_id != None):
    #     abort(400)
    track_uris = get_discoverweekly_tracks()
    return make_copy_tracks_request(track_uris, archive_playlist_id)


if __name__ == "__main__":
    token_repo = TokenRepository()
    copy_discoverweekly_to_archive()
