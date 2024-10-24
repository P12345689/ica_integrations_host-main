# Docbuilder Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Docbuilder Tool

> Auto-generated documentation for [app.tools.global_tools.docbuilder_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/docbuilder_tool.py) module.

#### Attributes

- `global_docbuilder` - Create a global variable to store the docbuilder function: None


- [Docbuilder Tool](#docbuilder-tool)
  - [docbuilder_tool_markdown_to_pptx_docx](#docbuilder_tool_markdown_to_pptx_docx)
  - [initialize_docbuilder](#initialize_docbuilder)

## docbuilder_tool_markdown_to_pptx_docx

[Show source in docbuilder_tool.py:53](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/docbuilder_tool.py#L53)

Tool for generating PPTX and DOCX documents from input text.

#### Arguments

- `input_text` *str* - The text content to be converted into documents.
- `template_type` *str, optional* - The type of template to use. Defaults to "IBM Consulting Green".

#### Returns

- `str` - A message containing URLs to the generated PPTX and DOCX documents.

#### Raises

- `ValueError` - If the input text is empty or invalid.

#### Examples

```python
>>> text = "OpenShift is a Kubernetes platform..."
>>> result = docbuilder_tool_markdown_to_pptx_docx(text)
>>> print(result)
URLs to the generated documents: PPTX: http://..., DOCX: http://...
```

#### Signature

```python
@tool
def docbuilder_tool_markdown_to_pptx_docx(
    input_text: str, template_type: Optional[str] = "IBM Consulting Green"
) -> str: ...
```



## initialize_docbuilder

[Show source in docbuilder_tool.py:37](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/docbuilder_tool.py#L37)

Initialize the global docbuilder function.

#### Signature

```python
def initialize_docbuilder() -> None: ...
```
