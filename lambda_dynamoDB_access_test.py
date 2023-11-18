import json
import logging
import boto3


def lambda_handler(event, context):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(f"CloudWatch logs group: {context.log_group_name}")

    # gets the test item from the dynamoDB table

    # local: uses the credentials in ~/.aws/credentials

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Users')

    response = table.get_item(
        Key={
            'UserSpotifyId': 'test_id',
        }
    )

    return json.dumps(response)
