from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Annotated
from pydantic import BaseModel
import secrets

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
secret_key = secrets.token_hex(16)

class FormData(BaseModel):
    username: str
    password: str
    terms: bool = True
    model_config = {"extra": "forbid"}

class UserAuthenticator:
    async def authenticate(self, username, password):
        # 設定基本密碼檢查規則
        pass

class HardcodedAuthenticator(UserAuthenticator):
    async def authenticate(self, username, password):
        correct_username = "test"
        correct_password = "test"
        if username == correct_username and password == correct_password:
            return True
        else:
            return False
        
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        is_authenticated = request.session.get("authenticated", False)
        if request.url.path == "/member" and not is_authenticated:
            return RedirectResponse(url="/", status_code=303)
        response = await call_next(request)
        return response

app.add_middleware(AuthMiddleware)
app.add_middleware(SessionMiddleware,secret_key=secret_key,session_cookie="user_session",max_age=86400)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )

@app.post("/signin")
async def signin(sign_in_data:Annotated[FormData,Form()],request: Request):
    authenticator = HardcodedAuthenticator()
    if await authenticator.authenticate(sign_in_data.username,sign_in_data.password):
        request.session["authenticated"] = True
        return RedirectResponse(url="/member", status_code=303)
    elif sign_in_data.username == "" or sign_in_data.password == "":
        error_token = secrets.token_hex(4)
        request.session["error_token"] = error_token
        return RedirectResponse(url=f"/error?message=請輸入帳號和密碼&token={error_token}", status_code=303)
    else:
        error_token = secrets.token_hex(4)
        request.session["error_token"] = error_token
        return RedirectResponse(url=f"/error?message=帳號、或密碼錯誤&token={error_token}", status_code=303)

@app.get("/member")
async def member_page(request: Request):
        return templates.TemplateResponse(
        "member.html",{"request": request})

@app.get("/error")
async def error_page(request: Request, message:str = None, token:str = None):
    session_token = request.session.pop("error_token", None)
    if not token or token != session_token:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        "error.html",{"request": request, "message": message}
    )

@app.get("/signout")
async def signout(request: Request):
        request.session.clear()
        return RedirectResponse(url="/", status_code=303)

@app.get("/square/{number}", response_class=HTMLResponse)
async def calculate_square(request: Request, number:int):
    result =  number * number
    return templates.TemplateResponse(
        "square.html", {"request": request,"number":number,"result":result}
    )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)