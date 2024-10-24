# File Upload Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [File Upload](./index.md#file-upload) / File Upload Router

> Auto-generated documentation for [app.routes.file_upload.file_upload_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/file_upload/file_upload_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/file_upload/templates'))


- [File Upload Router](#file-upload-router)
  - [FileListOutputModel](#filelistoutputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [UploadURLOutputModel](#uploadurloutputmodel)
  - [UserInputModel](#userinputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [generate_user_hash](#generate_user_hash)

## FileListOutputModel

[Show source in file_upload_router.py:58](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/file_upload/file_upload_router.py#L58)

Model to structure the file list response.

#### Signature

```python
class FileListOutputModel(BaseModel): ...
```



## OutputModel

[Show source in file_upload_router.py:67](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/file_upload/file_upload_router.py#L67)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in file_upload_router.py:62](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/file_upload/file_upload_router.py#L62)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## UploadURLOutputModel

[Show source in file_upload_router.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/file_upload/file_upload_router.py#L54)

Model to structure the upload URL response.

#### Signature

```python
class UploadURLOutputModel(BaseModel): ...
```



## UserInputModel

[Show source in file_upload_router.py:49](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/file_upload/file_upload_router.py#L49)

Model to validate input data for user identification.

#### Signature

```python
class UserInputModel(BaseModel): ...
```



## add_custom_routes

[Show source in file_upload_router.py:90](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/file_upload/file_upload_router.py#L90)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## generate_user_hash

[Show source in file_upload_router.py:73](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/file_upload/file_upload_router.py#L73)

Generate a hash from team ID and user email.

#### Arguments

- `team_id` *str* - The team ID.
- `user_email` *str* - The user's email.

#### Returns

- `str` - A hash string.

```python
>>> generate_user_hash("team123", "user@example.com")
'8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
```

#### Signature

```python
def generate_user_hash(team_id: str, user_email: str) -> str: ...
```
