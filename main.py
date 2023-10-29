import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from routes import *

load_dotenv(".env")

server = FastAPI()
server.mount("/static", StaticFiles(directory="static"), name="static")
server.add_middleware(SessionMiddleware, secret_key=os.getenv("MIDDLEWARE_SECRET"))

templates = Jinja2Templates(directory="templates")

register_routes(
    IndexPage,
	LoginPage,
    server=server
)

uvicorn.run(app=server, host="0.0.0.0", port=8080)
