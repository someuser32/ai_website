from typing import Any, Callable, Coroutine, Iterable

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


class BaseRoute:
	def __init__(self, server: FastAPI, **kwargs):
		self._server = server
		self._templates = Jinja2Templates(directory="templates")

		for key, value in kwargs.items():
			setattr(self, f"_{key}", value)

		self.routes : dict[str, Callable[..., Coroutine] | Iterable[Callable[..., Coroutine], dict[str, Any]]] = {}

		self.init()

		for path, route_info in self.routes.items():
			if callable(route_info):
				server.add_api_route(path, endpoint=route_info, name=path, methods=("GET",), response_class=HTMLResponse)
			else:
				server.add_api_route(path, endpoint=route_info[0], **({"name": path} | route_info[1]))

	def init():
		pass

	@property
	def server(self) -> FastAPI:
		return self._server

	@property
	def templates(self) -> Jinja2Templates:
		return self._templates
