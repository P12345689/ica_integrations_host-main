# Logo Generator Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / `attic` / `routes` / [Logo Generator](./index.md#logo-generator) / Logo Generator Router

> Auto-generated documentation for [attic.routes.logo_generator.logo_generator_router](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/logo_generator/logo_generator_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/logo_generator/templates'))


- [Logo Generator Router](#logo-generator-router)
  - [InputModel](#inputmodel)
  - [LLMResponseModel](#llmresponsemodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## InputModel

[Show source in logo_generator_router.py:33](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/logo_generator/logo_generator_router.py#L33)

Model to validate input data.

#### Signature

```python
class InputModel(BaseModel): ...
```



## LLMResponseModel

[Show source in logo_generator_router.py:38](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/logo_generator/logo_generator_router.py#L38)

Model to structure the LLM response data.

#### Signature

```python
class LLMResponseModel(BaseModel): ...
```



## OutputModel

[Show source in logo_generator_router.py:54](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/logo_generator/logo_generator_router.py#L54)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in logo_generator_router.py:47](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/logo_generator/logo_generator_router.py#L47)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in logo_generator_router.py:62](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/logo_generator/logo_generator_router.py#L62)

Add custom routes to the FastAPI app.

#### Arguments

- [App](../../../app/index.md#app) *FastAPI* - The FastAPI application instance.

#### Examples

```python
>>> from fastapi.testclient import TestClient
>>> app = FastAPI()
>>> add_custom_routes(app)
>>> client = TestClient(app)
>>> response = client.post("/logo_generator/invoke", json={"model": "test_model", "prompt": "Hello"})
>>> response.status_code
200
>>> response.json()["status"]
'success'
```

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
