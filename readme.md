# Textsynth

This is a convenient wrapper over [TextSynth](https://bellard.org/textsynth/).

Essentially, it provides randomly chosen text completion backed by GPT-2 and GPT-J transformer based language models. This wrapper exists to facilitate integration in a variety of Python applications.

## Usage

```
>>> from textsynth import TextSynth
>>> synth = TextSynth()
```

From this point, you have two choices depending on whether you care to receive each token as it gets generated in realtime.

If you do, you can call `synth.completion_generator()` as such:

```
generator = synth.completion_generator("Python is my favorite language")
for (text, reached_end, total_tokens) in generator:
	print(text)
	if reached_end:
		# todo: total_tokens is 0 until reached_end=True
		print(f"{total_tokens} tokens processed, end of output")
```

Otherwise, just call `synth.complete()`, wait, and interact with the JSON.

```
# try to get the model to spit out python code
>>> response = synth.complete("import sys, os")
>>> print(response)
# trimmed
{'text': 'import caffe\nimport caffe.io\nfrom caffe import layers as L\nfrom caffe.io import imagenet_io\nfrom keras import backend as K\nfrom keras.layers import Dense\nfrom keras.models import Model\nimport keras_model_utils\nimport numpy as np...', 'reached_end': True, 'total_tokens': 204}
```

# Licensing

TextSynth is the work of [Fabrice Bellard](https://bellard.org/). I simply got intrigued by the implications of GPT-2 and other coherent language models. All credit is his.

This code is released into the public domain (CC0 because Github).
