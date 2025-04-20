import os
from dotenv import load_dotenv

load_dotenv()

SQS_NOTIFICATION_QUEUE_URL = os.getenv("SQS_NOTIFICATION_QUEUE_URL")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
STATUS_SERVICE_URL = os.getenv("STATUS_SERVICE_URL")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL")
S3_BUCKET = os.getenv("S3_BUCKET")
