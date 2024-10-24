# Assistant Finder Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Assistant Finder](./index.md#assistant-finder) / Assistant Finder Router

> Auto-generated documentation for [app.routes.assistant_finder.assistant_finder_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_finder/assistant_finder_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/assistant_finder/templates'))


- [Assistant Finder Router](#assistant-finder-router)
  - [InputModel](#inputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [calculate_similarity](#calculate_similarity)

## InputModel

[Show source in assistant_finder_router.py:45](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_finder/assistant_finder_router.py#L45)

Model to validate input data.

#### Signature

```python
class InputModel(BaseModel): ...
```



## OutputModel

[Show source in assistant_finder_router.py:60](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_finder/assistant_finder_router.py#L60)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in assistant_finder_router.py:53](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_finder/assistant_finder_router.py#L53)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in assistant_finder_router.py:110](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_finder/assistant_finder_router.py#L110)

Add custom routes to the FastAPI app.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## calculate_similarity

[Show source in assistant_finder_router.py:68](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_finder/assistant_finder_router.py#L68)

Calculate the cosine similarity between a list of assistant descriptions and a given description.

#### Arguments

assistants (List[Dict[str, Any]]): List of dictionaries representing assistants.
- `description` *str* - Input description to compare against.

#### Returns

- `List[Dict[str,` *Any]]* - Assistants sorted by similarity in descending order.

#### Examples

```python
>>> test_assistants = [{'id': '1', 'description': 'Data analysis'}, {'id': '2', 'description': 'Web development'}]
>>> test_description = 'Data science'
>>> calculate_similarity(test_assistants, test_description) # doctest: +ELLIPSIS
[{'id': ..., 'description': ..., 'similarity': ..., 'match_percentage': ...}]
```

#### Signature

```python
def calculate_similarity(
    assistants: List[Dict[str, Any]], description: str
) -> List[Dict[str, Any]]: ...
```
