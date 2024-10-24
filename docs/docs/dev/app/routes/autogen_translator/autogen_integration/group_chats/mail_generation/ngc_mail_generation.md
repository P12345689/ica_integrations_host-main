# Ngc Mail Generation

[ica_integrations_host Index](../../../../../../../README.md#ica_integrations_host-index) / [Dev](../../../../../../index.md#dev) / [App](../../../../../index.md#app) / [Routes](../../../../index.md#routes) / [Autogen Translator](../../../index.md#autogen-translator) / [Autogen Integration](../../index.md#autogen-integration) / [Group Chats](../index.md#group-chats) / [Mail Generation](./index.md#mail-generation) / Ngc Mail Generation

> Auto-generated documentation for [dev.app.routes.autogen_translator.autogen_integration.group_chats.mail_generation.ngc_mail_generation](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py) module.

#### Attributes

- `Subject` - Defining custom type annotations for the send_email() tool function's parameters: Annotated[str, 'The subject of the email']


- [Ngc Mail Generation](#ngc-mail-generation)
  - [EmailNGC](#emailngc)
    - [EmailNGC.__load_agents_config](#emailngc__load_agents_config)
    - [EmailNGC().__register_functions](#emailngc()__register_functions)
    - [EmailNGC().__setup_agents](#emailngc()__setup_agents)
    - [EmailNGC().__setup_group_chat](#emailngc()__setup_group_chat)
    - [EmailNGC().get_manager](#emailngc()get_manager)
    - [EmailNGC().get_proxy](#emailngc()get_proxy)
  - [send_mail](#send_mail)
  - [template_html](#template_html)

## EmailNGC

[Show source in ngc_mail_generation.py:149](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L149)

Class that contains the agents that are setup in an autogen group chat.

The configuration is loaded automatically from the jinja templates
It is necessary to call set_queues to populate the asyncio queues used for async input and output of messages.

#### Signature

```python
class EmailNGC:
    def __init__(
        self,
        client_receive_queue: asyncio.Queue,
        client_sent_queue: asyncio.Queue,
        recipient_email_address: str,
    ) -> None: ...
```

### EmailNGC.__load_agents_config

[Show source in ngc_mail_generation.py:191](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L191)

Load the agents config from the local JSON file.

#### Returns

- `Dict[str,` *Any]* - agents configuration

#### Signature

```python
@staticmethod
def __load_agents_config() -> Dict[str, Any]: ...
```

### EmailNGC().__register_functions

[Show source in ngc_mail_generation.py:348](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L348)

Register Functions.

#### Signature

```python
def __register_functions(self) -> None: ...
```

### EmailNGC().__setup_agents

[Show source in ngc_mail_generation.py:204](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L204)

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

### EmailNGC().__setup_group_chat

[Show source in ngc_mail_generation.py:267](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L267)

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

### EmailNGC().get_manager

[Show source in ngc_mail_generation.py:358](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L358)

Retrieve the GroupChatWebManager.

#### Returns

- `GroupChatManagerWithAsyncQueue` - the group chat manager of the underlying group chat

#### Signature

```python
def get_manager(self) -> GroupChatManagerWithAsyncQueue: ...
```

#### See also

- [GroupChatManagerWithAsyncQueue](../../web/group_chat_manager_with_async_queue.md#groupchatmanagerwithasyncqueue)

### EmailNGC().get_proxy

[Show source in ngc_mail_generation.py:367](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L367)

Retrieve the proxy of the underlying group chat.

#### Returns

- `ConversableAgentWithAsyncQueue` - the proxy of the underlying group chat

#### Signature

```python
def get_proxy(self) -> ConversableAgentWithAsyncQueue: ...
```

#### See also

- [ConversableAgentWithAsyncQueue](../../web/conversable_agent_with_async_queue.md#conversableagentwithasyncqueue)



## send_mail

[Show source in ngc_mail_generation.py:75](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L75)

Send an email with a given subject, body, and recipient email.

#### Arguments

- `subject` *Subject* - The subject of the email.
- `body` *Body* - The body of the email.
- `to_email` *ToEmail* - The recipient's email address.

#### Returns

- `str` - A success message if the email is sent successfully, or an error message if there's an error.

#### Signature

```python
def send_mail(subject: Subject, body: Body, to_email: ToEmail) -> str: ...
```

#### See also

- [Body](#body)
- [Subject](#subject)
- [ToEmail](#toemail)



## template_html

[Show source in ngc_mail_generation.py:35](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/group_chats/mail_generation/ngc_mail_generation.py#L35)

Generate an HTML template for the email content.

#### Arguments

- `body` *str* - The body of the email:

#### Signature

```python
def template_html(body: str) -> str: ...
```
