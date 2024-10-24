# Ms Teams Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Ms Teams](./index.md#ms-teams) / Ms Teams Router

> Auto-generated documentation for [dev.app.routes.ms_teams.ms_teams_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/ms_teams/ms_teams_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/ms_teams/templates'))


- [Ms Teams Router](#ms-teams-router)
  - [ExperienceInputModel](#experienceinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [TeamsInputModel](#teamsinputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [teams_operation](#teams_operation)

## ExperienceInputModel

[Show source in ms_teams_router.py:53](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/ms_teams/ms_teams_router.py#L53)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## OutputModel

[Show source in ms_teams_router.py:67](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/ms_teams/ms_teams_router.py#L67)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in ms_teams_router.py:60](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/ms_teams/ms_teams_router.py#L60)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## TeamsInputModel

[Show source in ms_teams_router.py:45](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/ms_teams/ms_teams_router.py#L45)

Model to validate input data for Teams operations.

#### Signature

```python
class TeamsInputModel(BaseModel): ...
```



## add_custom_routes

[Show source in ms_teams_router.py:147](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/ms_teams/ms_teams_router.py#L147)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## teams_operation

[Show source in ms_teams_router.py:76](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/ms_teams/ms_teams_router.py#L76)

Perform an action on MS Teams

#### Arguments

- `token` *str* - Teams access token.
- `action` *str* - Action to perform.
- `params` *dict* - Additional parameters for the action.

#### Returns

- `str` - Result of the operation.

#### Raises

- `ValueError` - If the action is not supported or if required parameters are missing.

#### Signature

```python
def teams_operation(action: str, params: dict, token: str) -> str: ...
```
