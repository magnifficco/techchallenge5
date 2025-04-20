import os
from dotenv import load_dotenv

load_dotenv()

def get_env(name, default):
    return os.getenv(name, default)

SQS_QUEUE_URL = get_env("SQS_QUEUE_URL", "")
AWS_REGION = get_env("AWS_REGION", "us-east-1")
S3_BUCKET = get_env("S3_BUCKET", "")

# Permite sobrescrever por variável local
STATUS_SERVICE_URL = get_env("STATUS_SERVICE_URL", "http://status-service:8003")
NOTIFICATION_SERVICE_URL = get_env("NOTIFICATION_SERVICE_URL", "http://notification-service:8004")
