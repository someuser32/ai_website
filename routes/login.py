import os

from fastapi import Request
from fastapi_login import LoginManager

from .routes import BaseRoute
from .lib import generate_captcha

manager = LoginManager(os.getenv("LOGIN_SECRET"), "/api/login")

class LoginPage(BaseRoute):
	def init(self):
		self.routes = {
			"/login": self.login_page,
		}

	async def login_page(self, request: Request, registration: int | None=0, utm_source: str | None=None):
		captcha = None
		if registration == 1:
			text, captcha = generate_captcha(request=request, width=400, height=100)
		return self.templates.TemplateResponse("login.html", {"request": request, "registration": registration, "captcha": captcha})
