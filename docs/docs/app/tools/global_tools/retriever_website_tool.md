# Retriever Website Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Retriever Website Tool

> Auto-generated documentation for [app.tools.global_tools.retriever_website_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/retriever_website_tool.py) module.

- [Retriever Website Tool](#retriever-website-tool)
  - [clean_input_json](#clean_input_json)
  - [retrieve_website_content](#retrieve_website_content)

## clean_input_json

[Show source in retriever_website_tool.py:28](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/retriever_website_tool.py#L28)

Cleans the input JSON string by removing any trailing characters after the JSON object.

#### Arguments

- `input_str` *str* - The input JSON string.

#### Returns

- `str` - The cleaned JSON string.

#### Signature

```python
def clean_input_json(input_str: str) -> str: ...
```



## retrieve_website_content

[Show source in retriever_website_tool.py:47](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/retriever_website_tool.py#L47)

Retrieves the content of a website and converts it to plain text.

#### Arguments

- `input_json` *Any* - A JSON string or dictionary containing a 'url' key with the website URL.

#### Returns

- `str` - The plain text content of the website.

#### Raises

- `ValueError` - If the input JSON is invalid or missing the required 'url' key.
- `requests.exceptions.RequestException` - If there's an error retrieving the website content.

#### Signature

```python
@tool
def retrieve_website_content(input_json: Any) -> str: ...
```
