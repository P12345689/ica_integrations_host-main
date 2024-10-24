# Gpt4vision Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Gpt4vision Tool

> Auto-generated documentation for [app.tools.global_tools.gpt4vision_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/gpt4vision_tool.py) module.

- [Gpt4vision Tool](#gpt4vision-tool)
  - [call_gpt4_vision_api](#call_gpt4_vision_api)

## call_gpt4_vision_api

[Show source in gpt4vision_tool.py:33](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/gpt4vision_tool.py#L33)

Calls the GPT-4 Vision API to perform image-to-text transformation.

#### Arguments

- `input_json` *str* - A JSON string containing 'image' (URL of the image) and 'query' (question about the image) keys.

#### Returns

- `str` - The content of the response from the GPT-4 Vision API.

#### Raises

- `ValueError` - If the input JSON is invalid or missing required keys.
- `requests.exceptions.RequestException` - If there's an error sending the request to the GPT-4 Vision API.

#### Signature

```python
def call_gpt4_vision_api(input_json: str) -> str: ...
```
