# Agent Copilot Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Agent Copilot](./index.md#agent-copilot) / Agent Copilot Router

> Auto-generated documentation for [app.routes.agent_copilot.agent_copilot_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_copilot/agent_copilot_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `AGENT_COPILOT_ENDPOINT` - Load environment variables: os.getenv('AGENT_COPILOT_ENDPOINT', 'https://va-gpt-4omni.openai.azure.com/')

- `AVAILABLE_ASSISTANTS` - Define available assistants: {'appmod': 'asst_u60Wef7HJOWjHuOV6nhuBHsS', 'migration': 'asst_xfL12XBmKIM2pfzeMMOiQz3e'}

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/agent_copilot/templates'))


- [Agent Copilot Router](#agent-copilot-router)
  - [ConversationInputModel](#conversationinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [agent_copilot_request](#agent_copilot_request)
  - [create_thread_and_run](#create_thread_and_run)

## ConversationInputModel

[Show source in agent_copilot_router.py:46](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_copilot/agent_copilot_router.py#L46)

Model to validate input data for the conversation.

#### Signature

```python
class ConversationInputModel(BaseModel): ...
```



## OutputModel

[Show source in agent_copilot_router.py:55](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_copilot/agent_copilot_router.py#L55)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in agent_copilot_router.py:50](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_copilot/agent_copilot_router.py#L50)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in agent_copilot_router.py:141](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_copilot/agent_copilot_router.py#L141)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## agent_copilot_request

[Show source in agent_copilot_router.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_copilot/agent_copilot_router.py#L61)

Make a request to the Agent Copilot API.

#### Arguments

- `method` *str* - HTTP method (GET, POST, etc.)
- `endpoint` *str* - API endpoint
- `data` *Dict, optional* - Request payload

#### Returns

- `Dict` - API response

#### Raises

- `HTTPException` - If the API request fails

#### Signature

```python
def agent_copilot_request(method: str, endpoint: str, data: Dict = None) -> Dict: ...
```



## create_thread_and_run

[Show source in agent_copilot_router.py:91](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_copilot/agent_copilot_router.py#L91)

Create a new thread, send a message, and run the assistant.

#### Arguments

- `assistant_id` *str* - The ID of the assistant to use
- `message` *str* - The initial message to start the conversation

#### Returns

- `Dict` - The result of the assistant run

#### Raises

- `HTTPException` - If any step in the process fails

#### Signature

```python
async def create_thread_and_run(assistant_id: str, message: str) -> Dict: ...
```
