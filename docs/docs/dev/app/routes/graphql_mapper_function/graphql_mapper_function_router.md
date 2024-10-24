# Graphql Mapper Function Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Graphql Mapper Function](./index.md#graphql-mapper-function) / Graphql Mapper Function Router

> Auto-generated documentation for [dev.app.routes.graphql_mapper_function.graphql_mapper_function_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphql_mapper_function/graphql_mapper_function_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/graphql_mapper_function/templates'))


- [Graphql Mapper Function Router](#graphql-mapper-function-router)
  - [ExperienceInputModel](#experienceinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## ExperienceInputModel

[Show source in graphql_mapper_function_router.py:67](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphql_mapper_function/graphql_mapper_function_router.py#L67)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## OutputModel

[Show source in graphql_mapper_function_router.py:76](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphql_mapper_function/graphql_mapper_function_router.py#L76)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in graphql_mapper_function_router.py:71](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphql_mapper_function/graphql_mapper_function_router.py#L71)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in graphql_mapper_function_router.py:84](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphql_mapper_function/graphql_mapper_function_router.py#L84)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
