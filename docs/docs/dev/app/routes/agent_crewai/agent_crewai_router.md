# Agent Crewai Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Agent Crewai](./index.md#agent-crewai) / Agent Crewai Router

> Auto-generated documentation for [dev.app.routes.agent_crewai.agent_crewai_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)


- [Agent Crewai Router](#agent-crewai-router)
  - [AgentConfig](#agentconfig)
  - [AgentConfigException](#agentconfigexception)
  - [AgentData](#agentdata)
  - [InputModel](#inputmodel)
  - [MyAgentFinish](#myagentfinish)
  - [TaskConfigException](#taskconfigexception)
  - [TaskData](#taskdata)
  - [add_custom_routes](#add_custom_routes)

## AgentConfig

[Show source in agent_crewai_router.py:77](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py#L77)

#### Signature

```python
class AgentConfig(BaseModel): ...
```



## AgentConfigException

[Show source in agent_crewai_router.py:57](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py#L57)

#### Signature

```python
class AgentConfigException(Exception): ...
```



## AgentData

[Show source in agent_crewai_router.py:60](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py#L60)

#### Signature

```python
class AgentData(BaseModel): ...
```



## InputModel

[Show source in agent_crewai_router.py:35](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py#L35)

Model for incoming request data to specify query, optional context, tools to use, model configuration, and prompt template.

#### Signature

```python
class InputModel(BaseModel): ...
```



## MyAgentFinish

[Show source in agent_crewai_router.py:50](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py#L50)

#### Signature

```python
class MyAgentFinish:
    def __init__(self, crew_results): ...
```



## TaskConfigException

[Show source in agent_crewai_router.py:54](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py#L54)

#### Signature

```python
class TaskConfigException(Exception): ...
```



## TaskData

[Show source in agent_crewai_router.py:72](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py#L72)

#### Signature

```python
class TaskData(BaseModel): ...
```



## add_custom_routes

[Show source in agent_crewai_router.py:82](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/agent_crewai/agent_crewai_router.py#L82)

Add custom routes

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
