from __future__ import annotations

import datetime
import os
from contextlib import suppress as except_error
from typing import TYPE_CHECKING, Annotated

from email_validator import EmailNotValidError, validate_email
from fastapi import Body, Depends, Form, Request, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic import BaseModel

from .exceptions import IncorrectCaptchaException, UsernameExistsException
from .lib import check_captcha, generate_captcha
from .routes import BaseRoute

if TYPE_CHECKING:
	from ..util import DB, User


class LoginPage(BaseRoute):
	def init(self):
		self.manager.useRequest(self.server)
		self.routes = {
			"/login": self.login_page,
			"/logout": self.logout_page,
			"/api/login": (self.api_login, {
				"methods": ("POST",),
			}),
			"/api/register": (self.api_register, {
				"methods": ("POST",),
			}),
			"/api/logout": (self.api_logout, {
				"methods": ("POST",),
			}),
		}
		self.manager.user_loader()(self._query_login_user)

	@property
	def db(self) -> DB:
		return self._db

	@property
	def manager(self) -> LoginManager:
		return self._manager

	async def login_page(self, request: Request, registration: int | None=0, utm_source: str | None=None):
		user = request.state.user
		if user is not None:
			return RedirectResponse(f"{request.url_for('/')}?utm_source=login")
		captcha = None
		if registration == 1:
			text, captcha = generate_captcha(request=request, width=400, height=100)
		return self.templates.TemplateResponse("login.html", {"request": request, "registration": registration, "captcha": captcha})

	async def logout_page(self, request: Request, redirect_to: str | None=None):
		response = await self.api_logout(request=request, response=RedirectResponse(url=redirect_to or request.url_for("/")))
		response.status_code = 307
		return response

	async def api_login(self, response: Response, data: Annotated[OAuth2PasswordRequestForm, Depends()], save: Annotated[int, Form()]):
		user = await self.db.query_user({"username": data.username})
		if not user:
			raise InvalidCredentialsException
		elif not user.check_password(data.password):
			raise InvalidCredentialsException

		session_token = self.manager.create_access_token(data={"sub": user.username}, expires=datetime.timedelta(days=14) if save == 1 else datetime.timedelta(hours=2))
		# NOTE: may be security risks if i disable httponly?
		# but it's need for websocket requests
		response.set_cookie(key=self.manager.cookie_name, value=session_token, httponly=False)
		# self.manager.set_cookie(response, session_token)
		response.status_code = 200
		return response

	async def api_register(self, request: Request, response: Response, username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], captcha: Annotated[str, Form()]):
		if not check_captcha(request, captcha):
			raise IncorrectCaptchaException

		user = await self.db.query_user({"username": username})
		if user is not None:
			raise UsernameExistsException

		try:
			emailinfo = validate_email(email, check_deliverability=False)
			email = emailinfo.normalized
		except EmailNotValidError as e:
			raise HTTPException(status_code=400, detail=e.args[0], headers={"WWW-Authenticate": "Bearer"})

		user = await self.db.create_user(username, email, password)

		with except_error(InvalidCredentialsException):
			response = await self.api_login(response=response, data=OAuth2PasswordRequestForm(username=username, password=password), save=1)

		response.status_code = 200
		return response

	async def api_logout(self, request: Request, response: Response):
		user = request.state.user
		if not user:
			raise InvalidCredentialsException

		response.delete_cookie("access-token")
		response.status_code = 200
		return response

	async def _query_login_user(self, username: str):
		return await self.db.query_user({"username": username})
