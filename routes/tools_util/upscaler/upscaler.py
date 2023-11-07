import os

import numpy as np
import PIL.Image
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from realesrgan import RealESRGANer


class Upscaler:
	models_info : dict[str, dict[str, tuple[str] | int]] = {
		"RealESRGAN_x4plus": {
			"urls": ("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",),
			"netscale": 4,
			"num_block": 23,
		},
		"RealESRNet_x4plus": {
			"urls": ("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth",),
			"netscale": 4,
			"num_block": 23,
		},
		"RealESRGAN_x4plus_anime_6B": {
			"urls": ("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",),
			"netscale": 4,
			"num_block": 6,
		},
		"RealESRGAN_x2plus": {
			"urls": ("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",),
			"netscale": 2,
			"num_block": 23,
		},
	}

	models : dict[str, RRDBNet] = {}
	upsamplers : dict[str, RealESRGANer] = {}

	model_names : tuple[str] = tuple(models_info.keys())

	def __init__(self):
		pass

	def load_models(self) -> bool:
		if len(type(self).models) > 0:
			return False
		type(self).models = {name: RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=info["num_block"], num_grow_ch=32, scale=info["netscale"]) for name, info in type(self).models_info.items()}
		for model_name, model_info in type(self).models_info.items():
			model_path = os.path.join("weights", f"{model_name}.pth")
			if not os.path.isfile(model_path):
				ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
				for url in model_info["urls"]:
					model_path = load_file_from_url(url=url, model_dir=os.path.join(ROOT_DIR, "weights"), progress=True, file_name=None)
			type(self).upsamplers[model_name] = RealESRGANer(scale=model_info["netscale"], model_path=model_path, dni_weight=None, model=type(self).models[model_name], tile=512, tile_pad=10, pre_pad=0, half=True)
		return True

	def upscale(self, input_img: PIL.Image.Image, outscale: int=4, model_name: str="RealESRGAN_x4plus_anime_6B") -> PIL.Image.Image | None:
		if model_name not in type(self).upsamplers:
			raise NameError(f"Model name {model_name} has not found or not loaded yet.")
		try:
			output_image, _ = type(self).upsamplers[model_name].enhance(np.array(input_img), outscale)
		except RuntimeError:
			return None
		return PIL.Image.fromarray(output_image)
