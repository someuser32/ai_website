from dataclasses import dataclass, field
from decimal import Decimal

import cv2
import PIL.Image
import numpy as np

class SketchMaker:
	@dataclass()
	class arg_range:
		start : int | float
		stop : int | float
		step : int | float = 1
		default : int | float | None = None
		name : str = ""
		range : tuple[int | float] = field(init=False)

		def __post_init__(self):
			if self.start > self.stop and self.step > 0:
				raise ValueError
			elif self.start < self.stop and self.step < 0:
				raise ValueError
			elif self.start != self.stop and self.step == 0:
				raise ValueError
			if self.default is None:
				self.default = self.start
			range, stop, step = set(), Decimal(str(self.stop)), Decimal(str(self.step))
			i = Decimal(str(self.start))
			while i <= stop:
				range.add(float(i))
				i += step
			self.range = tuple(range)

		def __contains__(self, __key: object) -> bool:
			if not isinstance(__key, (int, float)):
				return False
			return self.start <= __key <= self.stop

	ranges = {
		"kernel": arg_range(0, 25, 1, 0, "Kernel size"),
		"sigma": arg_range(1, 5, 0.05, 1.4, "Sigma"),
		"k_sigma": arg_range(1, 5, 0.05, 1.6, "K Sigma"),
		"eps": arg_range(-0.2, 0.2, 0.005, -0.03, "Epsilon"),
		"phi": arg_range(1, 50, 1, 10, "Phi"),
		"gamma": arg_range(0.75, 1, 0.005, 1, "Gamma"),
	}

	def __init__(self):
		pass

	def sketch(self, input_img: PIL.Image.Image, kernel: int=0, sigma: float=1.4, k_sigma: float=1.6, eps: float=-0.03, phi: int=10, gamma: float=1, scale: bool=False) -> PIL.Image.Image:
		"""
			kernel: 0 - 25 (1)
			sigma: 1 - 5 (0.05)
			k_sigma: 1 - 5 (0.05)
			eps: -0.2 - 0.2 (0.005)
			phi: 1 - 50 (1)
			gamma: 0.75 - 1 (0.005)
		"""
		if kernel % 2 == 0:
			kernel -= 1

		img = cv2.cvtColor(np.array(input_img), cv2.COLOR_RGB2GRAY)

		dog = cv2.GaussianBlur(img, (kernel, kernel), sigma) - (gamma-0.001) * cv2.GaussianBlur(img, (kernel, kernel), sigma*k_sigma)
		dog = dog/dog.max()

		e = 1 + np.tanh((phi-0.001) * (dog-(eps-0.001)))
		e[e>=1] = 1

		img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

		if not scale:
			e[e<1] = 0

		return PIL.Image.fromarray((e*255).astype("uint8"))
