# Code Splitter

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [App](../../../index.md#app) / [Routes](../../index.md#routes) / [Code Splitter](../index.md#code-splitter) / [Ica Code Splitter](./index.md#ica-code-splitter) / Code Splitter

> Auto-generated documentation for [app.routes.code_splitter.ica_code_splitter.code_splitter](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/code_splitter.py) module.

- [Code Splitter](#code-splitter)
  - [code_splitter](#code_splitter)

## code_splitter

[Show source in code_splitter.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/code_splitter.py#L54)

Split the provided source code into chunks based on a maximum token limit and logical structures.

This function uses the Tree-sitter library to parse the source code and identify logical structures
such as functions, classes, and nested code blocks. It then splits the code into chunks, aiming to
keep related code together within the token limit constraints.

#### Arguments

- `code` *str* - The source code to be split.
- `filepath` *str* - The path to the source code file.
- `output_dir` *str* - The output directory for the generated chunks and headers file.
- `language_str` *Optional[str]* - The programming language of the source code. If not provided, the language is detected based on the file extension.
- `max_tokens` *int* - The maximum number of tokens allowed per chunk.
- `estimation_method` *str* - The method to estimate the number of tokens. Options are 'average', 'words', 'chars', 'max', 'min'.
- `preprocess` *bool* - Whether to preprocess the code to remove comments and extra newlines/spaces.

#### Returns

- `Tuple[List[str],` *List[str]]* - A tuple containing a list of code chunks, where each chunk is a string containing a portion of the source code, and a list of headers extracted from the code.

#### Raises

- `ValueError` - If the programming language is not specified and cannot be detected from the file extension.

#### Signature

```python
def code_splitter(
    code: str,
    filepath: str,
    output_dir: str,
    language_str: Optional[str],
    max_tokens: int,
    estimation_method: str,
    preprocess: bool,
) -> (List[str], List[str]): ...
```
