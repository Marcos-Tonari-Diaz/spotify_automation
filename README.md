# spotify_automation
Web app to save Discover weekly playlist songs in a single archive playlist.

#### Key Decisions
- Used Flask as the web framework: very simple user authorization flow and data access, no need for a more complete framework. After this initial flow all the work is scheduled, not on demand.
- Not using spotipy: I wanted to code the authorization flow by myself for my own education
- Cloud architecture:
    - Use AWS Lambda to :
        - listen to requests for the first access. A simple backend function can trigger the Sopitfy authorization flow and save the new user's refresh token.
        - run the copying script. After the initial authorization flow, all the backend needs to do is call the Spotify API to copy new songs to the archive.
    - Use CloudWatch to trigger the Lambda function weekly.
    - Use DynamoDB as the refresh token store: AWS Secrets Manager would be the best way to store user tokens, but it doesn't have a free tier. Dynamo DB has an encryption API, so we can encrypt at rest and in transit.

#### How to deploy
- AWS Permissions setup
    - Create an AWS account. This project only uses the Free Tier.
    - Create an IAM organization and an IAM administrative user.
    - Create an IAM user (spotify_app).
    - Create a DynamoDB table called "Users"
    - Create a IAM policy with permission to read and write from the DynamoDB table. Assign this policy to the IAM user.
      ```
      "Statement": {
        "Effect": "Allow",
        "Action": [
            "dynamodb:BatchGetItem",
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:BatchWriteItem",
            "dynamodb:PutItem",
            "dynamodb:UpdateItem"
        ],
        "Resource": "arn:aws:dynamodb:[your aws region]:[your_aws_account_id]:table/Users"
        ```
    - Use the IAM user credentials to authorize the requests

- AWS Lambda Setup
      - create Lambda function
      - assign the IAM policy created above to it
      - change Handler to copy_all_users_playlists.lambda_handler
      - change timeout to something lik 10s
      - create env variables for SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET and ENVIRONMENT
