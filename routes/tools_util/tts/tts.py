import io
import os
import re
from typing import Any

import num2words
import torch
import torch.package
import torchaudio
from pydub import AudioSegment


class VoiceMod():
	def __init__(self):
		pass

	def pitch(self, audio: io.BytesIO, pitch_shift: int) -> io.BytesIO:
		audio_segment = AudioSegment.from_file(audio, format="wav")
		modified_audio_segment = audio_segment._spawn(audio_segment.raw_data, overrides={"frame_rate": audio_segment.frame_rate + int(pitch_shift * 100)})
		modified_audio_segment = modified_audio_segment.set_frame_rate(audio_segment.frame_rate)
		modified_audio = io.BytesIO()
		modified_audio_segment.export(modified_audio, format="wav")
		modified_audio.seek(0)
		return modified_audio


class TTS():
	models_infos = {
		"v4_ru": {
			"url": "https://models.silero.ai/models/tts/ru/v4_ru.pt",
			"language": "ru",
			"samples": {
				"baya": ("Привет, мир!",),
			},
		},
		"v4_cyrillic": {
			"url": "https://models.silero.ai/models/tts/cyr/v4_cyrillic.pt",
			"speakers_languages": {
				"b_ava": "Avar",
				"b_bashkir": "Bashkir",
				"b_bulb": "Bulgarian",
				"b_bulc": "Bulgarian",
				"b_che": "Chechen",
				"b_cv": "Chuvash",
				"cv_ekaterina": "Chuvash",
				"b_myv": "Erzya",
				"b_kalmyk": "Kalmyk",
				"b_krc": "Karachay-Balkar",
				"kz_M1": "kz",
				"kz_M2": "kz",
				"kz_F3": "kz",
				"kz_F1": "kz",
				"kz_F2": "kz",
				"b_kjh": "Khakas",
				"b_kpv": "Komi-Ziryan",
				"b_lez": "Lezghian",
				"b_mhr": "Mari",
				"b_mrj": "Mari High",
				"b_nog": "Nogai",
				"b_oss": "Ossetic",
				"b_ru": "ru",
				"b_tat": "Tatar",
				"marat_tt": "Tatar",
				"b_tyv": "Tuvinian",
				"b_udm": "Udmurt",
				"b_uzb": "Uzbek",
				"b_sah": "Yakut",
				"kalmyk_erdni": "Kalmyk",
				"kalmyk_delghir": "Kalmyk",
			},
			"samples": {
				"b_ru": ("Привет, мир!",),
			},
		},
		"v4_ua": {
			"url": "https://models.silero.ai/models/tts/ua/v4_ua.pt",
			"language": "ua",
			"samples": {
				"mykyta": ("Привіт, світ!",),
			},
		},
		"v4_uz": {
			"url": "https://models.silero.ai/models/tts/uz/v4_uz.pt",
			"language": "uz",
			"samples": {
				"dilnavoz": ("Salom, dunyo!",),
			},
		},
		"v3_en": {
			"url": "https://models.silero.ai/models/tts/en/v3_en.pt",
			"language": "en",
			"samples": {
				"en_0": ("Hello, world!",),
			},
		},
	}

	models : dict[str, Any] = {} # NOTE: typehintings are not avaiable for <class '<torch_package_0>.multi_acc_v3_package.TTSModelMultiAcc_v3'>
	models_speakers : dict[str, list[str]] = {}

	model_names : tuple[str] = tuple(models_infos.keys())

	supported_num2words = ("ru", "kz", "ua", "uz", "en")

	def __init__(self):
		torch._C._jit_set_profiling_mode(False)
		torch.set_num_threads(4)

	def get_speaker_language(self, model_name: str, speaker: str | None = None) -> str | None:
		if model_name not in type(self).models_infos:
			return None
		if language := type(self).models_infos[model_name].get("language"):
			return language
		if speakers_list := type(self).models_infos[model_name].get("speakers_languages"):
			if language := speakers_list.get(speaker):
				return language
		return None

	def load_models(self) -> bool:
		if len(type(self).models) > 0:
			return False
		ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
		if not os.path.exists(os.path.join(ROOT_DIR, "models")):
			os.mkdir(os.path.join(ROOT_DIR, "models"))
		for model_name, model_info in type(self).models_infos.items():
			model_path = os.path.join(ROOT_DIR, "models", f"{model_name}.pt")
			if not os.path.isfile(model_path):
				torch.hub.download_url_to_file(model_info["url"], model_path)
			type(self).models[model_name] = torch.package.PackageImporter(model_path).load_pickle("tts_models", "model")
			type(self).models[model_name].to(torch.device("cuda"))
			type(self).models_speakers[model_name] = [speaker for speaker in type(self).models[model_name].speakers if speaker != "random"]

			# for some reason it works slowly first time
			# we need to "prepare" models before "fast-usage"
			for speaker, samples in model_info.get("samples", {}).items():
				for sample in samples:
					self.create_audio(model_name=model_name, speaker=speaker, text=sample)
		return True

	def create_audio(self, model_name: str, speaker: str, text: str) -> io.BytesIO:
		if model_name not in type(self).models:
			raise NameError(f"Model name {model_name} has not found or not loaded yet.")
		elif speaker not in type(self).models_speakers.get(model_name, {}):
			raise NameError(f"Speaker {speaker} is not avaiable for model {model_name}. Avaiable speakers: {type(self).models_speakers.get(model_name, {})}")
		tts_audio : torch.Tensor = type(self).models[model_name].apply_tts(text=text, speaker=speaker, sample_rate=48000, put_accent=True, put_yo=True)
		audio = io.BytesIO()
		torchaudio.save(audio, tts_audio.unsqueeze(0), sample_rate=48000, format="wav")
		audio.seek(0)
		return audio

	def format_numbers(self, text: str, language: str) -> str:
		language_transformations = {
			"ua": "uk",
		}
		lang = language_transformations.get(language, language)
		if lang not in num2words.CONVERTER_CLASSES:
			return text
		return re.sub(r"\d+", lambda match: num2words.num2words(int(match.group()), lang=lang), text)
