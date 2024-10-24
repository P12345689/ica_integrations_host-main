# Autogen Mail Generator Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [autogen_mail_generator Integration](./index.md#autogen_mail_generator-integration) / Autogen Mail Generator Router

> Auto-generated documentation for [dev.app.routes.autogen_mail_generator.autogen_mail_generator_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote)
  Default URL as fallback: os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/autogen_mail_generator/templates'))


- [Autogen Mail Generator Router](#autogen-mail-generator-router)
  - [EmailGenarationInputModel](#emailgenarationinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [do_mail_generation_group_chat](#do_mail_generation_group_chat)
  - [get_email_generation](#get_email_generation)
  - [get_email_generation_result](#get_email_generation_result)
  - [stream_mail_generation_chat_response](#stream_mail_generation_chat_response)

## EmailGenarationInputModel

[Show source in autogen_mail_generator_router.py:53](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py#L53)

Model to validate input data for timestamp generation.

#### Signature

```python
class EmailGenarationInputModel(BaseModel): ...
```



## OutputModel

[Show source in autogen_mail_generator_router.py:67](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py#L67)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in autogen_mail_generator_router.py:60](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py#L60)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in autogen_mail_generator_router.py:265](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py#L265)

Add custom routes to the FastAPI application for email generator agent result retrieval.

#### Arguments

- [App](../../../../app/index.md#app) *FastAPI* - The FastAPI application to which the routes will be added.

#### Returns

None

#### Examples

```python
>>> from fastapi import FastAPI
>>> app = FastAPI()
>>> add_custom_routes(app)
>>> [route.path for route in app.routes]
['/autogen_mail_generator/result']
```

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## do_mail_generation_group_chat

[Show source in autogen_mail_generator_router.py:144](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py#L144)

Trigger the mail generation group chat.

#### Arguments

- `receive_queue` *asyncio.Queue* - Queue on which the chat messages will be written onto
- `group_chat_manager` *GroupChatManagerWithAsyncQueue* - Group chat manager of the mail generation group chat
- `mail_generation_proxy` *ConversableAgentWithAsyncQueue* - Proxy of the mail generation group chat
- `mail_generation_prompt` *str* - Prompt that acts as the initial message of the group chat

#### Signature

```python
async def do_mail_generation_group_chat(
    receive_queue: asyncio.Queue,
    group_chat_manager: GroupChatManagerWithAsyncQueue,
    mail_generation_proxy: ConversableAgentWithAsyncQueue,
    mail_generation_prompt: str,
) -> None: ...
```

#### See also

- [ConversableAgentWithAsyncQueue](../autogen_translator/autogen_integration/web/conversable_agent_with_async_queue.md#conversableagentwithasyncqueue)
- [GroupChatManagerWithAsyncQueue](../autogen_translator/autogen_integration/web/group_chat_manager_with_async_queue.md#groupchatmanagerwithasyncqueue)



## get_email_generation

[Show source in autogen_mail_generator_router.py:106](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py#L106)

Run the group chat to generate the email.

Works by using the NGC implementation and storing the agents' outputs in a queue

#### Arguments

- `text` *str* - Content from which to base the email
- `recipient_email_address` *str* - Recipient's email address

#### Returns

- `Union[str,` *None]* - The sent email text
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the email

#### Signature

```python
async def get_email_generation(
    text: str, recipient_email_address: str
) -> Tuple[Union[str, None], List[Dict[str, Any]]]: ...
```



## get_email_generation_result

[Show source in autogen_mail_generator_router.py:75](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py#L75)

Look for the final message of the mail generator and also returns the whole chat history.

#### Arguments

- `message_queue` *asyncio.Queue* - The queue containing the chat_history

#### Returns

- `Union[str,` *None]* - The sent email text
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the email

#### Signature

```python
def get_email_generation_result(
    message_queue: asyncio.Queue,
) -> Tuple[Union[str, None], List[Dict[str, Any]]]: ...
```



## stream_mail_generation_chat_response

[Show source in autogen_mail_generator_router.py:164](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_mail_generator/autogen_mail_generator_router.py#L164)

Create the generator which yields the chat messages of the email generation group chat.

Works by using the NGC implementation and storing the agents' outputs in a queue

#### Arguments

- `text` *str* - Content from which to base the email
- `recipient_email_address` *str* - Recipient's email address

#### Returns

- `AsyncGenerator[str,` *None]* - Generator with the JSON strings of the message objects of the email generation group chat

#### Signature

```python
async def stream_mail_generation_chat_response(
    text: str, recipient_email_address: str
) -> AsyncGenerator[str, None]: ...
```
