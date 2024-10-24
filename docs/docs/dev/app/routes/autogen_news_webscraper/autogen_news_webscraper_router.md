# Autogen News Webscraper Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Autogen News Webscraper](./index.md#autogen-news-webscraper) / Autogen News Webscraper Router

> Auto-generated documentation for [dev.app.routes.autogen_news_webscraper.autogen_news_webscraper_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('dev/app/routes/autogen_news_webscraper/templates'))


- [Autogen News Webscraper Router](#autogen-news-webscraper-router)
  - [NewsWebscrapingInputModel](#newswebscrapinginputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [do_webscraping_group_chat](#do_webscraping_group_chat)
  - [get_text_news_webscraping](#get_text_news_webscraping)
  - [get_webscraping_result](#get_webscraping_result)
  - [stream_news_webscraping_chat_response](#stream_news_webscraping_chat_response)

## NewsWebscrapingInputModel

[Show source in autogen_news_webscraper_router.py:48](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py#L48)

Model to validate input data for timestamp generation.

#### Signature

```python
class NewsWebscrapingInputModel(BaseModel): ...
```



## OutputModel

[Show source in autogen_news_webscraper_router.py:62](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py#L62)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in autogen_news_webscraper_router.py:55](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py#L55)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in autogen_news_webscraper_router.py:255](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py#L255)

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
['/autogen_news_webscraper/result']
```

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## do_webscraping_group_chat

[Show source in autogen_news_webscraper_router.py:138](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py#L138)

Trigger the news webscraping group chat.

#### Arguments

- `receive_queue` *asyncio.Queue* - Queue on which the chat messages will be written onto
- `group_chat_manager` *GroupChatManagerWithAsyncQueue* - Group chat manager of the news webscraping group chat
- `webscraping_proxy` *ConversableAgentWithAsyncQueue* - Proxy of the news webscraping group chat
- `webscraping_prompt` *str* - Prompt that acts as the initial message of the group chat

#### Signature

```python
async def do_webscraping_group_chat(
    receive_queue: asyncio.Queue,
    group_chat_manager: GroupChatManagerWithAsyncQueue,
    webscraping_proxy: ConversableAgentWithAsyncQueue,
    webscraping_prompt: str,
) -> None: ...
```

#### See also

- [ConversableAgentWithAsyncQueue](../autogen_translator/autogen_integration/web/conversable_agent_with_async_queue.md#conversableagentwithasyncqueue)
- [GroupChatManagerWithAsyncQueue](../autogen_translator/autogen_integration/web/group_chat_manager_with_async_queue.md#groupchatmanagerwithasyncqueue)



## get_text_news_webscraping

[Show source in autogen_news_webscraper_router.py:101](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py#L101)

Run the group chat to generate the webscraping result.

Works by using the NGC implementation and storing the agents' outputs in a queue

#### Arguments

- `text` *str* - The text to be translated
- `language_from` *str* - Source language of the text to be translated
- `language_to` *str* - Target language to translate to

#### Returns

- `Union[str,` *None]* - The translated text in the target language
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the webscraping result

#### Signature

```python
async def get_text_news_webscraping(
    news_url: str, industry: str
) -> Tuple[Union[str, None], List[Dict[str, Any]]]: ...
```



## get_webscraping_result

[Show source in autogen_news_webscraper_router.py:70](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py#L70)

Look for the final message of the translator and also returns the whole chat history.

#### Arguments

- `message_queue` *asyncio.Queue* - The queue containing the chat_history

#### Returns

- `Union[str,` *None]* - The translated text in the target language
- `List[Dict[str,` *Any]]* - The chat history of the agents that worked to generate the scraped results

#### Signature

```python
def get_webscraping_result(
    message_queue: asyncio.Queue,
) -> Tuple[Union[str, None], List[Dict[str, Any]]]: ...
```



## stream_news_webscraping_chat_response

[Show source in autogen_news_webscraper_router.py:158](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_news_webscraper/autogen_news_webscraper_router.py#L158)

Create the generator which yields the chat messages of the news webscraping group chat.

#### Arguments

- `news_url` *str* - The URL to scrape and get the news from
- `industry` *str* - The industry of interest

#### Returns

- `AsyncGenerator[str,` *None]* - Generator with the JSON strings of the message objects of the news webscraping group chat

#### Signature

```python
async def stream_news_webscraping_chat_response(
    news_url: str, industry: str
) -> AsyncGenerator[str, None]: ...
```
