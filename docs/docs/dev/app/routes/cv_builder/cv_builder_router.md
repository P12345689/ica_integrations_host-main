# Cv Builder Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Cv Builder](./index.md#cv-builder) / Cv Builder Router

> Auto-generated documentation for [dev.app.routes.cv_builder.cv_builder_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/cv_builder/templates'))


- [Cv Builder Router](#cv-builder-router)
  - [OutputModel](#outputmodel)
  - [ProfilePostRequestModel](#profilepostrequestmodel)
  - [ProfileUpdateRequestModel](#profileupdaterequestmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [fetch_cv](#fetch_cv)
  - [get_cv_section](#get_cv_section)
  - [update_cv](#update_cv)

## OutputModel

[Show source in cv_builder_router.py:78](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py#L78)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ProfilePostRequestModel

[Show source in cv_builder_router.py:67](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py#L67)

Model to validate input data for profile update.

#### Signature

```python
class ProfilePostRequestModel(BaseModel): ...
```



## ProfileUpdateRequestModel

[Show source in cv_builder_router.py:61](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py#L61)

Model to validate input data for profile enhance.

#### Signature

```python
class ProfileUpdateRequestModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in cv_builder_router.py:73](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py#L73)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in cv_builder_router.py:134](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py#L134)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## fetch_cv

[Show source in cv_builder_router.py:110](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py#L110)

Fetch the CV from the external API.

#### Arguments

- `user_id` *str* - The user ID for fetching the CV.

#### Returns

- `dict` - The fetched CV data.

#### Raises

- `HTTPException` - If the CV fetching fails.

#### Signature

```python
async def fetch_cv(user_id: str): ...
```



## get_cv_section

[Show source in cv_builder_router.py:288](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py#L288)

#### Signature

```python
async def get_cv_section(input_data): ...
```



## update_cv

[Show source in cv_builder_router.py:84](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/cv_builder/cv_builder_router.py#L84)

Update the CV on the external API.

#### Arguments

- `user_id` *str* - The user ID for updating the CV.
- `updated_cv` *dict* - The updated CV data.

#### Returns

- `dict` - The API response.

#### Raises

- `HTTPException` - If the CV update fails.

#### Signature

```python
async def update_cv(user_id: str, updated_cv: dict): ...
```
