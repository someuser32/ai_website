import asyncio
import base64
import io
from contextlib import suppress as except_error
from typing import Annotated

import PIL.Image
from fastapi import Body, Depends, Request, Response, WebSocket
from pydantic import BaseModel

from .routes import BaseRoute
from .tools_util import Upscaler, SketchMaker


class UpscalerUpscaleRequestModel(BaseModel):
	model: str = "RealESRGAN_x4plus_anime_6B"
	scale: int = 4


class ToolsPage(BaseRoute):
	def init(self):
		self.routes = {
			"/tools": self.tools_page,
			"/tools/upscaler": self.upscaler_page,
			"/tools/sketch-maker": self.sketchmaker_page,
		}
		self.websockets = {
			"/websocket/tools/upscaler/upscale": self.upscaler_api_upscale,
			"/websocket/tools/sketch-maker/sketch": self.sketchmaker_api_sketch,
		}
		self._upscaler = Upscaler()
		self.upscaler.load_models()
		self._sketchmaker = SketchMaker()

	@property
	def upscaler(self) -> Upscaler:
		return self._upscaler

	@property
	def sketchmaker(self) -> SketchMaker:
		return self._sketchmaker

	async def tools_page(self, request: Request):
		return self.templates.TemplateResponse("tools.html", {"request": request})

	async def upscaler_page(self, request: Request):
		return self.templates.TemplateResponse("tools/upscaler.html", {"request": request, "models": Upscaler.model_names})

	async def upscaler_api_upscale(self, websocket: WebSocket):
		await websocket.accept()

		img = await websocket.receive_bytes()
		image = PIL.Image.open(io.BytesIO(img))
		if (image.size[0] * image.size[1]) > (800*800):
			await websocket.send_json({"status": "error", "reason": f"cannot process image greater than {800*800} pixels! (> ~800*800)"})
			return await websocket.close()

		await websocket.send_json({"status": "success"})

		data = await websocket.receive_json()
		if data["scale"] not in (2, 4):
			await websocket.send_json({"status": "error", "reason": "scale must be 2 or 4!"})
			return await websocket.close()
		if data["model"] not in Upscaler.model_names:
			await websocket.send_json({"status": "error", "reason": "unknown model name!"})
			return await websocket.close()

		try:
			loop = asyncio.get_event_loop()
			out_img = await loop.run_in_executor(None, self.upscaler.upscale, image, data["scale"], data["model"])
		except BaseException as e:
			await websocket.send_json({"status": "error", "reason": e.args[0]})
		else:
			out_img_io = io.BytesIO()
			out_img.save(out_img_io, "png")
			out_img_io.seek(0)
			await websocket.send_bytes(out_img_io.read())

		return await websocket.close()

	async def sketchmaker_page(self, request: Request):
		return self.templates.TemplateResponse("tools/sketchmaker.html", {"request": request, "ranges": SketchMaker.ranges})

	async def sketchmaker_api_sketch(self, websocket: WebSocket):
		await websocket.accept()

		img = await websocket.receive_bytes()
		await websocket.send_json({"status": "success"})

		data = await websocket.receive_json()
		for key, value in data.items():
			if rang := SketchMaker.ranges.get(key):
				if value not in rang:
					await websocket.send_json({"status": "error", "reason": f"{key} must be between {rang.start} and {rang.stop} with step {rang.step}"})
					return await websocket.close()

		try:
			image = PIL.Image.open(io.BytesIO(img))

			loop = asyncio.get_event_loop()
			out_img = await loop.run_in_executor(None, lambda: self.sketchmaker.sketch(image, **data))
		except BaseException as e:
			await websocket.send_json({"status": "error", "reason": e.args[0]})
		else:
			out_img_io = io.BytesIO()
			out_img.save(out_img_io, "png")
			out_img_io.seek(0)
			await websocket.send_bytes(out_img_io.read())

		return await websocket.close()
