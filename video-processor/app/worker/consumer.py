import boto3
import json
import time
import httpx
import traceback
from pathlib import Path
from app.utils.processing import process_video
from app.core.config import (
    SQS_QUEUE_URL,
    AWS_REGION,
    STATUS_SERVICE_URL,
    NOTIFICATION_SERVICE_URL,
    S3_BUCKET,
)

sqs = boto3.client("sqs", region_name=AWS_REGION)
s3 = boto3.client("s3", region_name=AWS_REGION)


def process_messages():
    print("[INFO] Iniciando consumidor da fila SQS...")

    while True:
        print("[DEBUG] Aguardando mensagem da fila...")
        try:
            response = sqs.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )
        except Exception as e:
            print(f"[ERRO] Erro ao receber mensagem da fila: {e}")
            time.sleep(5)
            continue

        messages = response.get("Messages", [])
        if not messages:
            print("[DEBUG] Nenhuma mensagem recebida.")
            continue

        for msg in messages:
            try:
                print(f"[DEBUG] Mensagem recebida: {msg}")
                body = json.loads(msg["Body"])
                s3_key = body["s3_key"]
                video_id = body["video_id"]
                user_id = body.get("user_id", "usuario@exemplo.com")

                local_path = f"/tmp/{s3_key}"
                print(f"[INFO] Baixando do S3: bucket={S3_BUCKET}, key={s3_key}")
                with open(local_path, "wb") as f:
                    s3.download_fileobj(S3_BUCKET, s3_key, f)
                print(f"[DEBUG] Arquivo salvo em: {local_path}")

                print(f"[INFO] Iniciando processamento do vídeo {video_id}...")
                zip_path = process_video(local_path)
                print(f"[SUCESSO] ZIP gerado em: {zip_path}")

                # Upload do zip para o S3
                zip_filename = Path(zip_path).name
                s3_output_key = f"outputs/{zip_filename}"
                with open(zip_path, "rb") as f:
                    s3.upload_fileobj(f, S3_BUCKET, s3_output_key)
                print(f"[INFO] ZIP enviado para o S3: {s3_output_key}")

                # Atualizar status
                status_payload = {
                    "video_id": video_id,
                    "user_id": user_id,
                    "status": "done"
                }
                print(f"[INFO] Enviando status para {STATUS_SERVICE_URL}...")
                r = httpx.post(f"{STATUS_SERVICE_URL}/videos/status", json=status_payload)
                print(f"[DEBUG] Resposta STATUS: {r.status_code} {r.text}")

                # Notificar
                notification_payload = {
                    "email": user_id,
                    "status": "done",
                    "video_id": video_id
                }
                print(f"[INFO] Enviando notificação para {NOTIFICATION_SERVICE_URL}...")
                r = httpx.post(f"{NOTIFICATION_SERVICE_URL}/notify", json=notification_payload)
                print(f"[DEBUG] Resposta NOTIFY: {r.status_code} {r.text}")

            except Exception as e:
                print(f"[ERRO] Erro ao processar vídeo: {e}")
                traceback.print_exc()

            try:
                print(f"[INFO] Removendo mensagem da fila...")
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
                print("[DEBUG] Mensagem removida com sucesso.")
            except Exception as e:
                print(f"[ERRO] Erro ao remover mensagem da fila: {e}")
