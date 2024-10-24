# Gs Agents Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Gs Agents](./index.md#gs-agents) / Gs Agents Router

> Auto-generated documentation for [dev.app.routes.gs_agents.gs_agents_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/gs_agents/gs_agents_router.py) module.

- [Gs Agents Router](#gs-agents-router)
  - [InputModel](#inputmodel)
  - [LLMResponseModel](#llmresponsemodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## InputModel

[Show source in gs_agents_router.py:30](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/gs_agents/gs_agents_router.py#L30)

Model to validate input data.

#### Signature

```python
class InputModel(BaseModel): ...
```



## LLMResponseModel

[Show source in gs_agents_router.py:36](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/gs_agents/gs_agents_router.py#L36)

Model to structure the LLM response data.

#### Signature

```python
class LLMResponseModel(BaseModel): ...
```



## OutputModel

[Show source in gs_agents_router.py:52](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/gs_agents/gs_agents_router.py#L52)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in gs_agents_router.py:45](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/gs_agents/gs_agents_router.py#L45)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in gs_agents_router.py:60](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/gs_agents/gs_agents_router.py#L60)

Add custom routes to the FastAPI app.

#### Arguments

- [App](../../../../app/index.md#app) *FastAPI* - The FastAPI application instance.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
