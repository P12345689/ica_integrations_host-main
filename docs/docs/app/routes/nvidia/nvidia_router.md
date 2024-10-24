# Nvidia Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Nvidia](./index.md#nvidia) / Nvidia Router

> Auto-generated documentation for [app.routes.nvidia.nvidia_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/nvidia/nvidia_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/nvidia/templates'))


- [Nvidia Router](#nvidia-router)
  - [InputModel](#inputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## InputModel

[Show source in nvidia_router.py:41](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/nvidia/nvidia_router.py#L41)

Model to validate input data.

#### Signature

```python
class InputModel(BaseModel): ...
```



## OutputModel

[Show source in nvidia_router.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/nvidia/nvidia_router.py#L54)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in nvidia_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/nvidia/nvidia_router.py#L48)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in nvidia_router.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/nvidia/nvidia_router.py#L61)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```
