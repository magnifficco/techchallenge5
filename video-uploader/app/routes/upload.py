import boto3
import json
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File
from app.core.config import SQS_QUEUE_URL, AWS_REGION, S3_BUCKET

router = APIRouter()
s3 = boto3.client("s3", region_name=AWS_REGION)
sqs = boto3.client("sqs", region_name=AWS_REGION)

@router.post("/")
async def upload_video(file: UploadFile = File(...)):
    try:
        file_id = str(uuid4())
        s3_key = f"{file_id}_{file.filename}"
        file_bytes = await file.read()

        # Upload para o S3
        s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=file_bytes)

        # Enviar metadados para fila
        message = {
            "s3_key": s3_key,
            "video_id": file_id,
            "user_id": "usuario@exemplo.com"  # ajustar depois
        }
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message)
        )
        print(f"[DEBUG] Resposta do SQS: {response}")

        return {"message": "Upload realizado com sucesso", "video_id": file_id}
    
    except Exception as e:
        print(f"[ERRO] Upload falhou: {e}")
        return {"error": str(e)}