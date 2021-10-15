# py 3 compat
try:
	from urllib.parse import urljoin
except (ModuleNotFoundError, ImportError):
	from urlparse import urljoin

import json
import requests


class TextSynthError(Exception):
	pass


class TextSynth:
	base_url = "https://bellard.org/textsynth/api/v1/"
	engines = (
		"gpt2_345M",
		"Gpt2_1.6B",
		"gptj_6B",
	)

	def __init__(self):
		self.session = self._requests_session()

	def _build_url(self, model):
		return urljoin(self.base_url, "/".join(("engines", model, "completions")))

	def _format_model(self, model):
		model = model.replace(" ", "_").replace("-", "")
		spl = model.split("_")
		return spl[0].lower() + "_" + spl[1]

	def perform_request(
		self,
		prompt,
		temperature=1.0,
		top_k=40,
		top_p=0.9,
		seed=0,
		model="GPTJ_6B",
		stream=True
	):
		# bunch of validation
		## TextSynth is picky about formatting
		model = self._format_model(model)
		if not isinstance(temperature, float):
			temperature = float(temperature)
		if temperature <= 0.1 or temperature > 10.0:
			raise TextSynthError("temperature must be between 0.1 and 10.0")
		if not isinstance(top_k, int):
			top_k = int(top_k)
		if top_k < 1 or top_k > 1000:
			raise TextSynthError("top-k must be between 1 and 1000")
		if not isinstance(top_p, float):
			top_p = float(top_p)
		if top_p <= 0 or top_p > 1:
			raise TextSynthError("top-p must be between 0 and 1")
		if not isinstance(seed, int):
			seed = int(seed)
		if not isinstance(stream, bool):
			stream = bool(stream)
		r = self.session.post(
			self._build_url(model),
			json={
				"prompt": prompt,
				"temperature": temperature,
				"top_k": top_k,
				"top_p": top_p,
				"seed": seed,
				"stream": stream,
			},
			stream=stream,
		)
		r.raise_for_status()
		return r

	def completion_generator(self, prompt, *args, **kwargs):
		req = self.perform_request(prompt, *args, **kwargs)
		for line in req.iter_lines():
			if not line:
				continue
			line = line.decode("utf-8")
			j = json.loads(line)
			yield (j.get("text"), j.get("reached_end"), j.get("total_tokens", 0))

	def complete(self, prompt, **kwargs):
		kwargs["stream"] = False
		req = self.perform_request(prompt, **kwargs)
		return req.json()

	def _requests_session(self):
		session = requests.Session()
		# session.headers["User-Agent"] = "Python TextSynth wrapper"
		return session
