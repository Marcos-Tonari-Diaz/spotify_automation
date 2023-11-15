# spotify_automation
Web app to save Discover weekly playlist songs in a single archive playlist.

Key Decisions
- Not using spotipy: I wanted to code the authorization flow by myself for my own education
- Cloud architecture:
    - Use AWS Lambda to :
        - listen to requests for the first access. A simple backend function can trigger the Sopitfy authorization flow and save the new user's refresh token.
        - run the copying script. After the initial authorization flow, all the backend needs to do is call the Spotify API to copy new song to the archive.
    - Use CloudWatch to trigger the Lambda function weekly.
    - Use DynamoDB as the refresh token store: AWS Secrets Manager would be the best way to store user tokens, but it doesn't have a free tier. Dynamo DB has an encryption API.
