# Github Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Github](./index.md#github) / Github Router

> Auto-generated documentation for [app.routes.github.github_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/github/github_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/github/templates'))


- [Github Router](#github-router)
  - [ExperienceInputModel](#experienceinputmodel)
  - [GitHubInputModel](#githubinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [github_operation](#github_operation)
  - [parse_repo_url](#parse_repo_url)

## ExperienceInputModel

[Show source in github_router.py:46](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/github/github_router.py#L46)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## GitHubInputModel

[Show source in github_router.py:39](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/github/github_router.py#L39)

Model to validate input data for GitHub operations.

#### Signature

```python
class GitHubInputModel(BaseModel): ...
```



## OutputModel

[Show source in github_router.py:57](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/github/github_router.py#L57)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in github_router.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/github/github_router.py#L52)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in github_router.py:155](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/github/github_router.py#L155)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## github_operation

[Show source in github_router.py:70](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/github/github_router.py#L70)

Perform a GitHub operation based on the given action.

#### Arguments

- `token` *Optional[str]* - GitHub access token.
- `repo_url` *str* - Full URL of the GitHub repository.
- `action` *str* - Action to perform.
- `params` *dict* - Additional parameters for the action.

#### Returns

- `str` - Result of the operation.

#### Raises

- `ValueError` - If the action is not supported or if required parameters are missing.

#### Signature

```python
def github_operation(
    token: Optional[str], repo_url: str, action: str, params: dict
) -> str: ...
```



## parse_repo_url

[Show source in github_router.py:63](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/github/github_router.py#L63)

Parse the repository URL to extract the base URL and repo name.

#### Signature

```python
def parse_repo_url(repo_url: str) -> tuple[str, str]: ...
```
