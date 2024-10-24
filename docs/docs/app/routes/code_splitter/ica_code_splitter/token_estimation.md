# Token Estimation

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [App](../../../index.md#app) / [Routes](../../index.md#routes) / [Code Splitter](../index.md#code-splitter) / [Ica Code Splitter](./index.md#ica-code-splitter) / Token Estimation

> Auto-generated documentation for [app.routes.code_splitter.ica_code_splitter.token_estimation](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/token_estimation.py) module.

- [Token Estimation](#token-estimation)
  - [count_tokens](#count_tokens)
  - [estimate_tokens](#estimate_tokens)

## count_tokens

[Show source in token_estimation.py:101](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/token_estimation.py#L101)

Count the estimated tokens in the specified files.

#### Arguments

- `filepaths` *List[str]* - List of file paths to count tokens for.
- `estimation_method` *str* - The method to estimate the number of tokens. Options are 'average', 'words', 'chars', 'max', 'min'.

#### Returns

- `Dict[str,` *int]* - A dictionary mapping file paths to their estimated token counts.

#### Signature

```python
def count_tokens(filepaths: List[str], estimation_method: str) -> Dict[str, int]: ...
```



## estimate_tokens

[Show source in token_estimation.py:41](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/token_estimation.py#L41)

Estimate the number of tokens in the given text based on the specified method.

The function provides five estimation methods:
1. 'average': Calculates the average of the word-based and character-based token estimates.
              - Word-based estimate: Divides the word count by 0.75 and rounds to the nearest integer.
              - Character-based estimate: Divides the character count by 4.0 and rounds to the nearest integer.
              - The final estimate is the average of the word-based and character-based estimates.
2. 'words': Uses the word-based token estimate.
            - Word-based estimate: Divides the word count by 0.75 and rounds to the nearest integer.
3. 'chars': Uses the character-based token estimate.
            - Character-based estimate: Divides the character count by 4.0 and rounds to the nearest integer.
4. 'max': Takes the maximum of the word-based and character-based token estimates.
5. 'min': Takes the minimum of the word-based and character-based token estimates.

#### Arguments

- `text` *str* - The text to estimate tokens for.
- `method` *str, optional* - The method to use for token estimation. Options are 'average', 'words', 'chars', 'max', 'min'. Default is 'max'.

#### Returns

- `int` - The estimated number of tokens.

#### Raises

- `ValueError` - If an invalid estimation method is provided.

#### Examples

```python
>>> text = "This is a sample text."
>>> estimate_tokens(text, method="average")
5
>>> estimate_tokens(text, method="words")
6
>>> estimate_tokens(text, method="chars")
5
>>> estimate_tokens(text, method="max")
6
>>> estimate_tokens(text, method="min")
5
```

#### Signature

```python
def estimate_tokens(text: str, method: str = "max") -> int: ...
```
