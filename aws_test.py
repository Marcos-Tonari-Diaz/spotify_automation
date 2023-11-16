import boto3
from botocore.exceptions import ClientError

# # assume a AWS IAM role in AWS STS to get temporary AWS credentials
# iam_resource = boto3.resource("iam")

# iam_resource.get_user("spotify_app_local")

# sts_client = boto3.client(
#     "sts", aws_access_key_id=user_key.id, aws_secret_access_key=user_key.secret)
# try:
#     response = sts_client.assume_role(
#         RoleArn=assume_role_arn, RoleSessionName=session_name)
#     temp_credentials = response["Credentials"]
#     print(f"Assumed role {assume_role_arn} and got temporary credentials.")
# except ClientError as error:
#     print(
#         f"Couldn't assume role {assume_role_arn}. Here's why: "
#         f"{error.response['Error']['Message']}")
#     raise

# gets the test item from the dynamoDB table
# currently using the credentials in ~/.aws/credentials
# need to change to

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Users')

response = table.get_item(
    Key={
        'UserSpotifyId': 'test_id',
    }
)

print(response)
