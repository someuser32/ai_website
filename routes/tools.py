import asyncio
import io
from contextlib import suppress as except_error
from typing import Annotated

import PIL.Image
from fastapi import Body, Depends, File, Form, Request, Response, WebSocket
from fastapi.responses import Response
from pydantic import BaseModel

from .routes import BaseRoute
from .tools_util import ColorCorrection, SketchMaker, Upscaler


class UpscalerUpscaleRequestModel(BaseModel):
	model: str = "RealESRGAN_x4plus_anime_6B"
	scale: int = 4


class ToolsPage(BaseRoute):
	def init(self):
		self.routes = {
			"/tools": self.tools_page,
			"/tools/upscaler": self.upscaler_page,
			"/tools/color-correction": self.color_correction_page,
			"/tools/sketch-maker": self.sketchmaker_page,
			"/api/tools/color-correction/correct": (self.color_correction_api_correct, {
				"methods": ("POST",),
			}),
			"/api/tools/sketch-maker/sketch": (self.sketchmaker_api_sketch, {
				"methods": ("POST",),
			}),
		}
		self.websockets = {
			"/websocket/tools/upscaler/upscale": self.upscaler_api_upscale,
		}
		self._upscaler = Upscaler()
		self.upscaler.load_models()
		self._color_correction = ColorCorrection()
		self._sketchmaker = SketchMaker()

	@property
	def upscaler(self) -> Upscaler:
		return self._upscaler

	@property
	def color_correction(self) -> ColorCorrection:
		return self._color_correction

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

	async def color_correction_page(self, request: Request):
		return self.templates.TemplateResponse("tools/color-correction.html", {"request": request, "ranges": ColorCorrection.ranges})

	async def color_correction_api_correct(self, request: Request, file: Annotated[bytes, File()], temperature: Annotated[int, Form()], hue: Annotated[int, Form()], brightness: Annotated[int, Form()], contrast: Annotated[int, Form()], saturation: Annotated[int, Form()], gamma: Annotated[float, Form()], exposure_offset: Annotated[float, Form()], vignette: Annotated[float, Form()], noise: Annotated[float, Form()], sharpness: Annotated[float, Form()], hdr: Annotated[float, Form()]):
		data = locals()
		for key, rang in ColorCorrection.ranges.items():
			value = data.get(key)
			if value is not None and value not in rang:
				return {"status": "error", "reason": f"{key} must be between {rang.start} and {rang.stop} with step {rang.step}"}

		try:
			image = PIL.Image.open(io.BytesIO(file))

			loop = asyncio.get_event_loop()
			out_img = await loop.run_in_executor(None, lambda: self.color_correction.correct(image, temperature, hue, brightness, contrast, saturation, gamma, exposure_offset, vignette, noise, sharpness, hdr))
		except BaseException as e:
			return {"status": "error", "reason": e.args[0]}
		else:
			out_img_io = io.BytesIO()
			out_img.save(out_img_io, "png")
			out_img_io.seek(0)

		return Response(content=out_img_io.read(), media_type="image/png")

	async def sketchmaker_page(self, request: Request):
		return self.templates.TemplateResponse("tools/sketchmaker.html", {"request": request, "ranges": SketchMaker.ranges})

	async def sketchmaker_api_sketch(self, request: Request, file: Annotated[bytes, File()], kernel: Annotated[int, Form()], sigma: Annotated[float, Form()], k_sigma: Annotated[float, Form()], eps: Annotated[float, Form()], phi: Annotated[float, Form()], gamma: Annotated[float, Form()]):
		data = locals()
		for key, rang in SketchMaker.ranges.items():
			value = data.get(key)
			if value is not None and value not in rang:
				return {"status": "error", "reason": f"{key} must be between {rang.start} and {rang.stop} with step {rang.step}"}

		try:
			image = PIL.Image.open(io.BytesIO(file))

			loop = asyncio.get_event_loop()
			out_img = await loop.run_in_executor(None, lambda: self.sketchmaker.sketch(image, kernel, sigma, k_sigma, eps, phi, gamma))
		except BaseException as e:
			return {"status": "error", "reason": e.args[0]}
		else:
			out_img_io = io.BytesIO()
			out_img.save(out_img_io, "png")
			out_img_io.seek(0)

		return Response(content=out_img_io.read(), media_type="image/png")
