# Mermaid Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Mermaid Tool

> Auto-generated documentation for [app.tools.global_tools.mermaid_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/mermaid_tool.py) module.

- [Mermaid Tool](#mermaid-tool)
  - [get_text_between_markers](#get_text_between_markers)
  - [syntax_to_image](#syntax_to_image)

## get_text_between_markers

[Show source in mermaid_tool.py:40](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/mermaid_tool.py#L40)

Extracts and returns the text between triple backtick markers.

#### Arguments

- `text` *str* - The input text potentially containing triple backtick markers.

#### Returns

- `str` - The text found between the triple backtick markers. If no markers are found,
     returns the trimmed input text.

#### Signature

```python
def get_text_between_markers(text: str) -> str: ...
```



## syntax_to_image

[Show source in mermaid_tool.py:8](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/mermaid_tool.py#L8)

Generates a mermaid diagram image from mermaid syntax and returns a URL.

#### Arguments

- `mermaid_syntax` *str* - The mermaid syntax string, which may contain code blocks.

#### Returns

- `str` - A URL linking to the generated mermaid diagram image.

#### Signature

```python
@tool
def syntax_to_image(mermaid_syntax: str) -> str: ...
```
