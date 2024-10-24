# Assistant Reviewer Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Assistant Reviewer](./index.md#assistant-reviewer) / Assistant Reviewer Router

> Auto-generated documentation for [app.routes.assistant_reviewer.assistant_reviewer_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_reviewer/assistant_reviewer_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/assistant_reviewer/templates'))


- [Assistant Reviewer Router](#assistant-reviewer-router)
  - [InputModel](#inputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## InputModel

[Show source in assistant_reviewer_router.py:43](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_reviewer/assistant_reviewer_router.py#L43)

Model to validate input data.

#### Signature

```python
class InputModel(BaseModel): ...
```



## OutputModel

[Show source in assistant_reviewer_router.py:58](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_reviewer/assistant_reviewer_router.py#L58)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in assistant_reviewer_router.py:51](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_reviewer/assistant_reviewer_router.py#L51)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in assistant_reviewer_router.py:66](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_reviewer/assistant_reviewer_router.py#L66)

Add custom routes to the FastAPI app.

#### Arguments

- [App](../../index.md#app) *FastAPI* - The FastAPI application instance.

#### Examples

```python
>>> from fastapi.testclient import TestClient
>>> app = FastAPI()
>>> add_custom_routes(app)
>>> client = TestClient(app)
>>> response = client.post("/assistant_reviewer/invoke", json={"prompt": "Hello"})
>>> response.status_code
200
>>> response.json()["status"]
'success'
```

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
