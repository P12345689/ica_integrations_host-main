# Mail Template Creation Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Mail Template Creation](./index.md#mail-template-creation) / Mail Template Creation Router

> Auto-generated documentation for [dev.app.routes.mail_template_creation.mail_template_creation_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/mail_template_creation/templates'))


- [Mail Template Creation Router](#mail-template-creation-router)
  - [ExperienceInputModel](#experienceinputmodel)
  - [ExperienceMailInputModel](#experiencemailinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [TimestampInputModel](#timestampinputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [extract_and_save_html](#extract_and_save_html)
  - [generate_timestamp](#generate_timestamp)
  - [generate_zip_file](#generate_zip_file)

## ExperienceInputModel

[Show source in mail_template_creation_router.py:67](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L67)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## ExperienceMailInputModel

[Show source in mail_template_creation_router.py:71](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L71)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceMailInputModel(BaseModel): ...
```



## OutputModel

[Show source in mail_template_creation_router.py:81](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L81)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in mail_template_creation_router.py:76](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L76)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## TimestampInputModel

[Show source in mail_template_creation_router.py:63](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L63)

Model to validate input data for timestamp generation.

#### Signature

```python
class TimestampInputModel(BaseModel): ...
```



## add_custom_routes

[Show source in mail_template_creation_router.py:174](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L174)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## extract_and_save_html

[Show source in mail_template_creation_router.py:118](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L118)

Extracts HTML content enclosed within triple backticks from the provided text
and saves it to an HTML file, then returns the path to the file.

#### Arguments

- `text` *str* - The input text containing the HTML content enclosed in triple backticks.
- `base_dir` *str* - The base directory where the HTML file will be saved.

#### Returns

- `str` - The path to the generated HTML file.

#### Signature

```python
def extract_and_save_html(text: str, base_dir: str = "public/html_files") -> str: ...
```



## generate_timestamp

[Show source in mail_template_creation_router.py:89](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L89)

Generate a timestamp using the date command.

#### Arguments

- `format` *str* - The format string for the date command.

#### Returns

- `str` - The generated timestamp.

#### Raises

- `RuntimeError` - If the timestamp generation fails.

#### Signature

```python
def generate_timestamp(format: str) -> str: ...
```



## generate_zip_file

[Show source in mail_template_creation_router.py:152](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/mail_template_creation/mail_template_creation_router.py#L152)

Generate a ZIP file containing the given content.

#### Arguments

- `content` *str* - The content to be included in the ZIP file.
- `filename` *str* - The name of the file to be created inside the ZIP.

#### Returns

- `str` - The URL of the generated ZIP file.

#### Signature

```python
def generate_zip_file(content: str, filename: str) -> str: ...
```
