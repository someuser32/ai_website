import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

load_dotenv(".env")

from routes import *
from util import DB

server = FastAPI()
server.mount("/static", StaticFiles(directory="static"), name="static")
server.add_middleware(SessionMiddleware, secret_key=os.getenv("MIDDLEWARE_SECRET"))

db = DB(os.getenv("MONGODB_SECRET"))

def register_routes():
    API(server=server, db=db)
    IndexPage(server=server)
    LoginPage(server=server, db=db)
    ProfilePage(server=server)
    ToolsPage(server=server)

def main():
    register_routes()
    uvicorn.run(app=server, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
