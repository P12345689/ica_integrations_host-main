# Mermaid Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Mermaid](./index.md#mermaid) / Mermaid Router

> Auto-generated documentation for [app.routes.mermaid.mermaid_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/mermaid/mermaid_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/mermaid/templates'))


- [Mermaid Router](#mermaid-router)
  - [MermaidRequest](#mermaidrequest)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [format_prompt](#format_prompt)

## MermaidRequest

[Show source in mermaid_router.py:46](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/mermaid/mermaid_router.py#L46)

#### Signature

```python
class MermaidRequest(BaseModel): ...
```



## OutputModel

[Show source in mermaid_router.py:60](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/mermaid/mermaid_router.py#L60)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in mermaid_router.py:53](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/mermaid/mermaid_router.py#L53)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in mermaid_router.py:68](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/mermaid/mermaid_router.py#L68)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## format_prompt

[Show source in mermaid_router.py:220](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/mermaid/mermaid_router.py#L220)

Formats the prompt for generating Mermaid syntax.

#### Arguments

- `query` *str* - The query or text to generate the Mermaid syntax for.
- `max_tokens` *int* - The maximum number of tokens allowed in the generated syntax.

#### Returns

- `str` - The formatted prompt.

#### Signature

```python
def format_prompt(query: str, max_tokens: int) -> str: ...
```
