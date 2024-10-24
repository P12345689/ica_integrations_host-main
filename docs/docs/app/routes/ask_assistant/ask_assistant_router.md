# Ask Assistant Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Ask Assistant](./index.md#ask-assistant) / Ask Assistant Router

> Auto-generated documentation for [app.routes.ask_assistant.ask_assistant_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/ask_assistant/templates'))


- [Ask Assistant Router](#ask-assistant-router)
  - [AssistantInputModel](#assistantinputmodel)
  - [AssistantModel](#assistantmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [RoleModel](#rolemodel)
  - [TagModel](#tagmodel)
  - [add_custom_routes](#add_custom_routes)
  - [get_assistants](#get_assistants)

## AssistantInputModel

[Show source in ask_assistant_router.py:35](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py#L35)

Model to validate input data for assistant retrieval.

#### Signature

```python
class AssistantInputModel(BaseModel): ...
```



## AssistantModel

[Show source in ask_assistant_router.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py#L52)

Model to structure individual assistant data.

#### Signature

```python
class AssistantModel(BaseModel): ...
```



## OutputModel

[Show source in ask_assistant_router.py:75](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py#L75)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in ask_assistant_router.py:69](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py#L69)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## RoleModel

[Show source in ask_assistant_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py#L48)

#### Signature

```python
class RoleModel(BaseModel): ...
```



## TagModel

[Show source in ask_assistant_router.py:44](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py#L44)

#### Signature

```python
class TagModel(BaseModel): ...
```



## add_custom_routes

[Show source in ask_assistant_router.py:123](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py#L123)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## get_assistants

[Show source in ask_assistant_router.py:82](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_assistant/ask_assistant_router.py#L82)

Retrieve and filter assistants based on the given criteria.

#### Arguments

- `tags` *Optional[List[str]]* - List of tags to filter assistants.
- `roles` *Optional[List[str]]* - List of roles to filter assistants.
- `search_term` *Optional[str]* - Search term for assistant title or description.
- `assistant_id` *Optional[str]* - Specific assistant ID to retrieve.
- `refresh` *bool* - Whether to refresh the assistants data. Defaults to False.

#### Returns

- `List[AssistantModel]` - List of filtered assistants.

#### Examples

```python
>>> assistants = get_assistants(tags=["unified"], roles=["Software Developer"], refresh=True)
>>> len(assistants) > 0
True
```

#### Signature

```python
def get_assistants(
    tags: Optional[List[str]] = None,
    roles: Optional[List[str]] = None,
    search_term: Optional[str] = None,
    assistant_id: Optional[str] = None,
    refresh: bool = False,
) -> List[AssistantModel]: ...
```

#### See also

- [AssistantModel](#assistantmodel)
