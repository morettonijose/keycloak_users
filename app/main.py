from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas, crud, database, auth
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

 
load_dotenv()

 
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
TOKEN_URL_PUBLIC = os.getenv("KEYCLOAK_TOKEN_URL_PUBLIC")

 
app = FastAPI(
    title="MVP 2025 POS - API Users",
    version="1.0.0",
    description="API for User Management",
    openapi_tags=[{"name": "users", "description": "User operations"}],
    swagger_ui_init_oauth={
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "usePkceWithAuthorizationCodeGrant": False,
    },
    dependencies=[Security(auth.verify_token)]  
)

 
models.Base.metadata.create_all(bind=database.engine)

 
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

 

@app.post("/user", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db),
    token_info: dict = Security(auth.get_token_info)  # 👈 Usa Security aqui!
):
    keycloak_user_id = token_info["sub"]  # Captura o ID do usuário autenticado
    return crud.create_user(db=db, user=user, keycloak_user_id=keycloak_user_id)

@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/user/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)

 
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MVP 2025 POS - API Users",
        version="1.0.0",
        description="API for User Management",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": TOKEN_URL_PUBLIC,  
                    "scopes": {}
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# 🚀 Ativa o OpenAPI customizado
app.openapi = custom_openapi
