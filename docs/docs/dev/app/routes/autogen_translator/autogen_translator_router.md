# Autogen Translator Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Autogen Translator](./index.md#autogen-translator) / Autogen Translator Router

> Auto-generated documentation for [dev.app.routes.autogen_translator.autogen_translator_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/autogen_translator/templates'))


- [Autogen Translator Router](#autogen-translator-router)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [TranslationInputModel](#translationinputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [do_translation_group_chat](#do_translation_group_chat)
  - [get_text_translation](#get_text_translation)
  - [get_translation_result](#get_translation_result)
  - [stream_translation_chat_response](#stream_translation_chat_response)

## OutputModel

[Show source in autogen_translator_router.py:63](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py#L63)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in autogen_translator_router.py:56](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py#L56)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## TranslationInputModel

[Show source in autogen_translator_router.py:48](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py#L48)

Model to validate input data for timestamp generation.

#### Signature

```python
class TranslationInputModel(BaseModel): ...
```



## add_custom_routes

[Show source in autogen_translator_router.py:261](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py#L261)

Add custom routes to the FastAPI application for translator agent result retrieval.

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
['/autogen_translator/result']
```

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## do_translation_group_chat

[Show source in autogen_translator_router.py:140](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py#L140)

Trigger the translation group chat.

#### Arguments

- `receive_queue` *asyncio.Queue* - Queue on which the chat messages will be written onto
- `group_chat_manager` *GroupChatManagerWithAsyncQueue* - Group chat manager of the translation group chat
- `translation_proxy` *ConversableAgentWithAsyncQueue* - Proxy of the translation group chat
- `translation_prompt` *str* - Prompt that acts as the initial message of the group chat

#### Signature

```python
async def do_translation_group_chat(
    receive_queue: asyncio.Queue,
    group_chat_manager: GroupChatManagerWithAsyncQueue,
    translation_proxy: ConversableAgentWithAsyncQueue,
    translation_prompt: str,
) -> None: ...
```

#### See also

- [ConversableAgentWithAsyncQueue](autogen_integration/web/conversable_agent_with_async_queue.md#conversableagentwithasyncqueue)
- [GroupChatManagerWithAsyncQueue](autogen_integration/web/group_chat_manager_with_async_queue.md#groupchatmanagerwithasyncqueue)



## get_text_translation

[Show source in autogen_translator_router.py:96](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py#L96)

Run the group chat to generate the translation.

Works by using the NGC implementation and storing the agents' outputs in a queue

#### Arguments

- `text` *str* - The text to be translated
- `language_from` *str* - Source language of the text to be translated
- `language_to` *str* - Target language to translate to

#### Returns

- `Union[str,` *None]* - The translated text in the target language
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the translation

#### Signature

```python
async def get_text_translation(
    text: str, language_from: str, language_to: str
) -> Tuple[Union[str, None], List[Dict[str, Any]]]: ...
```



## get_translation_result

[Show source in autogen_translator_router.py:71](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py#L71)

Look for the final message of the translator and also returns the whole chat history.

#### Arguments

- `message_queue` *asyncio.Queue* - The queue containing the chat_history

#### Returns

- `Union[str,` *None]* - The translated text in the target language
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the translation

#### Signature

```python
def get_translation_result(
    message_queue: asyncio.Queue,
) -> Tuple[Union[str, None], List[Dict[str, Any]]]: ...
```



## stream_translation_chat_response

[Show source in autogen_translator_router.py:160](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_translator_router.py#L160)

Create the generator which yields the chat messages of the translation group chat.

#### Arguments

- `text` *str* - The text to be translated
- `language_from` *str* - Source language of the text to be translated
- `language_to` *str* - Target language to translate to

#### Returns

- `AsyncGenerator[str,` *None]* - Generator with the JSON strings of the message objects of the translation group chat

#### Signature

```python
async def stream_translation_chat_response(
    text: str, language_from: str, language_to: str
) -> AsyncGenerator[str, None]: ...
```
