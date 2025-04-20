from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.aws import get_cognito_client
import os

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    try:
        client = get_cognito_client()
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': request.username,
                'PASSWORD': request.password
            },
            ClientId=os.getenv("COGNITO_CLIENT_ID")
        )
        return {"access_token": response["AuthenticationResult"]["AccessToken"]}
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
