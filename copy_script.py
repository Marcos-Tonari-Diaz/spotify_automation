
import common
import requests
import base64
from common import FileTokenRepository


class Copier:

    def __init__(self):
        self.token_repo = FileTokenRepository()
        self.access_token = self.refresh_acess_token()

    def refresh_acess_token(self):
        req_url = common.SPOTIFY_ACCOUNT_BASE_ADDRESS + common.SPOTIFY_ACESS_TOKEN_ADDRESS
        req_headers = {"content-type": "application/x-www-form-urlencoded",
                       "Authorization": "Basic " + base64.b64encode((common.SPOTIFY_CLIENT_ID + ":" + common.SPOTIFY_CLIENT_SECRET).encode("ascii")).decode('ascii')}

        body_params = {"grant_type": "refresh_token",
                       "refresh_token": self.token_repo.get_refresh_token()}

        response = requests.post(
            req_url, headers=req_headers, data=body_params)

        return response.json()["access_token"]

    def get_discoverweekly_tracks(self):
        playlistid, tracks_url = self.search_playlist_by_name(
            "discover+weekly")
        return self.get_discoverweekly_track_uris(tracks_url)

    def get_current_user_spotifyid(self):
        req_url = common.SPOTIFY_API_BASE_ADRESS + \
            common.SPOTIFY_CURRENT_USER_ADDRESS
        req_headers = {"Authorization": "Bearer " +
                       self.access_token}
        res = requests.get(req_url, headers=req_headers)
        return res.json()["id"]

    def get_playlists(self):
        req_url = common.SPOTIFY_API_BASE_ADRESS + \
            common.SPOTIFY_MY_PLAYLISTS_ADDRESS
        req_headers = {"Authorization": "Bearer " +
                       self.access_token}
        res = requests.get(req_url, headers=req_headers)
        return res.json()

    def search_playlist_by_name(self, name):
        req_url = common.SPOTIFY_API_BASE_ADRESS + \
            common.SPOTIFY_SEARCH_ADDRESS
        req_headers = {"Authorization": "Bearer " +
                       self.access_token}
        req_params = {"q": name,
                      "type": "playlist"}
        res = requests.get(req_url, headers=req_headers, params=req_params)
        discoverweekly_playlist = res.json()["playlists"]["items"][0]
        playlistid = discoverweekly_playlist["id"]
        tracks_link = discoverweekly_playlist["tracks"]["href"]
        return (playlistid, tracks_link)

    def get_discoverweekly_track_uris(self, tracks_url):
        req_headers = {"Authorization": "Bearer " +
                       self.access_token}
        res = requests.get(
            tracks_url, headers=req_headers)
        tracks = res.json()["items"]
        track_uris = [track["track"]["uri"] for track in tracks]
        return track_uris

    def create_test_archive_playlist(self, playlist_name, spotify_id):
        req_url = common.SPOTIFY_USER_PLAYLISTS_ADDRESS(spotify_id)
        req_headers = {"Authorization": "Bearer " +
                       self.access_token}
        req_body = {"name": playlist_name, "description": "test"}
        res = requests.post(req_url, headers=req_headers, json=req_body)
        return res.json()["id"]

    def make_copy_tracks_request(self, track_uris, target_playlist):
        req_url = common.SPOTIFY_PLAYLISTS_TRACKS_ADDRESS(target_playlist)
        req_headers = {"Authorization": "Bearer " +
                       self.access_token}
        req_body = {"uris": track_uris}
        res = requests.post(req_url, headers=req_headers, json=req_body)
        return res

    def copy_discoverweekly_to_archive(self):
        spotify_id = self.get_current_user_spotifyid()
        archive_playlist_id, _ = self.search_playlist_by_name("archive")
        if (archive_playlist_id == None):
            archive_playlist_id = self.create_test_archive_playlist(
                "archive", spotify_id)
        track_uris = self.get_discoverweekly_tracks()
        self.make_copy_tracks_request(track_uris, archive_playlist_id)


if __name__ == "__main__":
    copier = Copier()
    copier.copy_discoverweekly_to_archive()
