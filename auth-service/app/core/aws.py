import os
import boto3

def get_cognito_client():
    return boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION"))
