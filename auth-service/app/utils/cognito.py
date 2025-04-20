import os
import boto3
from botocore.exceptions import ClientError

COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")

client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))

def authenticate_user(email: str, password: str):
    try:
        response = client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password
            }
        )
        return response["AuthenticationResult"]
    except ClientError as e:
        raise Exception(e.response["Error"]["Message"])
