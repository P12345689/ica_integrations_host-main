# Docbuilder Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Docbuilder](./index.md#docbuilder) / Docbuilder Router

> Auto-generated documentation for [app.routes.docbuilder.docbuilder_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/docbuilder/docbuilder_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/docbuilder/templates'))


- [Docbuilder Router](#docbuilder-router)
  - [InputModel](#inputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [call_llm_async](#call_llm_async)
  - [clean_markdown_edge_quotes](#clean_markdown_edge_quotes)
  - [get_ibm_template_name](#get_ibm_template_name)

## InputModel

[Show source in docbuilder_router.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/docbuilder/docbuilder_router.py#L54)

Model to validate input data.

#### Signature

```python
class InputModel(BaseModel): ...
```



## OutputModel

[Show source in docbuilder_router.py:68](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/docbuilder/docbuilder_router.py#L68)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in docbuilder_router.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/docbuilder/docbuilder_router.py#L61)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in docbuilder_router.py:168](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/docbuilder/docbuilder_router.py#L168)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## call_llm_async

[Show source in docbuilder_router.py:144](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/docbuilder/docbuilder_router.py#L144)

Call the LLM with the given prompt asynchronously.

#### Arguments

- `prompt` *str* - The prompt to send to the LLM.

#### Returns

- `str` - The response from the LLM.

#### Raises

- `HTTPException` - If there is an error calling the LLM.

#### Signature

```python
async def call_llm_async(prompt: str) -> str: ...
```



## clean_markdown_edge_quotes

[Show source in docbuilder_router.py:76](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/docbuilder/docbuilder_router.py#L76)

Removes the leading and trailing triple backticks from a markdown text, typically used for code blocks.

#### Arguments

- `input_text` *str* - The markdown text from which to remove the edge triple backticks.

#### Returns

- `str` - The cleaned markdown text with the leading and trailing triple backticks removed.

#### Examples

```python
>>> clean_markdown_edge_quotes('```\nsome markdown\n```')
'some markdown'
>>> clean_markdown_edge_quotes('  ```\nsome markdown\n```  ')
'some markdown'
>>> clean_markdown_edge_quotes('some markdown')
'some markdown'
```

#### Signature

```python
def clean_markdown_edge_quotes(input_text: str) -> str: ...
```



## get_ibm_template_name

[Show source in docbuilder_router.py:108](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/docbuilder/docbuilder_router.py#L108)

Get the IBM template name based on the provided template type.

#### Arguments

- `template_type` *str* - The type of template.

#### Returns

- `str` - The corresponding IBM template name.

#### Examples

```python
>>> get_ibm_template_name("IBM Consulting Green")
'templates/ibm_consulting_green.pptx'
>>> get_ibm_template_name("IBM Technology Blue")
'templates/ibm_technology_blue.pptx'
>>> get_ibm_template_name("Unknown Type")
'templates/ibm_consulting_green.pptx'
```

#### Signature

```python
def get_ibm_template_name(template_type: str) -> str: ...
```
