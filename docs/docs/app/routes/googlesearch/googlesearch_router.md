# Googlesearch Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Google Search](./index.md#google-search) / Googlesearch Router

> Auto-generated documentation for [app.routes.googlesearch.googlesearch_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/googlesearch/googlesearch_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/googlesearch/templates'))


- [Googlesearch Router](#googlesearch-router)
  - [GoogleSearchRequest](#googlesearchrequest)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## GoogleSearchRequest

[Show source in googlesearch_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/googlesearch/googlesearch_router.py#L48)

#### Signature

```python
class GoogleSearchRequest(BaseModel): ...
```



## OutputModel

[Show source in googlesearch_router.py:59](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/googlesearch/googlesearch_router.py#L59)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in googlesearch_router.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/googlesearch/googlesearch_router.py#L52)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in googlesearch_router.py:67](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/googlesearch/googlesearch_router.py#L67)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
