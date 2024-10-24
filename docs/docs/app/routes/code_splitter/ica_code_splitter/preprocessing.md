# Preprocessing

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [App](../../../index.md#app) / [Routes](../../index.md#routes) / [Code Splitter](../index.md#code-splitter) / [Ica Code Splitter](./index.md#ica-code-splitter) / Preprocessing

> Auto-generated documentation for [app.routes.code_splitter.ica_code_splitter.preprocessing](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/preprocessing.py) module.

- [Preprocessing](#preprocessing)
  - [preprocess_code](#preprocess_code)

## preprocess_code

[Show source in preprocessing.py:39](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/ica_code_splitter/preprocessing.py#L39)

Preprocess the code by removing comments and extra newlines/spaces using regular expressions.

#### Arguments

- `code` *str* - The source code to preprocess.
- `language` *str* - The programming language of the source code.

#### Returns

- `str` - The preprocessed code with comments and extra newlines/spaces removed.

#### Signature

```python
def preprocess_code(code: str, language: str) -> str: ...
```
