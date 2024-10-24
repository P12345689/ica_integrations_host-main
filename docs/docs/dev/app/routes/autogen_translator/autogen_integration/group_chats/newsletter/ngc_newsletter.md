# Ngc Newsletter

[ica_integrations_host Index](../../../../../../../README.md#ica_integrations_host-index) / [Dev](../../../../../../index.md#dev) / [App](../../../../../index.md#app) / [Routes](../../../../index.md#routes) / [Autogen Translator](../../../index.md#autogen-translator) / [Autogen Integration](../../index.md#autogen-integration) / [Group Chats](../index.md#group-chats) / [Newsletter](./index.md#newsletter) / Ngc Newsletter

> Auto-generated documentation for [dev.app.routes.autogen_translator.autogen_integration.group_chats.newsletter.ngc_newsletter](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/newsletter/ngc_newsletter.py) module.

- [Ngc Newsletter](#ngc-newsletter)
  - [NewsletterNGC](#newsletterngc)
    - [NewsletterNGC.__load_agents_config](#newsletterngc__load_agents_config)
    - [NewsletterNGC().__register_functions](#newsletterngc()__register_functions)
    - [NewsletterNGC().__setup_agents](#newsletterngc()__setup_agents)
    - [NewsletterNGC().__setup_group_chat](#newsletterngc()__setup_group_chat)
    - [NewsletterNGC().get_manager](#newsletterngc()get_manager)
    - [NewsletterNGC().get_proxy](#newsletterngc()get_proxy)

## NewsletterNGC

[Show source in ngc_newsletter.py:28](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/newsletter/ngc_newsletter.py#L28)

Class that contains the agents that are setup in an autogen group chat.

The configuration is loaded automatically from agents_config.json.
It is necessary to call set_queues to populate the asyncio queues used for async input and output of messages.

#### Signature

```python
class NewsletterNGC:
    def __init__(
        self,
        client_receive_queue: asyncio.Queue,
        client_sent_queue: asyncio.Queue,
        industry: str,
        recipient_email_address: str,
    ): ...
```

### NewsletterNGC.__load_agents_config

[Show source in ngc_newsletter.py:55](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/newsletter/ngc_newsletter.py#L55)

Load the agents config from the local JSON file.

#### Returns

- `Dict[str,` *Any]* - agents configuration

#### Signature

```python
@staticmethod
def __load_agents_config() -> Dict[str, Any]: ...
```

### NewsletterNGC().__register_functions

[Show source in ngc_newsletter.py:163](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/newsletter/ngc_newsletter.py#L163)

Register functions.

#### Signature

```python
def __register_functions(self) -> None: ...
```

### NewsletterNGC().__setup_agents

[Show source in ngc_newsletter.py:68](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/newsletter/ngc_newsletter.py#L68)

Set up all the agents.

#### Arguments

- `client_receive_queue` *asyncio.Queue* - Queue on which the agents' messages will be saved
- `client_sent_queue` *asyncio.Queue* - Queue on which the user's messages will be read from

#### Signature

```python
def __setup_agents(
    self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue
) -> None: ...
```

### NewsletterNGC().__setup_group_chat

[Show source in ngc_newsletter.py:98](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/newsletter/ngc_newsletter.py#L98)

Set up the group chat.

#### Arguments

- `client_receive_queue` *asyncio.Queue* - Queue on which the agents' messages will be saved
- `client_sent_queue` *asyncio.Queue* - Queue on which the user's messages will be read from

#### Signature

```python
def __setup_group_chat(
    self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue
) -> None: ...
```

### NewsletterNGC().get_manager

[Show source in ngc_newsletter.py:167](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/newsletter/ngc_newsletter.py#L167)

Retrieve the GroupChatWebManager.

#### Returns

- `GroupChatManagerWithAsyncQueue` - the group chat manager of the underlying group chat

#### Signature

```python
def get_manager(self) -> GroupChatManagerWithAsyncQueue: ...
```

#### See also

- [GroupChatManagerWithAsyncQueue](../../web/group_chat_manager_with_async_queue.md#groupchatmanagerwithasyncqueue)

### NewsletterNGC().get_proxy

[Show source in ngc_newsletter.py:176](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/newsletter/ngc_newsletter.py#L176)

Retrieve the proxy of the underlying group chat.

#### Returns

- `ConversableAgentWithAsyncQueue` - the proxy of the underlying group chat

#### Signature

```python
def get_proxy(self) -> ConversableAgentWithAsyncQueue: ...
```

#### See also

- [ConversableAgentWithAsyncQueue](../../web/conversable_agent_with_async_queue.md#conversableagentwithasyncqueue)
