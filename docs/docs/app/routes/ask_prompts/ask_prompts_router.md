# Ask Prompts Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Ask Prompts](./index.md#ask-prompts) / Ask Prompts Router

> Auto-generated documentation for [app.routes.ask_prompts.ask_prompts_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/ask_prompts/templates'))


- [Ask Prompts Router](#ask-prompts-router)
  - [OutputModel](#outputmodel)
  - [PromptInputModel](#promptinputmodel)
  - [PromptModel](#promptmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [RoleModel](#rolemodel)
  - [TagModel](#tagmodel)
  - [Visibility](#visibility)
  - [add_custom_routes](#add_custom_routes)
  - [get_prompts](#get_prompts)
  - [match_pattern](#match_pattern)

## OutputModel

[Show source in ask_prompts_router.py:75](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L75)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## PromptInputModel

[Show source in ask_prompts_router.py:49](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L49)

Model to validate input data for prompt retrieval.

#### Signature

```python
class PromptInputModel(BaseModel): ...
```



## PromptModel

[Show source in ask_prompts_router.py:59](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L59)

Model to structure individual prompt data.

#### Signature

```python
class PromptModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in ask_prompts_router.py:70](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L70)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## RoleModel

[Show source in ask_prompts_router.py:46](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L46)

#### Signature

```python
class RoleModel(BaseModel): ...
```



## TagModel

[Show source in ask_prompts_router.py:43](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L43)

#### Signature

```python
class TagModel(BaseModel): ...
```



## Visibility

[Show source in ask_prompts_router.py:37](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L37)

Enum for prompt visibility options.

#### Signature

```python
class Visibility(str, Enum): ...
```



## add_custom_routes

[Show source in ask_prompts_router.py:168](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L168)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## get_prompts

[Show source in ask_prompts_router.py:102](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L102)

Retrieve and filter prompts based on the given criteria.

#### Arguments

- `tags` *Optional[List[str]]* - List of tags to filter prompts (supports glob).
- `roles` *Optional[List[str]]* - List of roles to filter prompts.
- `search_term` *Optional[str]* - Search term for prompt title or description (supports regex and glob).
visibility (Optional[Union[Visibility, str]]): Visibility filter (PRIVATE, TEAM, PUBLIC, or * for any).
- `user_email` *Optional[str]* - Filter by user email.
- `prompt_id` *Optional[str]* - Specific prompt ID to retrieve.
- `refresh` *bool* - Whether to refresh the prompts data. Defaults to False.

#### Returns

- `List[PromptModel]` - List of filtered prompts.

#### Examples

```python
>>> prompts = get_prompts(tags=["crew*"], visibility="*", refresh=True)
>>> len(prompts) > 0
True
```

#### Signature

```python
def get_prompts(
    tags: Optional[List[str]] = None,
    roles: Optional[List[str]] = None,
    search_term: Optional[str] = None,
    visibility: Optional[Union[Visibility, str]] = None,
    user_email: Optional[str] = None,
    prompt_id: Optional[str] = None,
    refresh: bool = False,
) -> List[PromptModel]: ...
```

#### See also

- [PromptModel](#promptmodel)
- [Visibility](#visibility)



## match_pattern

[Show source in ask_prompts_router.py:81](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/ask_prompts/ask_prompts_router.py#L81)

Match the pattern against the text using regex and glob patterns.

#### Arguments

- `text` *str* - The text to search in.
- `pattern` *str* - The search pattern (regex or glob).

#### Returns

- `bool` - True if the pattern matches, False otherwise.

#### Signature

```python
def match_pattern(text: str, pattern: str) -> bool: ...
```
