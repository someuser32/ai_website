from __future__ import annotations

import datetime
from contextlib import suppress as except_error
from typing import TYPE_CHECKING

from fastapi import Depends, Request, Response
from fastapi.responses import PlainTextResponse

from .lib import generate_captcha
from .routes import BaseRoute

if TYPE_CHECKING:
	from util import DB


class API(BaseRoute):
	def init(self):
		self.routes = {
			"/api/refresh_captcha": (
				self.refresh_captcha, {
					"methods": ("POST",),
					"response_class": PlainTextResponse,
				},
			),
		}

	@property
	def db(self) -> DB:
		return self._db

	async def refresh_captcha(self, request: Request):
		text, captcha = generate_captcha(request=request, width=400, height=100)
		return PlainTextResponse(content=captcha)
