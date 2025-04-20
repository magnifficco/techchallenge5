from fastapi import APIRouter
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key
import boto3
from app.core.config import AWS_REGION, DYNAMODB_TABLE
from datetime import datetime

router = APIRouter()
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

class StatusUpdate(BaseModel):
    video_id: str
    user_id: str
    status: str

@router.post("/videos/status")
def update_status(payload: StatusUpdate):
    table.put_item(Item={
        "video_id": payload.video_id,
        "user_id": payload.user_id,
        "status": payload.status,
        "updated_at": datetime.utcnow().isoformat()
    })
    return {"message": "Status atualizado com sucesso"}

@router.get("/videos/{user_id}")
def list_status(user_id: str):
    response = table.query(
        IndexName="user_id-index",
        KeyConditionExpression=Key("user_id").eq(user_id)
    )
    return response["Items"]
