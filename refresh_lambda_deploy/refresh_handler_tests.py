import unittest
from lambda_refresh_access_token import *


class TestRefreshHandler(unittest.TestCase):
    def test_refreshLambdaHandler_BadQueryParams_ReturnsErrorResponse(self):
        # arrange
        event = {
            "params": {}
        }
        context = {}

        # act
        error_response = lambda_handler(event, context)

        # assert
        self.assertEqual(error_response["statusCode"], 500)

    # unfinished, need dependency injection to mock spotify providers (ProviderFactory with TestProvider implementation)
    def test_refreshLambdaHandler_BadRequestAcessTokenResponse_ReturnsErrorResponse(self):
        # arrange
        event = {
            "params": {
                "queryStringParameters": {
                    "code": "test code"
                }
            }
        }
        context = {}

        # act
        error_response = lambda_handler(event, context)

        # assert
        self.assertEqual(error_response["statusCode"], 500)


if __name__ == '__main__':
    unittest.main()
