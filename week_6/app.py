from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated, Optional
import mysql.connector
import os
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import secrets

app = FastAPI()
app.mount("/statics", StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")
secret_key = secrets.token_hex(16)

load_dotenv()

DB_CONFIG = {
    "host":os.getenv("DB_HOST"),
    "port":os.getenv("DB_PORT"),
    "user":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD"),
    "database":os.getenv("DB_DATABASE"),
}

class FormData(BaseModel):
    name: Optional[str] = None
    username: str
    password: str
    model_config = {"extra": "forbid"}

class FormMessage(BaseModel):
    name: Optional[str] = None
    content: str
    model_config = {"extra": "forbid"}

class DataBase:
    def __init__(self,host,port,user,password,database):
        self.config = {
            "host":host,
            "port":port,
            "user":user,
            "password":password,
            "database":database
        }

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        is_authenticated = request.session.get("authenticated",False)
        if request.url.path == "/member" and not is_authenticated:
            return RedirectResponse(url="/",status_code=303)
        response = await call_next(request)
        return response

app.add_middleware(AuthMiddleware)
app.add_middleware(SessionMiddleware,secret_key=secret_key,session_cookie="user_session",max_age=86400)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )

@app.post("/signup")
async def signup(sign_up_data:Annotated[FormData,Form()],request: Request):
    with DataBase(**DB_CONFIG) as db:
        cursor =db.connection.cursor(dictionary=True)
        query = "SELECT * FROM `member` WHERE `username` = %s"
        cursor.execute(query,(sign_up_data.username,))
        user = cursor.fetchone()
        if user:
            error_token = secrets.token_hex(4)
            request.session["error_token"] = error_token
            return RedirectResponse(url=f"/error?message=此帳號已被註冊&token={error_token}",status_code=303)
        else: 
            query = "INSERT INTO `member`(`name`, `username`, `password`) VALUES(%s, %s, %s)"
            cursor.execute(query,(sign_up_data.name,sign_up_data.username,sign_up_data.password,))
            db.connection.commit()
            return RedirectResponse(url="/?success=true",status_code=303)

@app.post("/signin")
async def signin(sign_in_data:Annotated[FormData,Form()],request: Request):
    with DataBase(**DB_CONFIG) as db:
        cursor = db.connection.cursor(dictionary=True)
        query = "SELECT * FROM `member` WHERE `username` = %s"
        cursor.execute(query,(sign_in_data.username,))
        user = cursor.fetchone()
        if user and user["password"] == sign_in_data.password:
            request.session["authenticated"] = True
            request.session["name"] = user["name"]
            request.session["id"] = user["id"]
            return RedirectResponse(url="/member",status_code=303)
        else:
            error_token = secrets.token_hex(4)
            request.session["error_token"] = error_token
            return RedirectResponse(url=f"/error?message=帳號或密碼輸入錯誤&token={error_token}",status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def read_member_page(request: Request):
    name = request.session.get("name")
    id = int(request.session.get("id"))
    with DataBase(**DB_CONFIG) as db:
        cursor = db.connection.cursor(dictionary=True)
        query = "SELECT `message`.`id`,`message`.`member_id`,`member`.`name`, `message`.`content` FROM `member` JOIN `message` ON `message`.`member_id` = `member`.`id`"
        cursor.execute(query,)
        messages = cursor.fetchall()
    return templates.TemplateResponse("member.html", {"request": request, "name": name, "id":id, "messages": messages})

@app.get("/error")
async def read_error_page(request: Request, message:str = None,token:str = None):
    session_token = request.session.pop("error_token", None)
    if not token or token != session_token:
        return RedirectResponse(url="/",status_code=303)
    return templates.TemplateResponse(
        "error.html", {"request": request, "message": message}
    )

@app.get("/signout")
async def sign_out(request: Request):
    request.session.clear()
    return RedirectResponse(url="/",status_code=303)


@app.post("/createMessage", name="createMessage")
async def create_message(message_data:Annotated[FormMessage,Form()],request: Request):
    with DataBase(**DB_CONFIG) as db:
        id = request.session.get("id")
        if not id:
            return RedirectResponse(url="/",status_code=303)
        else:
            cursor = db.connection.cursor(dictionary=True)
            query = "INSERT INTO `message`(`member_id`, `content`) VALUES(%s, %s)"
            cursor.execute(query,(id, message_data.content))
            db.connection.commit()
        return RedirectResponse(url="/member",status_code=303)
    
    
@app.post("/deleteMessage", name="deleteMessage")
async def delete_message(message_id:Annotated[int, Form()],request:Request):
    with DataBase(**DB_CONFIG) as db:
        id = request.session.get("id")
        cursor = db.connection.cursor(dictionary=True)
        query = "DELETE FROM `message` WHERE `id` = %s AND `member_id` = %s"
        cursor.execute(query,(message_id, id))
        db.connection.commit()
    return RedirectResponse(url="/member",status_code=303)


if __name__ ==  "__main__":
    import uvicorn
    uvicorn.run(app, host= "0.0.0.0", port= 8000)