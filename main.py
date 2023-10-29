import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

load_dotenv(".env")

from util import DB
from routes import *


server = FastAPI()
server.mount("/static", StaticFiles(directory="static"), name="static")
server.add_middleware(SessionMiddleware, secret_key=os.getenv("MIDDLEWARE_SECRET"))

db = DB(os.getenv("MONGO_CONNECTION"))

def register_routes():
    IndexPage(server=server)
    LoginPage(server=server)

def main():
    register_routes()
    uvicorn.run(app=server, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()