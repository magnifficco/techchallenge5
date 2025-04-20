from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.utils.notifier import send_notification

router = APIRouter()

class Notification(BaseModel):
    email: EmailStr
    status: str
    video_id: str

@router.post("/notify")
async def notify(payload: Notification):
    subject = f"Status do seu vídeo {payload.video_id}"
    message = f"Seu vídeo foi processado com status: {payload.status}"

    await send_notification(
        email=payload.email,
        subject=subject,
        message=message
    )

    return {"message": "Notificação publicada no SNS"}
