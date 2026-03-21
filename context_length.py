"""
This algorithm implements a synthetic data generator for language model benchmarking,
with a specific focus on **handling long contexts and inserted noise**.

The workflow operates in clearly defined steps.

First, the `generateDatabase` method reads a text file (`bible.txt`) that serves as the base content.
This text is then adjusted to have exactly the desired number of tokens (`n_tokens`) using the internal `_adjust_text_tokens` function,
which relies on the `cl100k_base` tokenizer from the `tiktoken` library. If the original text has more tokens than needed, it is truncated;
if it has fewer, it is repeated until the target token count is reached.
This ensures precise control over context length, which is essential for LLM testing.

Next, the text is split into words. For each sample (`n_samples`),
the algorithm creates an independent copy of this word list and randomly inserts a four-digit number (the "intruder") at a random position in the text.
This number does not belong to the original content and is intentionally added as noise.

The text is then reconstructed and formatted as an input problem.
The associated task is straightforward in description but challenging in practice: the model must identify which number in the text does not belong.

The algorithm generates four multiple-choice alternatives (A, B, C, D).
One alternative contains the correct inserted number, while the other three are distinct random numbers.
Alternatives are shuffled and then alphabetically sorted for consistent formatting.
Each dataset entry contains the `input` (text + question + alternatives) and the `output` (correct alternative).

The usefulness of this algorithm in language model evaluation is significant:

* It tests **long-context attention**, since the model must analyze thousands of tokens.
* It evaluates **anomaly detection**, identifying an element that does not fit the text.
* It measures **distributed information retention**, as the intruder number can appear anywhere.
* It allows precise difficulty control by adjusting text length (`n_tokens`) and the number of samples.

In practice, this benchmark is similar to the "needle in a haystack" problem,
where the model must locate a specific detail amid a large amount of irrelevant information.

In short, the algorithm provides a controlled, scalable environment to test real limitations of language models,
especially in tasks requiring memory, attention, and robustness to noise.
"""
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
class ContextLength:
	def __init__(self, show_errors=True, display_error_point=False):
		try:
			self.__show_errors = bool(show_errors) if type(show_errors) in (bool, int, float) else True
			self.__display_error_point = bool(display_error_point) if type(display_error_point) in (bool, int, float) else False
			try:
				from warnings import simplefilter, filterwarnings
				from logging import disable, CRITICAL
				from os import environ
				simplefilter('ignore')
				filterwarnings('ignore')
				disable(CRITICAL)
			except: pass
			from traceback import print_exc
			self.__print_exc = print_exc
		except Exception as error:
			try:
				if self.__show_errors:
					error_message = 'ERROR in ContextLength.__init__: '+str(error)
					print(error_message)
					try: self.__print_exc() if self.__display_error_point else None
					except: pass
			except: pass
	def generateDatabase(self, n_samples=10, n_tokens=10000):
		try:
			return_dictionary, database = {}, []
			n_samples = max(1, int(n_samples)) if type(n_samples) in (int, float) else 10
			n_tokens = max(1, int(n_tokens)) if type(n_tokens) in (int, float) else 10000
			def _adjust_text_tokens(bible_string='', n_tokens=10000):
				from tiktoken import get_encoding
				encoding = get_encoding('cl100k_base')
				tokens = encoding.encode(bible_string)
				total_tokens = len(tokens)
				if n_tokens == total_tokens: return bible_string
				if n_tokens < total_tokens: return encoding.decode(tokens[:n_tokens])
				repeated_tokens = []
				while len(repeated_tokens) < n_tokens: repeated_tokens.extend(tokens)
				return encoding.decode(repeated_tokens[:n_tokens])
			bible_string = ''
			with open('bible.txt', 'r', encoding='utf-8') as file: bible_string = str(file.read()).strip()
			bible_string = _adjust_text_tokens(bible_string=bible_string, n_tokens=n_tokens)
			from copy import deepcopy
			bible_words = bible_string.split(chr(32))
			original_bible_words = deepcopy(bible_words)
			words_length = len(bible_words)
			def _shuffle_list(input_list=[]):
			    from random import shuffle
			    shuffle(input_list)
			    return input_list
			from random import randint
			alternatives = ['A)', 'B)', 'C)', 'D)']
			for _ in range(n_samples):
				bible_words = deepcopy(original_bible_words)
				random_index = randint(0, words_length)
				intruder = str(randint(1000, 9999))
				bible_words.insert(random_index, intruder)
				bible_string = chr(32).join(bible_words)
				formatted_input = f"```txt\n{bible_string}\n```\n\nThe presented text contains a number that doesn't make sense somewhere among the words. What number is that?"
				alternative_answers, input_output, used_values = [], {}, set()
				for index, alternative in enumerate(_shuffle_list(input_list=alternatives)):
					if index == 0:
						correct_alternative = f'{alternative} {intruder}'
						alternative_answers.append(correct_alternative)
						input_output['output'] = correct_alternative
						used_values.add(intruder)
					else:
						while True:
							wrong_answer = str(randint(1000, 9999))
							if wrong_answer not in used_values:
								used_values.add(wrong_answer)
								string_wrong_answer = f'{alternative} {wrong_answer}'
								alternative_answers.append(string_wrong_answer)
								break
				_input = f'{formatted_input}\n\n'
				alternative_answers = sorted(alternative_answers)
				for alternative_answer in alternative_answers: _input += f'{alternative_answer}\n'
				input_output['input'] = _input.strip()
				database.append(input_output)
			return_dictionary['data'] = database
			return return_dictionary
		except Exception as error:
			try:
				if self.__show_errors:
					error_message = 'ERROR in ContextLength.generateDatabase: '+str(error)
					print(error_message)
					try: self.__print_exc() if self.__display_error_point else None
					except: pass
			except: pass
			return {'data': []}
