from fastapi import APIRouter, Request, Depends
import mysql.connector
import os
from dotenv import load_dotenv
from pydantic import BaseModel


router = APIRouter(prefix = "/api", tags = ["api"])

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE"),
}

def get_db():
    db = mysql.connector.connect(**DB_CONFIG)
    try:
        yield db
    finally:
        db.close()

class NameUpdate(BaseModel):
    name: str


@router.get("/member")
def member_query(username: str, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = "SELECT `id`, `name`, `username` FROM `member` WHERE `username` = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    if user:
        return {"data": {"id": user["id"], "name": user["name"], "username": username}}
    else:
        return {"data": None}
    

@router.patch("/member")
def name_update(update_date: NameUpdate, request: Request, db=Depends(get_db)):
    id = request.session.get("id")
    if id:
        cursor = db.cursor(dictionary=True)
        query = "UPDATE `member` SET `name` = %s WHERE `id` = %s"
        cursor.execute(query, (update_date.name, id))
        db.commit()
        request.session["name"] = update_date.name
        return {"ok": True}
    else:
        return {"error": True}


