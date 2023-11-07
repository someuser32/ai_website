import g4f


class GPT:
	models = {model.name:model for model in (g4f.models.gpt_35_turbo, g4f.models.gpt_4)}

	def __init__(self):
		pass

	def send(self, text: str, model_name: str, stream: bool=False) -> g4f.CreateResult | str:
		if model_name not in type(self).models:
			raise NameError(f"Model name {model_name} has not found or not loaded yet.")
		return g4f.ChatCompletion.create(model=type(self).models[model_name], messages=[{"role": "User", "content": text}], stream=stream)

	async def async_send(self, text: str, model_name: str) -> str:
		if model_name not in type(self).models:
			raise NameError(f"Model name {model_name} has not found or not loaded yet.")
		return await g4f.ChatCompletion.create_async(model=type(self).models[model_name], messages=[{"role": "User", "content": text}])
