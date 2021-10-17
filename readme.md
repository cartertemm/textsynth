# Textsynth

This is a convenient wrapper over [TextSynth](https://bellard.org/textsynth/).

Essentially, it provides randomly chosen text completion backed by GPT-2 and GPT-J transformer based language models. This wrapper exists to facilitate integration in a variety of Python applications. Perfect for those wanting a little fun, but lacking the resources or not invested enough to set up the stack.

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

There are parameters you can use to fine tune your responses. For instance, you can change the model (gptj_6B is the best and default):

```
>>> synth.engines
('gpt2_345M', 'gpt2_1558M', 'gptj_6B')
>>> response = synth.complete("In an interview today, the president told a reporter that ", model="Gpt2_1.6B")
# trimmed
>>> print(response.get("text"))
 "I told President Putin at a meeting, I said, 'You're cyber-invading us.' . . . He said, I'm not going to do that.'"
"He didn't do it. And I really believe that when he tells me that, he means it."
>>>
```

An attempt has been made to document these parameters (to some extent at least) in the code. Play around with them for the best and most amusing results.

# Licensing

TextSynth is the work of [Fabrice Bellard](https://bellard.org/). I simply got intrigued by the implications of GPT-2 and other coherent language models. All credit is his.

This code is released into the public domain (CC0 because Github).
