import boto3
import os
import asyncio

sns = boto3.client("sns", region_name=os.getenv("AWS_REGION"))

async def send_notification(email: str, subject: str, message: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: sns.publish(
            TopicArn=os.getenv("SNS_TOPIC_ARN"),
            Subject=subject,
            Message=message,
            MessageAttributes={
                "email": {
                    "DataType": "String",
                    "StringValue": email
                }
            }
        )
    )
