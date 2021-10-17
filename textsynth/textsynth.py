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
		"gpt2_1558M",
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
		"""Perform the request.
		In almost all cases, you want to use either complete or completion_generator, with any number of the below as keyword arguments.

		args:
			prompt (str): The text you wish to have automatically completed.
				Supposedly has a max length of 4096KB
			temperature (float): Divide the logits (=log(probability) of the tokens) by the temperature value (0.1 <= temperature <= 10). Defaults to 1.0
			top_k (int): Keep only the top-k tokens with the highest probability (1 <= top-k <= 1000). Defaults to 40
			top_p (float): Keep the top tokens having cumulative probability >= top-p (0 < top-p <= 1). Defaults to 0.9
			seed (int): Seed of the random number generator. Use 0 for a random seed. Defaults to 0
			model (str): String representing the model name and number of parameters. Call self.engines for a list.
				note: This is case sensitive

		returns:
			requests.Response
		"""
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

	def completion_generator(self, prompt, **kwargs):
		"""Generator that completes the prompt.
		See self.perform_request for a list of possible keyword arguments.

		returns:
			Generator yielding a tuple of: (text, reached_end, total_tokens).
				note: total_tokens is 0 unless reached_end is True, signifying the end of the computed response
		"""
		req = self.perform_request(prompt, **kwargs)
		for line in req.iter_lines():
			if not line:
				continue
			line = line.decode("utf-8")
			j = json.loads(line)
			yield (j.get("text"), j.get("reached_end"), j.get("total_tokens", 0))

	def complete(self, prompt, **kwargs):
		"""Completes the provided prompt, blocking until a full response has been computed.
		See self.perform_request for a list of possible keyword arguments.

		returns:
			dict: {'text': ..., 'reached_end': True, 'total_tokens': int}
		"""
		kwargs["stream"] = False
		req = self.perform_request(prompt, **kwargs)
		return req.json()

	def _requests_session(self):
		session = requests.Session()
		# session.headers["User-Agent"] = "Python TextSynth wrapper"
		return session
