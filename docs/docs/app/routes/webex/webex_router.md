# Webex Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Webex](./index.md#webex) / Webex Router

> Auto-generated documentation for [app.routes.webex.webex_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/webex/webex_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Mixtral 8x7b Instruct')

- `WEBEX_API_BASE_URL` - WebEx API base URL: 'https://webexapis.com/v1'

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/webex/templates'))


- [Webex Router](#webex-router)
  - [ExperienceInputModel](#experienceinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [SummarizeTranscriptInputModel](#summarizetranscriptinputmodel)
  - [WebExInputModel](#webexinputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [webex_operation](#webex_operation)

## ExperienceInputModel

[Show source in webex_router.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/webex/webex_router.py#L52)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## OutputModel

[Show source in webex_router.py:76](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/webex/webex_router.py#L76)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in webex_router.py:69](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/webex/webex_router.py#L69)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## SummarizeTranscriptInputModel

[Show source in webex_router.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/webex/webex_router.py#L61)

Model to validate input data for the summarize transcript route.

#### Signature

```python
class SummarizeTranscriptInputModel(BaseModel): ...
```



## WebExInputModel

[Show source in webex_router.py:41](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/webex/webex_router.py#L41)

Model to validate input data for WebEx operations.

#### Signature

```python
class WebExInputModel(BaseModel): ...
```



## add_custom_routes

[Show source in webex_router.py:163](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/webex/webex_router.py#L163)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## webex_operation

[Show source in webex_router.py:84](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/webex/webex_router.py#L84)

Perform a WebEx operation based on the given action using REST API.

#### Arguments

- `token` *str* - WebEx access token.
- `action` *str* - Action to perform.
- `params` *dict* - Additional parameters for the action.

#### Returns

- `str` - Result of the operation.

#### Raises

- `ValueError` - If the action is not supported or if required parameters are missing.

#### Signature

```python
def webex_operation(token: str, action: str, params: dict) -> str: ...
```
