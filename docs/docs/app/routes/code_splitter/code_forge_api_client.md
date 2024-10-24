# Code Forge Api Client

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Code Splitter](./index.md#code-splitter) / Code Forge Api Client

> Auto-generated documentation for [app.routes.code_splitter.code_forge_api_client](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_forge_api_client.py) module.

#### Attributes

- `API_URL_ENV` - Environment variables for API URL and API key: 'CODE_SPLITTER_API_URL'


- [Code Forge Api Client](#code-forge-api-client)
  - [count_tokens](#count_tokens)
  - [main](#main)
  - [send_request](#send_request)

## count_tokens

[Show source in code_forge_api_client.py:63](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_forge_api_client.py#L63)

#### Signature

```python
def count_tokens(api_url, api_key, files): ...
```



## main

[Show source in code_forge_api_client.py:82](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_forge_api_client.py#L82)

#### Signature

```python
def main(): ...
```



## send_request

[Show source in code_forge_api_client.py:47](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_forge_api_client.py#L47)

#### Signature

```python
def send_request(
    api_url, api_key, code, language, max_chunk_size, model, request_type
): ...
```
