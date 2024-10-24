# Assistant Builder Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Assistant Builder](./index.md#assistant-builder) / Assistant Builder Router

> Auto-generated documentation for [app.routes.assistant_builder.assistant_builder_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_builder/assistant_builder_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/assistant_builder/templates'))


- [Assistant Builder Router](#assistant-builder-router)
  - [UserPrompt](#userprompt)
  - [add_custom_routes](#add_custom_routes)

## UserPrompt

[Show source in assistant_builder_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_builder/assistant_builder_router.py#L48)

Represents the user's prompt for generating an assistant.

#### Attributes

- `input` *str* - The description of the assistant to be generated.

#### Signature

```python
class UserPrompt(BaseModel): ...
```



## add_custom_routes

[Show source in assistant_builder_router.py:59](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_builder/assistant_builder_router.py#L59)

Adds custom routes to the FastAPI application.

#### Arguments

- [app](#assistant-builder-router) *FastAPI* - The FastAPI application instance.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
