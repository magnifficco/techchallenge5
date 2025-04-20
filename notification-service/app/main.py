from fastapi import FastAPI
from app.routes.notify import router as notification_router

app = FastAPI()

app.include_router(notification_router)
