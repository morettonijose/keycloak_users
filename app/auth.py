# app/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".local.env")

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_TOKEN_URL_PUBLIC = os.getenv("KEYCLOAK_TOKEN_URL_PUBLIC")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=KEYCLOAK_TOKEN_URL_PUBLIC
)

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        token_info = keycloak_openid.decode_token(
            token,
            key=None  # 👈 só key=None, mais nada
        )
        if not token_info:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or unauthorized token",
            )
    except Exception as e:
        print(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or unauthorized token",
        )
    return token


# 🔍 Se quiser pegar o token manualmente
def get_token_info(token: str = Depends(oauth2_scheme)):
    try:
        return keycloak_openid.decode_token(
            token,
            key=None  # 👈 apenas isso!
        )
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or unauthorized token",
        )