# Ask Docs Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Ask Docs](./index.md#ask-docs) / Ask Docs Router

> Auto-generated documentation for [app.routes.ask_docs.ask_docs_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_docs/ask_docs_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/ask_docs/templates'))


- [Ask Docs Router](#ask-docs-router)
  - [CollectionInputModel](#collectioninputmodel)
  - [CollectionModel](#collectionmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [get_collections](#get_collections)

## CollectionInputModel

[Show source in ask_docs_router.py:36](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_docs/ask_docs_router.py#L36)

Model to validate input data for collection retrieval and querying.

#### Signature

```python
class CollectionInputModel(BaseModel): ...
```



## CollectionModel

[Show source in ask_docs_router.py:45](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_docs/ask_docs_router.py#L45)

Model to structure individual collection data.

#### Signature

```python
class CollectionModel(BaseModel):
    def __init__(self, **data): ...
```



## OutputModel

[Show source in ask_docs_router.py:76](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_docs/ask_docs_router.py#L76)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in ask_docs_router.py:70](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_docs/ask_docs_router.py#L70)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in ask_docs_router.py:106](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_docs/ask_docs_router.py#L106)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## get_collections

[Show source in ask_docs_router.py:83](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_docs/ask_docs_router.py#L83)

Retrieve document collections.

#### Arguments

- `refresh` *bool* - Whether to refresh the collections data. Defaults to False.

#### Returns

- `List[CollectionModel]` - List of document collections.

#### Examples

```python
>>> collections = get_collections(refresh=True)
>>> len(collections) > 0
True
```

#### Signature

```python
def get_collections(refresh: bool = False) -> List[CollectionModel]: ...
```

#### See also

- [CollectionModel](#collectionmodel)
