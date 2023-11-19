import os
import json
import boto3
import common
import logging


class RepositoryFactory:
    @classmethod
    def create_repository(cls):
        if cls.environment == None:
            cls.environment = os.environ[common.ENVIRONMENT_ENV_VARIABLE]
        if cls.environment == common.LOCAL_ENVIRONMENT:
            return FileRepository.instance("Users")
        if cls.environment == common.DEPLOY_ENVIRONMENT:
            return DynamoDBRepository()


class DynamoDBRepository:

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.ERROR)

        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('Users')

    def get_user(self, user_id):
        response = self.table.get_item(
            Key={
                'UserSpotifyId': user_id,
            }
        )
        status = response["ResponseMetadata"]["HTTPStatusCode"]
        if status == 200:
            user_data = response["Item"]
            return {common.SPOTIFY_REFRESH_TOKEN_DB_KEY: user_data[common.SPOTIFY_REFRESH_TOKEN_DB_KEY],
                    common.ARCHIVE_PLAYLIST_ID_DB_KEY: user_data[common.ARCHIVE_PLAYLIST_ID_DB_KEY]}
        else:
            self.logger.info(f"Failed to read user. Response: {response}")
            return None

    def write_user(self, user_id, user_token, user_playlist_id):
        response = self.table.put_item(
            Item={
                common.SPOTIFY_USER_ID_DB_KEY: user_id,
                common.SPOTIFY_REFRESH_TOKEN_DB_KEY: user_token,
                common.ARCHIVE_PLAYLIST_ID_DB_KEY: user_playlist_id,
            }
        )
        # status = response["ResponseMetadata"]["HTTPStatusCode"]
        self.logger.info(f"Response: {response}")


# Collection of singleton file repositories
class FileRepository:
    _instances = {}

    @classmethod
    def instance(cls, instace_name):
        if instace_name not in cls._instances:
            cls._instances[instace_name] = FileRepository(
                instace_name)
        return cls._instances[instace_name]

    def __init__(self, instance_name):
        self.db_file = instance_name
        if os.path.isfile(self.db_file):
            # in-memory caching
            self.data = self.read_json_from_file(self.db_file)
        else:
            file = open(self.db_file, "w")
            file.close()
            self.data = None

    def __str__(self) -> str:
        return str(self.data)

    def get_user(self, user_id):
        if self.data == None:
            self.data = self.read_json_from_file(self.db_file)
        if self.data != None:
            return self.data[user_id]

    def write_user(self, user_id, user_token, user_playlist_id):
        user_data = {common.SPOTIFY_REFRESH_TOKEN_DB_KEY: user_token,
                     common.ARCHIVE_PLAYLIST_ID_DB_KEY: user_playlist_id}
        if self.data == None:
            self.data = {user_id: user_data}
        else:
            self.data[user_id] = user_data
        with open(self.db_file, 'w') as file:
            json.dump(self.data, file)

    def read_json_from_file(self, file_name):
        with open(file_name, 'r') as file:
            try:
                return json.loads(file.read())
            except json.decoder.JSONDecodeError:  # empty file
                return None
