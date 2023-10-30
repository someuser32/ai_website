from __future__ import annotations

import datetime
from contextlib import suppress as except_error
from typing import TYPE_CHECKING

from email_validator import validate_email, EmailNotValidError
from fastapi import Request, Depends, Response, Body
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from .routes import BaseRoute
from .lib import generate_captcha, check_captcha
from .exceptions import IncorrectCaptchaException, UsernameExistsException

if TYPE_CHECKING:
	from ..util import DB, User


class ProfilePage(BaseRoute):
	def init(self):
		self.routes = {
			"/profile": self.profile_page,
		}

	@property
	def db(self) -> DB:
		return self._db

	async def profile_page(self, request: Request):
		user = request.state.user
		if user is None:
			return RedirectResponse(f"{request.url_for('/profile')}")
		return self.templates.TemplateResponse("profile.html", {"request": request})
