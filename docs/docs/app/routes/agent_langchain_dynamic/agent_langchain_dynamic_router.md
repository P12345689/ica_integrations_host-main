# Agent Langchain Dynamic Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Agent Langchain Dynamic](./index.md#agent-langchain-dynamic) / Agent Langchain Dynamic Router

> Auto-generated documentation for [app.routes.agent_langchain_dynamic.agent_langchain_dynamic_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain_dynamic/agent_langchain_dynamic_router.py) module.

#### Attributes

- `MODEL_TYPE` - Constants: 'OLLAMA'

- `TOOLS_2` - get the tools: get_tools(['get_system_time'])


- [Agent Langchain Dynamic Router](#agent-langchain-dynamic-router)
  - [InputModel](#inputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [get_model](#get_model)

## InputModel

[Show source in agent_langchain_dynamic_router.py:33](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain_dynamic/agent_langchain_dynamic_router.py#L33)

Model for incoming request data to specify query.

#### Signature

```python
class InputModel(BaseModel): ...
```



## add_custom_routes

[Show source in agent_langchain_dynamic_router.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain_dynamic/agent_langchain_dynamic_router.py#L54)

Adds custom routes to the FastAPI application for agent invocation and result retrieval.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## get_model

[Show source in agent_langchain_dynamic_router.py:38](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain_dynamic/agent_langchain_dynamic_router.py#L38)

Returns the appropriate model based on the MODEL_TYPE environment variable.

#### Signature

```python
def get_model() -> Union[ChatOpenAI, ChatConsultingAssistants]: ...
```
