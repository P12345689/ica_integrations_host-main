# Ngc Webscraping

[ica_integrations_host Index](../../../../../../../README.md#ica_integrations_host-index) / [Dev](../../../../../../index.md#dev) / [App](../../../../../index.md#app) / [Routes](../../../../index.md#routes) / [Autogen Translator](../../../index.md#autogen-translator) / [Autogen Integration](../../index.md#autogen-integration) / [Group Chats](../index.md#group-chats) / [Webscraping](./index.md#webscraping) / Ngc Webscraping

> Auto-generated documentation for [dev.app.routes.autogen_translator.autogen_integration.group_chats.webscraping.ngc_webscraping](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/ngc_webscraping.py) module.

- [Ngc Webscraping](#ngc-webscraping)
  - [WebscrapingNGC](#webscrapingngc)
    - [WebscrapingNGC().__register_functions](#webscrapingngc()__register_functions)
    - [WebscrapingNGC().__setup_agents](#webscrapingngc()__setup_agents)
    - [WebscrapingNGC().__setup_group_chat](#webscrapingngc()__setup_group_chat)
    - [WebscrapingNGC().get_manager](#webscrapingngc()get_manager)
    - [WebscrapingNGC().get_proxy](#webscrapingngc()get_proxy)
  - [scrape_page](#scrape_page)

## WebscrapingNGC

[Show source in ngc_webscraping.py:90](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/ngc_webscraping.py#L90)

#### Signature

```python
class WebscrapingNGC:
    def __init__(
        self,
        client_receive_queue: asyncio.Queue,
        client_sent_queue: asyncio.Queue,
        industry: str,
    ) -> None: ...
```

### WebscrapingNGC().__register_functions

[Show source in ngc_webscraping.py:205](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/ngc_webscraping.py#L205)

Register Functions

#### Signature

```python
def __register_functions(self) -> None: ...
```

### WebscrapingNGC().__setup_agents

[Show source in ngc_webscraping.py:111](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/ngc_webscraping.py#L111)

Setup all the agents

#### Signature

```python
def __setup_agents(self, client_receive_queue, client_sent_queue) -> None: ...
```

### WebscrapingNGC().__setup_group_chat

[Show source in ngc_webscraping.py:169](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/ngc_webscraping.py#L169)

Setup The Group Chat based on StateFlow

#### Signature

```python
def __setup_group_chat(self, client_receive_queue, client_sent_queue) -> None: ...
```

### WebscrapingNGC().get_manager

[Show source in ngc_webscraping.py:220](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/ngc_webscraping.py#L220)

Retrieve the GroupChatWebManager.

#### Returns

- `GroupChatManagerWithAsyncQueue` - the group chat manager of the underlying group chat

#### Signature

```python
def get_manager(self) -> GroupChatManagerWithAsyncQueue: ...
```

#### See also

- [GroupChatManagerWithAsyncQueue](../../web/group_chat_manager_with_async_queue.md#groupchatmanagerwithasyncqueue)

### WebscrapingNGC().get_proxy

[Show source in ngc_webscraping.py:229](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/ngc_webscraping.py#L229)

Retrieve the proxy of the underlying group chat.

#### Returns

- `ConversableAgentWithAsyncQueue` - the proxy of the underlying group chat

#### Signature

```python
def get_proxy(self) -> ConversableAgentWithAsyncQueue: ...
```

#### See also

- [ConversableAgentWithAsyncQueue](../../web/conversable_agent_with_async_queue.md#conversableagentwithasyncqueue)



## scrape_page

[Show source in ngc_webscraping.py:21](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/ngc_webscraping.py#L21)

Scrape multiple URLs provided in the kwargs dictionary  and return the scraped content.

#### Arguments

- `kwargs` - Dictionary containing headlines and their URLs.
:type kwargs: dict

#### Returns

A dictionary with headlines as keys and their summaries as values.
Type: *dict*

#### Signature

```python
def scrape_page(**kwargs: Dict[str, Any]) -> str: ...
```
