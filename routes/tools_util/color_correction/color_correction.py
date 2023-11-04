import cv2
import numpy as np
from blendmodes.blend import BlendType, blendLayers
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps

from .. import arg_range


class ColorCorrection:
	ranges = {
		"temperature": arg_range(-100, 100, 1, 0, "Temperature"),
		"hue": arg_range(-100, 100, 1, 0, "Hue"),
		"brightness": arg_range(-100, 100, 1, 0, "Brightness"),
		"contrast": arg_range(-100, 100, 1, 0, "Contrast"),
		"saturation": arg_range(-100, 100, 1, 0, "Saturation"),
		"gamma": arg_range(0.2, 2.2, 0.1, 1, "Gamma"),
		"exposure_offset": arg_range(0, 1, 0.01, 0, "Exposure offset"),
		"vignette": arg_range(0, 1, 0.01, 0, "Vignette"),
		"noise": arg_range(0, 1, 0.01, 0, "Noise"),
		"sharpness": arg_range(0, 1, 0.01, 0, "Sharpness"),
		"hdr": arg_range(0, 1, 0.01, 0, "HDR"),
	}

	def __init__(self):
		pass

	def correct(self, input_img: Image.Image, temperature: int=0, hue: int=0, brightness: int=0, contrast: int=0, saturation: int=0, gamma: float=1, exposure_offset: float=0, vignette: float=0, noise: float=0, sharpness: float=0, hdr: float=0) -> Image.Image:
		brightness /= 100
		contrast /= 100
		temperature /= 100
		saturation /= 100

		img = input_img

		if exposure_offset > 0:
			img = ImageEnhance.Brightness(Image.fromarray(np.clip(np.array(img).astype(float) + exposure_offset * 75, 0, 255).astype(np.uint8))).enhance((brightness+1) - exposure_offset / 4)

		if hdr > 0:
			converted_original_img = (np.array(input_img)[:, :, ::-1].copy().astype("float32") / 255.0)
			converted_sharped = (np.array(Image.blend(img, ImageChops.difference(img, img.filter(ImageFilter.GaussianBlur(radius=2.8))), 1))[:, :, ::-1].copy().astype("float32") / 255.0)
			converted_color_dodge = (255 * (converted_original_img / (1 - converted_sharped))).clip(0, 255).astype(np.uint8)

			temp_img = Image.fromarray(cv2.cvtColor(converted_color_dodge, cv2.COLOR_BGR2RGB))
			black_white_color_dodge = ImageEnhance.Color(ImageOps.invert(temp_img)).enhance(0)
			hue_layer = blendLayers(temp_img, black_white_color_dodge, BlendType.HUE)

			img = blendLayers(img, blendLayers(hue_layer, temp_img, BlendType.NORMAL, 0.7), BlendType.NORMAL, hdr * 2).convert("RGB")

		if sharpness > 0:
			img = ImageEnhance.Sharpness(img).enhance((sharpness+1) * 1.5)

		if noise > 0:
			img = ImageChops.add(img, Image.fromarray(np.random.randint(0, noise * 100, img.size, np.uint8), 'L').resize(img.size).convert(img.mode))

		if vignette > 0:
			mask = Image.new("L", img.size, 0)
			padding = 100 - vignette * 100
			ImageDraw.Draw(mask).ellipse((-padding, -padding, img.size[0] + padding, img.size[1] + padding), fill=255)
			img = Image.composite(img, Image.new("RGB", img.size, "black"), mask.filter(ImageFilter.GaussianBlur(radius=100)))

		img = ImageEnhance.Brightness(img).enhance(1+brightness)

		img = ImageEnhance.Contrast(img).enhance(1+contrast)

		img = np.array(img).astype(np.float32)
		if temperature>0:
			img[:, :, 0] *= 1+temperature
			img[:, :, 1] *= 1+temperature*0.4
		elif temperature<0:
			img[:, :, 2] *= 1-temperature

		img = np.clip(np.power(np.clip(img, 0, 255)/255, gamma), 0, 1)

		hls_img = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
		hls_img[:, :, 2] = np.clip((saturation + 1)*hls_img[:, :, 2], 0, 1)
		img = cv2.cvtColor(hls_img, cv2.COLOR_HLS2RGB)*255

		hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
		hsv_img[:, :, 0] = (hsv_img[:, :, 0]+hue)%360
		img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)

		return Image.fromarray(img.astype(np.uint8), mode="RGB")
