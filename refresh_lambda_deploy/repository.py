import os
import json
import boto3
import common
import logging


class RepositoryFactory:
    @classmethod
    def create_repository(cls):
        environment = common.ENVIRONMENT
        if environment == common.LOCAL_ENVIRONMENT:
            return FileRepository.instance("Users")
        if environment == common.DEPLOY_ENVIRONMENT:
            return DynamoDBRepository.instance()


class DynamoDBRepository:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = DynamoDBRepository()
        return cls._instance

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
            try:
                user_data = response["Item"]
                return {common.SPOTIFY_REFRESH_TOKEN_DB_KEY: user_data[common.SPOTIFY_REFRESH_TOKEN_DB_KEY],
                        common.ARCHIVE_PLAYLIST_ID_DB_KEY: user_data[common.ARCHIVE_PLAYLIST_ID_DB_KEY]}
            except KeyError:
                return None
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

    def get_all_users(self):
        response = self.table.scan(TableName='Users',)
        return response["Items"]

    def set_archive_playlist_id(self, user_id, user_playlist_id):
        response = self.table.update_item(
            Key={
                'UserSpotifyId': user_id,
            },
            UpdateExpression='SET {} = :id'.format(
                common.ARCHIVE_PLAYLIST_ID_DB_KEY),
            ExpressionAttributeValues={
                ':id': user_playlist_id
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

    def read_json_from_file(self, file_name):
        with open(file_name, 'r') as file:
            try:
                return json.loads(file.read())
            except json.decoder.JSONDecodeError:  # empty file
                return None

    def get_user(self, user_id):
        if self.data == None:
            self.data = self.read_json_from_file(self.db_file)
        if self.data != None:
            return self.data[user_id]

    def write_user(self, user_id, user_token, user_playlist_id):
        data = self.read_json_from_file(self.db_file)
        # user already persisted - delete the contents before writing again
        if data != None:
            open(self.db_file, 'w').close()
        user_data = {common.SPOTIFY_REFRESH_TOKEN_DB_KEY: user_token,
                     common.ARCHIVE_PLAYLIST_ID_DB_KEY: user_playlist_id}
        if self.data == None:
            self.data = {user_id: user_data}
        else:
            self.data[user_id] = user_data
        with open(self.db_file, 'w') as file:
            json.dump(self.data, file)

    def set_archive_playlist_id(self, user_id, user_playlist_id):
        data = self.read_json_from_file(self.db_file)
        self.write_user(
            user_id, data[common.SPOTIFY_REFRESH_TOKEN_DB_KEY], user_playlist_id)
