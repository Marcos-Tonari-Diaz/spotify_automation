
import requests
import os

import common
from repository import RepositoryFactory


class Copier:
    def __init__(self, user_id, archive_playlist_name=None):
        self.user_id = user_id
        self.archive_playlist_name = archive_playlist_name
        self.repo = RepositoryFactory.create_repository()
        self.user_data = self.repo.get_user(user_id)
        self.access_token = common.refresh_access_token(
            self.user_data[common.SPOTIFY_REFRESH_TOKEN_DB_KEY])

    def create_auth_header(self):
        return {"Authorization": "Bearer " +
                self.access_token}

    def get_discoverweekly_tracks(self):
        playlistid, tracks_url = self.search_playlist_by_name(
            "discover+weekly")
        return self.get_discoverweekly_track_uris(tracks_url)

    def get_playlists(self):
        req_url = common.SPOTIFY_API_BASE_ADRESS + \
            common.SPOTIFY_MY_PLAYLISTS_ADDRESS
        req_headers = self.create_auth_header()
        res = requests.get(req_url, headers=req_headers)
        return res.json()

    def search_playlist_by_name(self, name):
        req_url = common.SPOTIFY_API_BASE_ADRESS + \
            common.SPOTIFY_SEARCH_ADDRESS
        req_headers = self.create_auth_header()
        req_params = {"q": name,
                      "type": "playlist"}
        res = requests.get(req_url, headers=req_headers, params=req_params)
        discoverweekly_playlist = res.json()["playlists"]["items"][0]
        playlistid = discoverweekly_playlist["id"]
        tracks_link = discoverweekly_playlist["tracks"]["href"]
        return (playlistid, tracks_link)

    def get_discoverweekly_track_uris(self, tracks_url):
        req_headers = self.create_auth_header()
        res = requests.get(
            tracks_url, headers=req_headers)
        tracks = res.json()["items"]
        track_uris = [track["track"]["uri"] for track in tracks]
        return track_uris

    def create_archive_playlist(self, playlist_name, spotify_id):
        req_url = common.SPOTIFY_USER_PLAYLISTS_ADDRESS(spotify_id)
        req_headers = self.create_auth_header()
        req_body = {"name": playlist_name, "description": "test"}
        res = requests.post(req_url, headers=req_headers, json=req_body)
        return res.json()["id"]

    def make_copy_tracks_request(self, track_uris, target_playlist):
        req_url = common.SPOTIFY_PLAYLISTS_TRACKS_ADDRESS(target_playlist)
        req_headers = self.create_auth_header()
        req_body = {"uris": track_uris}
        res = requests.post(req_url, headers=req_headers, json=req_body)
        return res

    def copy_discoverweekly_to_archive(self):
        archive_playlist_id = self.user_data[common.ARCHIVE_PLAYLIST_ID_DB_KEY]
        if (archive_playlist_id == None):
            archive_playlist_id = self.create_archive_playlist(
                self.archive_playlist_name, user_id)
            self.repo.set_archive_playlist_id(archive_playlist_id)
        track_uris = self.get_discoverweekly_tracks()
        self.make_copy_tracks_request(track_uris, archive_playlist_id)


if __name__ == "__main__":
    user_id = "user"
    copier = Copier(user_id)
    copier.copy_discoverweekly_to_archive()
