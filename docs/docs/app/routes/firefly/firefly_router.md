# Firefly Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Adobe Firefly Integration](./index.md#adobe-firefly-integration) / Firefly Router

> Auto-generated documentation for [app.routes.firefly.firefly_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py) module.

#### Attributes

- `log` - Logging: logging.getLogger(__name__)

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/firefly/templates'))

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')


- [Firefly Router](#firefly-router)
  - [FireflyAuthException](#fireflyauthexception)
  - [InputModel](#inputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [adobe_firefly_generative_fill](#adobe_firefly_generative_fill)
  - [adobe_firefly_headers](#adobe_firefly_headers)
  - [adobe_firefly_image_expand](#adobe_firefly_image_expand)
  - [adobe_firefly_image_generation](#adobe_firefly_image_generation)
  - [adobe_image_upload](#adobe_image_upload)
  - [call_adobe_firefly_api](#call_adobe_firefly_api)
  - [download_image](#download_image)
  - [get_adobe_firefly_token](#get_adobe_firefly_token)

## FireflyAuthException

[Show source in firefly_router.py:78](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L78)

Thrown whenever there are issues authenticating to the Firefly API.

This exception is raised when there is a failure to authenticate with the Firefly API,
either due to missing or invalid credentials, or any other authentication-related issues.

#### Attributes

- `message` *str* - The error message associated with the authentication exception.

#### Methods

- `__init__(self,` *message* - str): Initializes a new instance of the FireflyAuthException class
    with the specified error message.

#### Examples

```python
>>> try:
...     # Attempt to authenticate with Firefly API
...     token = get_adobe_firefly_token()
... except FireflyAuthException as e:
...     print(f"Authentication failed: {e}")
...
Authentication failed: Invalid credentials
```

#### Signature

```python
class FireflyAuthException(Exception):
    def __init__(self, message: str): ...
```



## InputModel

[Show source in firefly_router.py:51](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L51)

Model to validate input data.

#### Signature

```python
class InputModel(BaseModel): ...
```



## OutputModel

[Show source in firefly_router.py:71](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L71)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in firefly_router.py:65](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L65)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in firefly_router.py:380](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L380)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## adobe_firefly_generative_fill

[Show source in firefly_router.py:247](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L247)

Makes an image expand call, uploading the image to expand.

#### Arguments

- `input_data` *InputModel* - The input data for generative fill.
- `access_token` *str* - The access token for authentication.
- `firefly_endpoint` *str* - The Firefly API endpoint.

#### Returns

- `str` - The presigned URL of the generated image.

#### Raises

- `requests.RequestException` - If there is an error generating the image.

#### Examples

```python
>>> input_data = InputModel(query="A beautiful sunset", reference_image="https://example.com/image.png", mask_image="https://example.com/mask.png")
>>> access_token = "your_access_token"
>>> firefly_endpoint = "firefly-beta.adobe.io"
>>> image_url = adobe_firefly_generative_fill(input_data, access_token, firefly_endpoint)
>>> assert image_url.startswith("https://")
```

#### Signature

```python
def adobe_firefly_generative_fill(
    input_data: InputModel, access_token: str, firefly_endpoint: str
) -> str: ...
```

#### See also

- [InputModel](#inputmodel)



## adobe_firefly_headers

[Show source in firefly_router.py:151](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L151)

Creates headers needed for Firefly calls.

#### Arguments

- `access_token` *str* - The access token for authentication.

#### Returns

- `Dict[str,` *str]* - The headers dictionary.

#### Examples

```python
>>> access_token = "your_access_token"
>>> headers = adobe_firefly_headers(access_token)
>>> assert headers["Authorization"] == f"Bearer {access_token}"
```

#### Signature

```python
def adobe_firefly_headers(access_token: str) -> Dict[str, str]: ...
```



## adobe_firefly_image_expand

[Show source in firefly_router.py:285](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L285)

Makes a generative fill call, uploading the image to work on, and the mask area.

#### Arguments

- `input_data` *InputModel* - The input data for image expansion.
- `access_token` *str* - The access token for authentication.
- `firefly_endpoint` *str* - The Firefly API endpoint.

#### Returns

- `str` - The presigned URL of the generated image.

#### Raises

- `requests.RequestException` - If there is an error generating the image.

#### Examples

```python
>>> input_data = InputModel(query="A beautiful sunset", reference_image="https://example.com/image.png")
>>> access_token = "your_access_token"
>>> firefly_endpoint = "firefly-beta.adobe.io"
>>> image_url = adobe_firefly_image_expand(input_data, access_token, firefly_endpoint)
>>> assert image_url.startswith("https://")
```

#### Signature

```python
def adobe_firefly_image_expand(
    input_data: InputModel, access_token: str, firefly_endpoint: str
) -> str: ...
```

#### See also

- [InputModel](#inputmodel)



## adobe_firefly_image_generation

[Show source in firefly_router.py:204](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L204)

Makes an image generation call, uploading reference images as needed.

#### Arguments

- `input_data` *InputModel* - The input data for image generation.
- `access_token` *str* - The access token for authentication.
- `firefly_endpoint` *str* - The Firefly API endpoint.

#### Returns

- `str` - The presigned URL of the generated image.

#### Raises

- `requests.RequestException` - If there is an error generating the image.

#### Examples

```python
>>> input_data = InputModel(query="A beautiful sunset")
>>> access_token = "your_access_token"
>>> firefly_endpoint = "firefly-beta.adobe.io"
>>> image_url = adobe_firefly_image_generation(input_data, access_token, firefly_endpoint)
>>> assert image_url.startswith("https://")
```

#### Signature

```python
def adobe_firefly_image_generation(
    input_data: InputModel, access_token: str, firefly_endpoint: str
) -> str: ...
```

#### See also

- [InputModel](#inputmodel)



## adobe_image_upload

[Show source in firefly_router.py:174](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L174)

Grabs an image from a URL, then uploads it for use in Firefly.

#### Arguments

- `url` *str* - The URL of the image to upload.
- `access_token` *str* - The access token for authentication.
- `firefly_endpoint` *str* - The Firefly API endpoint.

#### Returns

- `str` - The ID of the uploaded image.

#### Raises

- `requests.RequestException` - If there is an error uploading the image.

#### Examples

```python
>>> url = "https://example.com/image.png"
>>> access_token = "your_access_token"
>>> firefly_endpoint = "firefly-beta.adobe.io"
>>> image_id = adobe_image_upload(url, access_token, firefly_endpoint)
>>> assert isinstance(image_id, str)
```

#### Signature

```python
def adobe_image_upload(url: str, access_token: str, firefly_endpoint: str) -> str: ...
```



## call_adobe_firefly_api

[Show source in firefly_router.py:322](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L322)

Makes a call to the Firefly API, authenticating as needed.

Authentication is handled by taking the Client ID and Secret,
then making an OAuth request for an access token.

#### Arguments

- `input_data` *InputModel* - The input data for the API call.

#### Returns

- `str` - The presigned URL of the generated image.

#### Raises

- [FireflyAuthException](#fireflyauthexception) - If there is an error authenticating with Firefly.
- `requests.RequestException` - If there is an error making the API call.

#### Examples

```python
>>> input_data = InputModel(query="A beautiful sunset")
>>> image_url = call_adobe_firefly_api(input_data)
>>> assert image_url.startswith("https://")
```

#### Signature

```python
def call_adobe_firefly_api(input_data: InputModel) -> str: ...
```

#### See also

- [InputModel](#inputmodel)



## download_image

[Show source in firefly_router.py:356](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L356)

Downloads an image from a URL and saves it to the specified output path.

#### Arguments

- `image_url` *str* - The URL of the image to download.
- `output_path` *str* - The path where the downloaded image will be saved.

#### Raises

- `requests.RequestException` - If there is an error downloading the image.

#### Examples

```python
>>> image_url = "https://example.com/image.png"
>>> output_path = "public/firefly/image.png"
>>> download_image(image_url, output_path)
>>> assert os.path.exists(output_path)
```

#### Signature

```python
def download_image(image_url: str, output_path: str) -> None: ...
```



## get_adobe_firefly_token

[Show source in firefly_router.py:113](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/firefly/firefly_router.py#L113)

Makes an OAuth call to get an API access token for Firefly.

The Client ID and Secret are provided by the following environment variables:
- ADOBE_FIREFLY_CLIENT_ID
- ADOBE_FIREFLY_CLIENT_SECRET

#### Returns

- `str` - The access token.

#### Raises

- [FireflyAuthException](#fireflyauthexception) - If there is a failure to authenticate.

#### Examples

```python
>>> os.environ["ADOBE_FIREFLY_CLIENT_ID"] = "your_client_id"
>>> os.environ["ADOBE_FIREFLY_CLIENT_SECRET"] = "your_client_secret"
>>> token = get_adobe_firefly_token()
>>> assert token.startswith("Bearer ")
```

#### Signature

```python
def get_adobe_firefly_token() -> str: ...
```
