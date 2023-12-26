provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      hashicorp-learn = "lambda-api-gateway"
    }
  }

}

// Authorize Lambda Setup
// S3 for lambda files
// random name generator
resource "random_pet" "spotifyapp-lambda-authorize-name" {
  prefix = "spotify-app"
  length = 4
}

// setting up s3 bucket to store lambda code
resource "aws_s3_bucket" "spotifyapp-lambda-authorize" {
  bucket = random_pet.spotifyapp-lambda-authorize-name.id
}

resource "aws_s3_bucket_ownership_controls" "spotifyapp-lambda-authorize" {
  bucket = aws_s3_bucket.spotifyapp-lambda-authorize.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "spotifyapp-lambda-authorize" {
  depends_on = [aws_s3_bucket_ownership_controls.spotifyapp-lambda-authorize]

  bucket = aws_s3_bucket.spotifyapp-lambda-authorize.id
  acl    = "private"
}

// zip the lambda files
data "archive_file" "spotifyapp-lambda-authorize" {
  type = "zip"

  source_dir  = "${path.module}/../authorize_lambda_deploy"
  output_path = "${path.module}/../authorize_lambda_deploy/spotify_lambda_auth.zip"
}

// copy lambda zip to s3
resource "aws_s3_object" "spotifyapp-lambda-authorize" {
  bucket = aws_s3_bucket.spotifyapp-lambda-authorize.id

  key    = "spotify_lambda_auth.zip"
  source = data.archive_file.spotifyapp-lambda-authorize.output_path

  etag = filemd5(data.archive_file.spotifyapp-lambda-authorize.output_path)
}

// function creation
resource "aws_lambda_function" "spotifyapp-lambda-authorize" {
  function_name = "spotifyapp-lambda-authorize"

  s3_bucket = aws_s3_bucket.spotifyapp-lambda-authorize.id
  s3_key    = aws_s3_object.spotifyapp-lambda-authorize.key

  runtime = "python3.11"
  handler = "lambda_authorize_user.handler"

  source_code_hash = data.archive_file.spotifyapp-lambda-authorize.output_base64sha256

  role = "arn:aws:iam::820978049141:role/Spotify_App_Lambda"
}

// Refresh Lambda Setup
// S3 for lambda files
// random name generator
resource "random_pet" "spotifyapp-lambda-refresh-name" {
  prefix = "spotify-app"
  length = 4
}

// setting up s3 bucket to store lambda code
resource "aws_s3_bucket" "spotifyapp-lambda-refresh" {
  bucket = random_pet.spotifyapp-lambda-refresh-name.id
}

resource "aws_s3_bucket_ownership_controls" "spotifyapp-lambda-refresh" {
  bucket = aws_s3_bucket.spotifyapp-lambda-refresh.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "spotifyapp-lambda-refresh" {
  depends_on = [aws_s3_bucket_ownership_controls.spotifyapp-lambda-refresh]

  bucket = aws_s3_bucket.spotifyapp-lambda-refresh.id
  acl    = "private"
}

// zip the lambda files
data "archive_file" "spotifyapp-lambda-refresh" {
  type = "zip"

  source_dir  = "${path.module}/../refresh_lambda_deploy"
  output_path = "${path.module}/../refresh_lambda_deploy/spotify_lambda_refresh.zip"
}

// copy lambda zip to s3
resource "aws_s3_object" "spotifyapp-lambda-refresh" {
  bucket = aws_s3_bucket.spotifyapp-lambda-refresh.id

  key    = "spotify_lambda_refresh.zip"
  source = data.archive_file.spotifyapp-lambda-refresh.output_path

  etag = filemd5(data.archive_file.spotifyapp-lambda-refresh.output_path)
}

// function creation
resource "aws_lambda_function" "spotifyapp-lambda-refresh" {
  function_name = "spotifyapp-lambda-refresh"

  s3_bucket = aws_s3_bucket.spotifyapp-lambda-refresh.id
  s3_key    = aws_s3_object.spotifyapp-lambda-refresh.key

  runtime = "python3.11"
  handler = "lambda_authorize_user.handler"

  source_code_hash = data.archive_file.spotifyapp-lambda-refresh.output_base64sha256

  role = "arn:aws:iam::820978049141:role/Spotify_App_Lambda"
}




// API Gateway
resource "aws_apigatewayv2_api" "spotifyapp" {
  name          = "spotifyapp-gateway"
  protocol_type = "HTTP"
}


resource "aws_apigatewayv2_stage" "spotifyapp-deploy" {
  api_id = aws_apigatewayv2_api.spotifyapp.id

  name        = "spotifyapp-deploy"
  auto_deploy = true
}

// authorization integration
// use proxy integration 
resource "aws_apigatewayv2_integration" "spotifyapp-integration-auth" {
  api_id = aws_apigatewayv2_api.spotifyapp.id

  integration_uri    = aws_lambda_function.spotifyapp-lambda-authorize.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "spotifyapp-route-auth" {
  api_id = aws_apigatewayv2_api.spotifyapp.id

  route_key = "POST /auth"
  target    = "integrations/${aws_apigatewayv2_integration.spotifyapp-integration-auth.id}"
}

resource "aws_lambda_permission" "api_gw_auth" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.spotifyapp-lambda-authorize.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.spotifyapp.execution_arn}/*/*"
}

// refresh integration
// use proxy integration 
resource "aws_apigatewayv2_integration" "spotifyapp-integration-refresh" {
  api_id = aws_apigatewayv2_api.spotifyapp.id

  integration_uri    = aws_lambda_function.spotifyapp-lambda-refresh.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "spotifyapp-route-refresh" {
  api_id = aws_apigatewayv2_api.spotifyapp.id

  route_key = "POST /refresh"
  target    = "integrations/${aws_apigatewayv2_integration.spotifyapp-integration-refresh.id}"
}

resource "aws_lambda_permission" "api_gw_refresh" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.spotifyapp-lambda-refresh.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.spotifyapp.execution_arn}/*/*"
}
