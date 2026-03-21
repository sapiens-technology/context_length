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
