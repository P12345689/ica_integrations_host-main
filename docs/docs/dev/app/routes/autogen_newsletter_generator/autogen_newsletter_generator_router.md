# Autogen Newsletter Generator Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Autogen Newsletter Generator](./index.md#autogen-newsletter-generator) / Autogen Newsletter Generator Router

> Auto-generated documentation for [dev.app.routes.autogen_newsletter_generator.autogen_newsletter_generator_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote)
  Default URL as fallback: os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/autogen_newsletter_generator/templates'))


- [Autogen Newsletter Generator Router](#autogen-newsletter-generator-router)
  - [NewsletterInputModel](#newsletterinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [do_newsletter_generation_group_chat](#do_newsletter_generation_group_chat)
  - [get_newsletter](#get_newsletter)
  - [get_newsletter_result](#get_newsletter_result)
  - [stream_newsletter_generator_chat_response](#stream_newsletter_generator_chat_response)

## NewsletterInputModel

[Show source in autogen_newsletter_generator_router.py:51](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py#L51)

Model to validate input data for timestamp generation.

#### Signature

```python
class NewsletterInputModel(BaseModel): ...
```



## OutputModel

[Show source in autogen_newsletter_generator_router.py:68](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py#L68)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in autogen_newsletter_generator_router.py:61](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py#L61)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in autogen_newsletter_generator_router.py:269](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py#L269)

Add custom routes to the FastAPI application for newsletter agent result retrieval.

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
['/autogen_newsletter/result']
```

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## do_newsletter_generation_group_chat

[Show source in autogen_newsletter_generator_router.py:146](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py#L146)

Trigger the newsletter generation group chat.

#### Arguments

- `receive_queue` *asyncio.Queue* - Queue on which the chat messages will be written onto
- `group_chat_manager` *GroupChatManagerWithAsyncQueue* - Group chat manager of the newsletter generation group chat
- `newsletter_proxy` *ConversableAgentWithAsyncQueue* - Proxy of the newsletter generation group chat
- `newsletter_prompt` *str* - Prompt that acts as the initial message of the group chat

#### Signature

```python
async def do_newsletter_generation_group_chat(
    receive_queue: asyncio.Queue,
    group_chat_manager: GroupChatManagerWithAsyncQueue,
    newsletter_proxy: ConversableAgentWithAsyncQueue,
    newsletter_prompt: str,
) -> None: ...
```

#### See also

- [ConversableAgentWithAsyncQueue](../autogen_translator/autogen_integration/web/conversable_agent_with_async_queue.md#conversableagentwithasyncqueue)
- [GroupChatManagerWithAsyncQueue](../autogen_translator/autogen_integration/web/group_chat_manager_with_async_queue.md#groupchatmanagerwithasyncqueue)



## get_newsletter

[Show source in autogen_newsletter_generator_router.py:104](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py#L104)

Run the group chat to generate the newsletter.

Works by using the NGC implementation and storing the agents' outputs in a queue

#### Arguments

- `language` - Language of the newsletter.
- `news_url` - URL of the news page
- `industry` - Industry of interest.
- `email_address` - Email address to send the newsletter to.

#### Returns

- `Union[str,` *None]* - The newsletter in the language.
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the newsletter.

#### Signature

```python
async def get_newsletter(
    language: str, news_url: str, industry: str, email_address: str
) -> Tuple[Union[str, None], List[Dict[str, Any]]]: ...
```



## get_newsletter_result

[Show source in autogen_newsletter_generator_router.py:76](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py#L76)

Look for the final message of the newsletter-generator and also returns the whole chat history.

#### Arguments

- `message_queue` *asyncio.Queue* - The queue containing the chat_history

#### Returns

- `Union[str,` *None]* - The newsletter
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the newsletter.

#### Signature

```python
def get_newsletter_result(
    message_queue: asyncio.Queue,
) -> Tuple[Union[str, None], List[Dict[str, Any]]]: ...
```



## stream_newsletter_generator_chat_response

[Show source in autogen_newsletter_generator_router.py:166](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_newsletter_generator/autogen_newsletter_generator_router.py#L166)

Create the generator which yields the chat messages of the newsletter generator group chat.

#### Arguments

- `language` - Language of the newsletter.
- `news_url` - URL of the news page
- `industry` - Industry of interest.
- `email_address` - Email address to send the newsletter to.

#### Returns

- `Union[str,` *None]* - The newsletter in the language.
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the newsletter.

#### Signature

```python
async def stream_newsletter_generator_chat_response(
    language: str, news_url: str, industry: str, email_address: str
) -> AsyncGenerator[str, None]: ...
```
