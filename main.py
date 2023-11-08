import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from starlette.middleware.sessions import SessionMiddleware

load_dotenv(".env")

from routes import *
from util import DB

server = FastAPI()
server.mount("/static", StaticFiles(directory="static"), name="static")
server.add_middleware(SessionMiddleware, secret_key=os.getenv("MIDDLEWARE_SECRET"))

db = DB(os.getenv("MONGODB_SECRET"))
manager = LoginManager(os.getenv("LOGIN_SECRET"), "/api/login", use_cookie=True)

def register_routes():
    API(server=server, db=db)
    IndexPage(server=server)
    LoginPage(server=server, db=db, manager=manager)
    ProfilePage(server=server)
    ToolsPage(server=server, manager=manager)

def main():
    register_routes()
    uvicorn.run(app=server, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
