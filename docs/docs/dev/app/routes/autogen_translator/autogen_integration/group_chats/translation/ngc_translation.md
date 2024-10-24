# Ngc Translation

[ica_integrations_host Index](../../../../../../../README.md#ica_integrations_host-index) / [Dev](../../../../../../index.md#dev) / [App](../../../../../index.md#app) / [Routes](../../../../index.md#routes) / [Autogen Translator](../../../index.md#autogen-translator) / [Autogen Integration](../../index.md#autogen-integration) / [Group Chats](../index.md#group-chats) / [Translation](./index.md#translation) / Ngc Translation

> Auto-generated documentation for [dev.app.routes.autogen_translator.autogen_integration.group_chats.translation.ngc_translation](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/translation/ngc_translation.py) module.

- [Ngc Translation](#ngc-translation)
  - [TranslationNGC](#translationngc)
    - [TranslationNGC.__load_agents_config](#translationngc__load_agents_config)
    - [TranslationNGC().__register_functions](#translationngc()__register_functions)
    - [TranslationNGC().__setup_agents](#translationngc()__setup_agents)
    - [TranslationNGC().__setup_group_chat](#translationngc()__setup_group_chat)
    - [TranslationNGC().get_manager](#translationngc()get_manager)
    - [TranslationNGC().get_proxy](#translationngc()get_proxy)

## TranslationNGC

[Show source in ngc_translation.py:22](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/translation/ngc_translation.py#L22)

Class that contains the agents that are setup in an autogen group chat.

The configuration is loaded automatically from the jinja templates
It is necessary to call set_queues to populate the asyncio queues used for async input and output of messages.

#### Signature

```python
class TranslationNGC:
    def __init__(
        self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue
    ): ...
```

### TranslationNGC.__load_agents_config

[Show source in ngc_translation.py:45](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/translation/ngc_translation.py#L45)

Load the agents config from the local JSON file.

#### Returns

- `Dict[str,` *Any]* - agents configuration

#### Signature

```python
@staticmethod
def __load_agents_config() -> Dict[str, Any]: ...
```

### TranslationNGC().__register_functions

[Show source in ngc_translation.py:139](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/translation/ngc_translation.py#L139)

Register functions.

#### Signature

```python
def __register_functions(self) -> None: ...
```

### TranslationNGC().__setup_agents

[Show source in ngc_translation.py:59](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/translation/ngc_translation.py#L59)

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

### TranslationNGC().__setup_group_chat

[Show source in ngc_translation.py:101](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/translation/ngc_translation.py#L101)

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

### TranslationNGC().get_manager

[Show source in ngc_translation.py:143](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/translation/ngc_translation.py#L143)

Retrieve the GroupChatWebManager.

#### Returns

- `GroupChatManagerWithAsyncQueue` - the group chat manager of the underlying group chat

#### Signature

```python
def get_manager(self) -> GroupChatManagerWithAsyncQueue: ...
```

#### See also

- [GroupChatManagerWithAsyncQueue](../../web/group_chat_manager_with_async_queue.md#groupchatmanagerwithasyncqueue)

### TranslationNGC().get_proxy

[Show source in ngc_translation.py:152](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/translation/ngc_translation.py#L152)

Retrieve the proxy of the underlying group chat.

#### Returns

- `ConversableAgentWithAsyncQueue` - the proxy of the underlying group chat

#### Signature

```python
def get_proxy(self) -> ConversableAgentWithAsyncQueue: ...
```

#### See also

- [ConversableAgentWithAsyncQueue](../../web/conversable_agent_with_async_queue.md#conversableagentwithasyncqueue)
