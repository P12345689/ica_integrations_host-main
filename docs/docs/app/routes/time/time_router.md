# Time Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Time](./index.md#time) / Time Router

> Auto-generated documentation for [app.routes.time.time_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/time/time_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/time/templates'))


- [Time Router](#time-router)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [SystemTimeInputModel](#systemtimeinputmodel)
  - [TimeInputModel](#timeinputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [get_system_time](#get_system_time)

## OutputModel

[Show source in time_router.py:47](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/time/time_router.py#L47)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in time_router.py:42](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/time/time_router.py#L42)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## SystemTimeInputModel

[Show source in time_router.py:38](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/time/time_router.py#L38)

Model to validate input data for system time retrieval.

#### Signature

```python
class SystemTimeInputModel(BaseModel): ...
```



## TimeInputModel

[Show source in time_router.py:34](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/time/time_router.py#L34)

Model to validate input data for time-related queries.

#### Signature

```python
class TimeInputModel(BaseModel): ...
```



## add_custom_routes

[Show source in time_router.py:60](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/time/time_router.py#L60)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## get_system_time

[Show source in time_router.py:53](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/time/time_router.py#L53)

Returns the current date and time in the specified format.

#### Signature

```python
def get_system_time(format: str = "%Y-%m-%dT%H:%M:%S%Z") -> str: ...
```
