import boto3
import json
import time
import traceback
from app.utils.notifier import send_notification
from app.core.config import AWS_REGION, SQS_NOTIFICATION_QUEUE_URL

sqs = boto3.client("sqs", region_name=AWS_REGION)

def process_notifications():
    print("[INFO] Iniciando consumidor da fila de notificações (SQS)...")

    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=SQS_NOTIFICATION_QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )
            messages = response.get("Messages", [])
            if not messages:
                print("[DEBUG] Nenhuma mensagem recebida.")
                continue

            for msg in messages:
                try:
                    body = json.loads(msg["Body"])
                    email = body.get("email")
                    status = body.get("status")
                    video_id = body.get("video_id")

                    print(f"[INFO] Notificando {email} sobre vídeo {video_id} com status {status}")
                    send_notification(email, status, video_id)
                    print(f"[SUCESSO] Notificação enviada para {email}")
                except Exception as e:
                    print(f"[ERRO] Falha ao processar notificação: {e}")
                    traceback.print_exc()

                try:
                    sqs.delete_message(
                        QueueUrl=SQS_NOTIFICATION_QUEUE_URL,
                        ReceiptHandle=msg["ReceiptHandle"]
                    )
                    print("[DEBUG] Mensagem removida da fila.")
                except Exception as e:
                    print(f"[ERRO] Erro ao remover mensagem: {e}")

        except Exception as e:
            print(f"[ERRO] Erro ao consumir mensagens: {e}")
            time.sleep(5)
