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
async def member_query(username: str, request: Request, db=Depends(get_db)):
    is_authenticated = request.session.get("authenticated",False)
    if not is_authenticated:
        return {"error": True}
    cursor = db.cursor(dictionary=True)
    select_query = "SELECT `id`, `name`, `username` FROM `member` WHERE `username` = %s"
    cursor.execute(select_query, (username,))
    user = cursor.fetchone()
    if user:
        return {"data": {"id": user["id"], "name": user["name"], "username": username}}
    else:
        return {"data": None}
    

@router.patch("/member")
async def name_update(update_data: NameUpdate, request: Request, db=Depends(get_db)):
    is_authenticated = request.session.get("authenticated",False)
    id = request.session.get("id")
    if not is_authenticated or not id:
        return {"error": True}
    cursor = db.cursor(dictionary=True)
    update_query = "UPDATE `member` SET `name` = %s WHERE `id` = %s"
    cursor.execute(update_query, (update_data.name, id))
    db.commit()
    request.session["name"] = update_data.name
    return {"ok": True}


