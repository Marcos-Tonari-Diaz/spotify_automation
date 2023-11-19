import copy_script
from repository import RepositoryFactory


def copy_all_users_playlists():
    repo = RepositoryFactory.create_repository()
    for user in repo.get_all_users():
        user_id = user["UserSpotifyId"]
        copier = copy_script.Copier(user_id)
        copier.copy_discoverweekly_to_archive()


if __name__ == "__main__":
    copy_all_users_playlists()
