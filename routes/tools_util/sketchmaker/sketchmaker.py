import PIL.Image
import cv2
import numpy as np

class SketchMaker:
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
		img = cv2.cvtColor(np.array(input_img), cv2.COLOR_RGB2GRAY)

		dog = cv2.GaussianBlur(img, (kernel, kernel), sigma) - (gamma-0.001) * cv2.GaussianBlur(img, (kernel, kernel), sigma*k_sigma)
		dog = dog/dog.max()

		e = 1 + np.tanh((phi-0.001) * (dog-(eps-0.001)))
		e[e>=1] = 1

		img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

		if not scale:
			e[e<1] = 0

		return PIL.Image.fromarray((e*255).astype("uint8"))
