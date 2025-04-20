import os

COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