"""
This algorithm implements a synthetic data generator for language model benchmarking,
with a specific focus on **handling long contexts and inserted noise**.

The workflow operates in clearly defined steps.

First, the `generateDatabase` method reads a text file (`bible.txt`) that serves as the base content.
This text is then adjusted to have exactly the desired number of tokens (`n_tokens`) using the internal `_adjust_text_tokens` function,
which relies on the `cl100k_base` tokenizer from the `tiktoken` library. If the original text has more tokens than needed, it is truncated;
if it has fewer, it is repeated until the target token count is reached.
This ensures precise control over context length, which is essential for LLM testing.

Next, the text is split into words. For each sample (`n_samples`),
the algorithm creates an independent copy of this word list and randomly inserts a four-digit number (the "intruder") at a random position in the text.
This number does not belong to the original content and is intentionally added as noise.

The text is then reconstructed and formatted as an input problem.
The associated task is straightforward in description but challenging in practice: the model must identify which number in the text does not belong.

The algorithm generates four multiple-choice alternatives (A, B, C, D).
One alternative contains the correct inserted number, while the other three are distinct random numbers.
Alternatives are shuffled and then alphabetically sorted for consistent formatting.
Each dataset entry contains the `input` (text + question + alternatives) and the `output` (correct alternative).

The usefulness of this algorithm in language model evaluation is significant:

* It tests **long-context attention**, since the model must analyze thousands of tokens.
* It evaluates **anomaly detection**, identifying an element that does not fit the text.
* It measures **distributed information retention**, as the intruder number can appear anywhere.
* It allows precise difficulty control by adjusting text length (`n_tokens`) and the number of samples.

In practice, this benchmark is similar to the "needle in a haystack" problem,
where the model must locate a specific detail amid a large amount of irrelevant information.

In short, the algorithm provides a controlled, scalable environment to test real limitations of language models,
especially in tasks requiring memory, attention, and robustness to noise.
"""
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
