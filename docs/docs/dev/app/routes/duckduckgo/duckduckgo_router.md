# Duckduckgo Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Duck Duck Go Search](./index.md#duck-duck-go-search) / Duckduckgo Router

> Auto-generated documentation for [dev.app.routes.duckduckgo.duckduckgo_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/duckduckgo/duckduckgo_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/duckduckgo/templates'))


- [Duckduckgo Router](#duckduckgo-router)
  - [DuckDuckGoSearchRequest](#duckduckgosearchrequest)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## DuckDuckGoSearchRequest

[Show source in duckduckgo_router.py:26](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/duckduckgo/duckduckgo_router.py#L26)

#### Signature

```python
class DuckDuckGoSearchRequest(BaseModel): ...
```



## OutputModel

[Show source in duckduckgo_router.py:37](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/duckduckgo/duckduckgo_router.py#L37)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in duckduckgo_router.py:30](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/duckduckgo/duckduckgo_router.py#L30)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in duckduckgo_router.py:45](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/duckduckgo/duckduckgo_router.py#L45)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```
