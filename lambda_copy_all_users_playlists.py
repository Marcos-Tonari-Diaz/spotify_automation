import lambda_deploy.copy_script as copy_script
from lambda_deploy.repository import RepositoryFactory


def lambda_handler(event, context):
    # def copy_all_users():
    repo = RepositoryFactory.create_repository()
    for user in repo.get_all_users():
        user_id = user["UserSpotifyId"]
        copier = copy_script.Copier(user_id)
        copier.copy_discoverweekly_to_archive()


# if __name__ == "__main__":
#     copy_all_users()
