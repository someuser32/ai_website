import io

import torch


class STT():
	languages = ("en", "de", "es", "ua")

	models = {}

	def __init__(self):
		self.device = torch.device("cuda")
		torch._C._jit_set_profiling_mode(False)
		torch.set_num_threads(4)

	def load_models(self) -> bool:
		if len(type(self).models) > 0:
			return False
		for language in type(self).languages:
			type(self).models[language] = torch.hub.load(repo_or_dir="snakers4/silero-models", model="silero_stt", language=language, device=self.device)
		return True

	def read_text(self, audio: io.BytesIO, language: str="en") -> str:
		if language not in type(self).models:
			raise NameError(f"Language {language} has not found or not loaded yet.")

		model, decoder, utils = type(self).models[language]
		read_audio, prepare_model_input = utils[2:]

		return "".join(decoder(i.cuda()) for i in model(prepare_model_input((read_audio(audio),), device=self.device)))
