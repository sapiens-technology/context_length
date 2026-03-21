Benchmarking algorithm for testing language model context windows.

# Context Length - Benchmarking

This algorithm implements a synthetic data generator for language model benchmarking, with a specific focus on **handling long contexts and inserted noise**.

The workflow operates in clearly defined steps.

First, the `generateDatabase` method reads a text file (`bible.txt`) that serves as the base content. This text is then adjusted to have exactly the desired number of tokens (`n_tokens`) using the internal `_adjust_text_tokens` function, which relies on the `cl100k_base` tokenizer from the `tiktoken` library. If the original text has more tokens than needed, it is truncated; if it has fewer, it is repeated until the target token count is reached. This ensures precise control over context length, which is essential for LLM testing.

Next, the text is split into words. For each sample (`n_samples`), the algorithm creates an independent copy of this word list and randomly inserts a four-digit number (the "intruder") at a random position in the text. This number does not belong to the original content and is intentionally added as noise.

The text is then reconstructed and formatted as an input problem. The associated task is straightforward in description but challenging in practice: the model must identify which number in the text does not belong.

The algorithm generates four multiple-choice alternatives (A, B, C, D). One alternative contains the correct inserted number, while the other three are distinct random numbers. Alternatives are shuffled and then alphabetically sorted for consistent formatting. Each dataset entry contains the `input` (text + question + alternatives) and the `output` (correct alternative).

The usefulness of this algorithm in language model evaluation is significant:

* It tests **long-context attention**, since the model must analyze thousands of tokens.
* It evaluates **anomaly detection**, identifying an element that does not fit the text.
* It measures **distributed information retention**, as the intruder number can appear anywhere.
* It allows precise difficulty control by adjusting text length (`n_tokens`) and the number of samples.

In practice, this benchmark is similar to the "needle in a haystack" problem, where the model must locate a specific detail amid a large amount of irrelevant information.

In short, the algorithm provides a controlled, scalable environment to test real limitations of language models, especially in tasks requiring memory, attention, and robustness to noise.

## Installation

