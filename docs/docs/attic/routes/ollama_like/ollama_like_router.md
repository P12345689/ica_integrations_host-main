# Ollama Like Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / `attic` / `routes` / [Ollama Like](./index.md#ollama-like) / Ollama Like Router

> Auto-generated documentation for [attic.routes.ollama_like.ollama_like_router](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/ollama_like/ollama_like_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/ollama_like/templates'))


- [Ollama Like Router](#ollama-like-router)
  - [GenerateInputModel](#generateinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## GenerateInputModel

[Show source in ollama_like_router.py:35](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/ollama_like/ollama_like_router.py#L35)

Model to validate input data for text generation.

#### Signature

```python
class GenerateInputModel(BaseModel): ...
```



## OutputModel

[Show source in ollama_like_router.py:49](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/ollama_like/ollama_like_router.py#L49)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in ollama_like_router.py:44](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/ollama_like/ollama_like_router.py#L44)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in ollama_like_router.py:55](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/ollama_like/ollama_like_router.py#L55)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```
