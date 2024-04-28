import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from database import database as database
from database.database import KorgiDB
from model.model import Korgi

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}


@app.post("/add_korgi")
async def add_korgi(korgi: Korgi, db: db_dependency):
    new_korgi = KorgiDB(**korgi.dict())
    db.add(new_korgi)
    db.commit()
    db.refresh(new_korgi)
    return new_korgi


@app.get("/korgis")
async def list_korgis(db: db_dependency):
    korgis = db.query(KorgiDB).all()
    return korgis


@app.get("/get_korgi_by_id")
async def get_korgi_by_id(korgi_id: int, db: db_dependency):
    korgi = db.query(KorgiDB).filter(KorgiDB.id == korgi_id).first()
    if not korgi:
        raise HTTPException(status_code=404, detail="Korgi not found")
    return korgi


@app.delete("/delete_korgi")
async def delete_korgi(korgi_id: int, db: db_dependency):
    korgi = db.query(KorgiDB).filter(KorgiDB.id == korgi_id).first()
    if not korgi:
        raise HTTPException(status_code=404, detail="Korgi not found")
    db.delete(korgi)
    db.commit()
    return {"message": "Korgi deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
