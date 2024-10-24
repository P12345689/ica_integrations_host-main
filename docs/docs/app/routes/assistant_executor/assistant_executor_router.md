# Assistant Executor Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Assistant Executor](./index.md#assistant-executor) / Assistant Executor Router

> Auto-generated documentation for [app.routes.assistant_executor.assistant_executor_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_executor/assistant_executor_router.py) module.

- [Assistant Executor Router](#assistant-executor-router)
  - [ExecutionRequest](#executionrequest)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## ExecutionRequest

[Show source in assistant_executor_router.py:40](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_executor/assistant_executor_router.py#L40)

Represents the request for executing an assistant.

#### Attributes

- `assistant_id` *str* - The ID of the assistant to be executed.
- `prompt` *str* - The prompt to be passed to the assistant.

#### Signature

```python
class ExecutionRequest(BaseModel): ...
```



## OutputModel

[Show source in assistant_executor_router.py:60](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_executor/assistant_executor_router.py#L60)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in assistant_executor_router.py:53](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_executor/assistant_executor_router.py#L53)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in assistant_executor_router.py:68](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/assistant_executor/assistant_executor_router.py#L68)

Adds custom routes to the FastAPI application.

#### Arguments

- [app](#assistant-executor-router) *FastAPI* - The FastAPI application instance.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
