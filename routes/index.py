from fastapi import Request
from fastapi.responses import FileResponse

from .routes import BaseRoute


class IndexPage(BaseRoute):
	def init(self):
		self.routes = {
			"/": self.index_page,
			"/favicon.ico": (self.favicon_page, {
				"methods": ("GET",),
				"response_class": FileResponse,
			}),
		}

	async def index_page(self, request: Request, utm_source: str | None=None):
		return self.templates.TemplateResponse("index.html", {"request": request})

	async def favicon_page(self, request: Request):
		return FileResponse("static/favicon.ico")
