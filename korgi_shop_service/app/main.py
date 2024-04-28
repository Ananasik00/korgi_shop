import os
import uvicorn
from fastapi import FastAPI, status, Form, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from keycloak import KeycloakOpenID

from database import database as database
from database.database import KorgiDB
from model.model import Korgi


app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def chech_for_role_test(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (chech_for_role_test(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.post("/add_korgi")
async def add_korgi(korgi: Korgi, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        new_korgi = KorgiDB(**korgi.dict())
        db.add(new_korgi)
        db.commit()
        db.refresh(new_korgi)
        return new_korgi
    else:
        return "Wrong JWT Token"

@app.get("/korgis")
async def list_korgis(db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        korgis = db.query(KorgiDB).all()
        return korgis
    else:
        return "Wrong JWT Token"

@app.get("/get_korgi_by_id")
async def get_korgi_by_id(korgi_id: int, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        korgi = db.query(KorgiDB).filter(KorgiDB.id == korgi_id).first()
        if not korgi:
            raise HTTPException(status_code=404, detail="Korgi not found")
        return korgi
    else:
        return "Wrong JWT Token"

@app.delete("/delete_korgi")
async def delete_korgi(korgi_id: int, db: db_dependency, token: str = Header()):
    if (chech_for_role_test(token)):
        korgi = db.query(KorgiDB).filter(KorgiDB.id == korgi_id).first()
        if not korgi:
            raise HTTPException(status_code=404, detail="Korgi not found")
        db.delete(korgi)
        db.commit()
        return {"message": "Korgi deleted successfully"}
    else:
        return "Wrong JWT Token"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