Use the package manager [pip](https://pypi.org/project/context-length/) to install Context Length - Benchmarking.

```bash
pip install context-length
```

If you have a problem with one or more dependencies, you can install them manually via the requirements file.

```bash
pip install -r requirements.txt
```

## Usage
Basic usage example:
```python
from context_length import ContextLength
context_length = ContextLength()

return_dictionary = context_length.generateDatabase(n_samples=2, n_tokens=100)
print('-'*150)
for data in return_dictionary['data']:
	print('INPUT:')
	print(data['input'])
	print()
	print('OUPUT:')
	print(data['output'])
	print('-'*150)

```
```bash
------------------------------------------------------------------------------------------------------------------------------------------------------
INPUT:
txt
	1:1 In the beginning God created the heaven and the earth.
	
	1:2 And the earth was without form, and void; and darkness was upon
	the face of the deep. And the Spirit of God moved upon the face 1047 of the
	waters.
	
	1:3 And God said, Let there be light: and there was light.
	
	1:4 And God saw the light, that it was good: and God divided the light
	from the darkness.
	
	1:5 And God called the

The presented text contains a number that doesn't make sense somewhere among the words. What number is that?

A) 3002
B) 7654
C) 1047
D) 9893

OUPUT:
C) 1047
------------------------------------------------------------------------------------------------------------------------------------------------------
INPUT:
txt
	1:1 In the beginning God created the heaven and the earth.
	
	1:2 And the earth was without form, and void; and darkness was upon
	the face of the deep. And the Spirit of God moved upon the face of the
	waters.
	
	1:3 And God said, Let there be light: and there was light.
	
	1:4 And God saw the light, that it was good: and God divided the light
	from the darkness.
	
	1:5 And 5472 God called the

The presented text contains a number that doesn't make sense somewhere among the words. What number is that?

A) 3828
B) 5472
C) 1661
D) 7754

OUPUT:
B) 5472
------------------------------------------------------------------------------------------------------------------------------------------------------
```

## ContextLength

```python
from context_length import ContextLength # import of the main class for accessing the module's resources
context_length = ContextLength( # construction of the main class of the module
	show_errors=True, # if True, displays a summarized error message when an error occurs; if False, does not display any error message (default value: True)
	display_error_point=False # if True, displays the error details when "show_errors" is enabled; if False, does not display the error details (default value: False)
) # returns the instantiation of the class object
if context_length: print('Context Length class SUCCESSFULLY created!')
else: print('ERROR creating the Context Length class.')

```
```bash
Context Length class SUCCESSFULLY created!
```
```python
from context_length import ContextLength
context_length = ContextLength()

if context_length: print('Context Length class SUCCESSFULLY created!')
else: print('ERROR creating the Context Length class.')

```
```bash
Context Length class SUCCESSFULLY created!
```

## generateDatabase

```python
from context_length import ContextLength
context_length = ContextLength()

return_dictionary = context_length.generateDatabase( # creates a dataset with pairs of multiple-choice questions and their respective correct answers
	n_samples=5, # integer number indicating the desired number of questions-answers pairs (default value: 10)
	n_tokens=200 # integer number representing the desired quantity of tokens in each text to be analyzed (default value: 10000)
) # returns a dictionary with the number of input/output pairs defined in the "n_samples" parameter
# the returned dictionary will have a key named "data" with a list of dictionaries containing the keys "input" and "output"
# the "input" key, with a string value, will contain the text with the number of tokens defined in "n_tokens" and the question with the answer choices (in english)
# the "output" key, with a string value, will contain the answer with the correct option
# the question text will contain a random four-digit integer inserted at a random position in the text; the model's task is to guess what that number is
# the correct alternative will be in a random option among the alternatives a, b, c, or d
# there is no limit to the number of samples to be generated (all of them will be generated randomly)
# the tested language model must not contain the samples generated in its training or fine-tuning data for the test to be reliable
print('-'*150)
for data in return_dictionary['data']:
	print('INPUT:')
	print(data['input'])
	print()
	print('OUPUT:')
	print(data['output'])
	print('-'*150)

```
```basg
------------------------------------------------------------------------------------------------------------------------------------------------------
INPUT:
txt
	1:1 In the beginning God created the heaven and the earth.
	
	1:2 And the earth was without form, and void; and darkness was upon
	the face of the deep. And the Spirit of God moved upon the face of the
	waters.
	
	1:3 And God said, Let there be light: and there was light.
	
	1:4 And God saw the light, that it was good: and God divided the light
	from the darkness.
	
	1:5 And God called the light Day, and the darkness he called Night.
	And the evening and the morning were the first 4730 day.
	
	1:6 And God said, Let there be a firmament in the midst of the waters,
	and let it divide the waters from the waters.
	
	1:7 And God made the firmament, and divided the waters which were
	under the firmament from the waters which were above the firmament:
	and it was so.
	
	1:8 And God called the firmament Heaven. And the

The presented text contains a number that doesn't make sense somewhere among the words. What number is that?

A) 8513
B) 4547
C) 4730
D) 8190

OUPUT:
C) 4730
------------------------------------------------------------------------------------------------------------------------------------------------------
INPUT:
txt
	1:1 In the beginning God created the heaven and the earth.
	
	1:2 And the earth was without form, and void; and darkness was upon
	the face of the deep. And the Spirit of God moved upon the face of the
	waters.
	
	1:3 And God said, Let there be light: and there was light.
	
	1:4 And God saw the light, that it was good: and God divided the 2364 light
	from the darkness.
	
	1:5 And God called the light Day, and the darkness he called Night.
	And the evening and the morning were the first day.
	
	1:6 And God said, Let there be a firmament in the midst of the waters,
	and let it divide the waters from the waters.
	
	1:7 And God made the firmament, and divided the waters which were
	under the firmament from the waters which were above the firmament:
	and it was so.
	
	1:8 And God called the firmament Heaven. And the

The presented text contains a number that doesn't make sense somewhere among the words. What number is that?

A) 6934
B) 4440
C) 9806
D) 2364

OUPUT:
D) 2364
------------------------------------------------------------------------------------------------------------------------------------------------------
INPUT:
txt
	1:1 In the beginning God created the heaven and the earth.
	
	1:2 And the earth was without form, and void; and darkness was upon
	the face of the deep. And the Spirit of God moved upon the face of the
	waters.
	
	1:3 And God said, Let there be light: and there was light.
	
	1:4 And God saw the light, that it was good: and God divided the light
	from the darkness.
	
	1:5 And God called the light 2341 Day, and the darkness he called Night.
	And the evening and the morning were the first day.
	
	1:6 And God said, Let there be a firmament in the midst of the waters,
	and let it divide the waters from the waters.
	
	1:7 And God made the firmament, and divided the waters which were
	under the firmament from the waters which were above the firmament:
	and it was so.
	
	1:8 And God called the firmament Heaven. And the

The presented text contains a number that doesn't make sense somewhere among the words. What number is that?

A) 2780
B) 2341
C) 1109
D) 9295

OUPUT:
B) 2341
------------------------------------------------------------------------------------------------------------------------------------------------------
INPUT:
txt
	1:1 In the beginning God created the heaven and the earth.
	
	1:2 And the earth was without form, and void; and darkness was upon
	the face of the deep. And the Spirit of God moved upon the face of the
	waters.
	
	1:3 And God said, Let there be light: and there was light.
	
	1:4 And God saw the light, that it was good: and God divided the light
	from the darkness.
	
	1:5 And God called the light Day, and the darkness he called Night.
	And the evening and the morning were the first day.
	
	1:6 And God said, Let there be a firmament in the midst of the waters,
	and let it divide the waters from the waters.
	
	1:7 And God made the firmament, and divided the waters which were
	under the firmament from the waters which were above the firmament:
	and it was so.
	
	1:8 And God called the firmament 6480 Heaven. And the

The presented text contains a number that doesn't make sense somewhere among the words. What number is that?

A) 1253
B) 9865
C) 2647
D) 6480

OUPUT:
D) 6480
------------------------------------------------------------------------------------------------------------------------------------------------------
INPUT:
txt
	1:1 In the beginning God created the heaven and the earth.
	
	1:2 And the earth was without form, and void; and darkness was upon
	the face of the deep. And the Spirit of God moved upon the face of the
	waters.
	
	1:3 And God said, Let there be light: and there was light.
	
	1:4 And God saw the light, that it was good: and God divided the light
	from the darkness.
	
	1:5 And God called the light Day, and the darkness he called Night.
	And the evening and the morning were the first day.
	
	1:6 And God said, Let there be a firmament in the midst of the waters,
	and let it divide the waters from the waters.
	
	1:7 And God made the firmament, and divided the waters which were
	under the firmament from 9097 the waters which were above the firmament:
	and it was so.
	
	1:8 And God called the firmament Heaven. And the

The presented text contains a number that doesn't make sense somewhere among the words. What number is that?

A) 9914
B) 9097
C) 1564
D) 4700

OUPUT:
B) 9097
------------------------------------------------------------------------------------------------------------------------------------------------------
```
```python
from context_length import ContextLength
context_length = ContextLength()

return_dictionary = context_length.generateDatabase(5, 200)
print(return_dictionary)

```
```bash
{'data': [{'output': 'B) 3270', 'input': "```txt\n1:1 In the beginning God created the heaven and the earth.\n\n1:2 And the earth was without form, and void; and darkness was upon\nthe face of the deep. And the Spirit of God moved upon the face of the\nwaters.\n\n1:3 And God said, Let there be light: and there was light.\n\n1:4 And God saw the light, that it was good: and God divided the light\nfrom the darkness.\n\n1:5 And God called the light Day, and the darkness he called Night.\nAnd the evening and the morning were the first day.\n\n1:6 And God said, Let there be a firmament in the midst of the waters,\nand let it divide the waters from the 3270 waters.\n\n1:7 And God made the firmament, and divided the waters which were\nunder the firmament from the waters which were above the firmament:\nand it was so.\n\n1:8 And God called the firmament Heaven. And the\n```\n\nThe presented text contains a number that doesn't make sense somewhere among the words. What number is that?\n\nA) 2370\nB) 3270\nC) 9833\nD) 8211"}, {'output': 'A) 2534', 'input': "```txt\n1:1 In the beginning God created the heaven and the earth.\n\n1:2 And the earth was without form, and void; and darkness was upon\nthe face of the 2534 deep. And the Spirit of God moved upon the face of the\nwaters.\n\n1:3 And God said, Let there be light: and there was light.\n\n1:4 And God saw the light, that it was good: and God divided the light\nfrom the darkness.\n\n1:5 And God called the light Day, and the darkness he called Night.\nAnd the evening and the morning were the first day.\n\n1:6 And God said, Let there be a firmament in the midst of the waters,\nand let it divide the waters from the waters.\n\n1:7 And God made the firmament, and divided the waters which were\nunder the firmament from the waters which were above the firmament:\nand it was so.\n\n1:8 And God called the firmament Heaven. And the\n```\n\nThe presented text contains a number that doesn't make sense somewhere among the words. What number is that?\n\nA) 2534\nB) 7680\nC) 8103\nD) 6209"}, {'output': 'C) 8367', 'input': "```txt\n1:1 In the beginning God created the heaven and the earth.\n\n1:2 And the earth was without form, and void; and darkness was upon\nthe face of the deep. And the Spirit of God moved upon the face of the\nwaters.\n\n1:3 And God said, Let there be light: and there was light.\n\n1:4 And God saw the light, that it was good: and God divided the light\nfrom the darkness.\n\n1:5 And God called the light Day, and the darkness he called Night.\nAnd the evening and the morning were the first day.\n\n1:6 And God said, Let there be a firmament in the midst of the waters,\nand let it divide the waters from the waters.\n\n1:7 And God made the firmament, and divided the waters which were\nunder the firmament from the waters which were above the firmament:\nand it was so.\n\n1:8 8367 And God called the firmament Heaven. And the\n```\n\nThe presented text contains a number that doesn't make sense somewhere among the words. What number is that?\n\nA) 9151\nB) 9473\nC) 8367\nD) 1897"}, {'output': 'A) 7563', 'input': "```txt\n1:1 In the beginning God created the heaven and the earth.\n\n1:2 And the earth was without form, and void; and darkness was upon\nthe face of the deep. And the Spirit of God moved upon the face of the\nwaters.\n\n1:3 And God said, Let there be light: and there was light.\n\n1:4 And God saw the light, that it was good: and God divided the light\nfrom the darkness.\n\n1:5 And God called the light Day, and the darkness he called Night.\nAnd the evening and the morning were the first day.\n\n1:6 And God said, Let there be a firmament in the midst of the waters,\nand let it divide the waters from the waters.\n\n1:7 And God made the firmament, and divided the waters which were\nunder the firmament from the waters which were above the firmament:\nand it was so.\n\n1:8 And God called the 7563 firmament Heaven. And the\n```\n\nThe presented text contains a number that doesn't make sense somewhere among the words. What number is that?\n\nA) 7563\nB) 8287\nC) 3596\nD) 8741"}, {'output': 'D) 2776', 'input': "```txt\n1:1 In the beginning God created the heaven and the earth.\n\n1:2 And the earth was without form, and void; and darkness was upon\nthe face of the deep. And the Spirit of God moved upon the face of the\nwaters.\n\n1:3 And God said, Let there be light: and there was light.\n\n1:4 And God saw the light, that it was good: and God divided the light\nfrom the darkness.\n\n1:5 And God called the light Day, and the darkness he called Night.\nAnd the evening and the morning were the first day.\n\n1:6 And God said, Let there be a firmament in the midst of the waters,\nand let it divide the waters from the waters.\n\n1:7 And God made the firmament, 2776 and divided the waters which were\nunder the firmament from the waters which were above the firmament:\nand it was so.\n\n1:8 And God called the firmament Heaven. And the\n```\n\nThe presented text contains a number that doesn't make sense somewhere among the words. What number is that?\n\nA) 7764\nB) 2918\nC) 3576\nD) 2776"}]}
```
```python
from context_length import ContextLength
context_length = ContextLength()

n_samples = 100
n_tokens = 500
return_dictionary = context_length.generateDatabase(n_samples, n_tokens)
print('main key:', list(return_dictionary.keys()))
print('keys of pairs:', list(return_dictionary['data'][0].keys()))
print('generated pairs:', len(return_dictionary['data']))

```
```bash
main key: ['data']
keys of pairs: ['output', 'input']
generated pairs: 100
```

## Saving the dataset to a JSON file.

```python
from context_length import ContextLength
context_length = ContextLength()

def save_dictionary_to_json(return_dictionary={}, file_path=''):
	from json import dump
	from os.path import exists
	with open(file_path, 'w', encoding='utf-8') as file: dump(return_dictionary, file, ensure_ascii=False, indent=4)
	return exists(file_path)

n_samples = 1000
n_tokens = 10000
file_path = f'./{n_samples}_samples.json'
return_dictionary = context_length.generateDatabase(n_samples, n_tokens)
saved_json = save_dictionary_to_json(return_dictionary=return_dictionary, file_path=file_path)
if saved_json: print(f'File "{file_path}" saved SUCCESSFULLY!')
else: print('ERROR saving the JSON file.')

```
```bash
File "./1000_samples.json" saved SUCCESSFULLY!
```

Copyright [2026] [Sapiens Technology®️]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
