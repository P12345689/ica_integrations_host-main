# Utils

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [App](../../../index.md#app) / [Routes](../../index.md#routes) / [Code Splitter](../index.md#code-splitter) / [Ica Code Splitter](./index.md#ica-code-splitter) / Utils

> Auto-generated documentation for [app.routes.code_splitter.ica_code_splitter.utils](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/utils.py) module.

- [Utils](#utils)
  - [extract_signature](#extract_signature)
  - [get_language_comment](#get_language_comment)
  - [load_language_mappings](#load_language_mappings)

## extract_signature

[Show source in utils.py:98](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/utils.py#L98)

Extract the function, class, or method signature from the header.

#### Arguments

- `header` *str* - The header containing the function, class, or method definition.

#### Returns

- `str` - The extracted signature without the body or comments.

#### Signature

```python
def extract_signature(header: str) -> str: ...
```



## get_language_comment

[Show source in utils.py:67](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/utils.py#L67)

Get the language-specific comment syntax based on the programming language.

#### Arguments

- `language` *str* - The programming language.

#### Returns

- `str` - The language-specific comment syntax.

#### Signature

```python
def get_language_comment(language: str) -> str: ...
```



## load_language_mappings

[Show source in utils.py:38](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/utils.py#L38)

Load language mappings from a JSON file to map file extensions to programming languages.

#### Returns

- `Dict[str,` *str]* - A dictionary mapping file extensions to programming languages.

#### Raises

- `FileNotFoundError` - If the language configuration file is not found.
- `json.JSONDecodeError` - If there is an error decoding the JSON file.

#### Signature

```python
def load_language_mappings() -> Dict[str, str]: ...
```
