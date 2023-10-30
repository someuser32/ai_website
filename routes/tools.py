from contextlib import suppress as except_error

from fastapi import Request, Depends, Response, Body
from fastapi.responses import RedirectResponse

from .routes import BaseRoute


class ToolsPage(BaseRoute):
	def init(self):
		self.routes = {
			"/tools": self.tools_page,
		}

	async def tools_page(self, request: Request):
		return self.templates.TemplateResponse("tools.html", {"request": request})
