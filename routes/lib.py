import base64
import random
import string

from captcha.image import ImageCaptcha
from fastapi import Request

chars = tuple(string.ascii_letters+string.digits)

def generate_captcha(request: Request, width: int, height: int) -> tuple[str, str]:
	text = "".join(random.choice(chars) for _ in range(4))
	img = ImageCaptcha(width=width, height=height).generate(text)
	captcha = f"data:image/png;base64,{base64.b64encode(img.read()).decode('utf-8')}"
	request.session["captcha"] = text
	return (text, captcha)

def check_captcha(request: Request, answer: str) -> bool:
	valid = request.session.get("captcha") == answer
	if "captcha" in request.session:
		del request.session["captcha"]
	return valid
