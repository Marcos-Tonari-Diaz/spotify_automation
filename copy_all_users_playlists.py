import copy_script
from repository import RepositoryFactory


def lambda_handler(event, context):
    repo = RepositoryFactory.create_repository()
    for user in repo.get_all_users():
        user_id = user["UserSpotifyId"]
        copier = copy_script.Copier(user_id)
        copier.copy_discoverweekly_to_archive()
