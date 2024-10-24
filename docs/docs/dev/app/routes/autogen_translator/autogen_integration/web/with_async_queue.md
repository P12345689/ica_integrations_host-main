# WithAsyncQueue

[ica_integrations_host Index](../../../../../../README.md#ica_integrations_host-index) / [Dev](../../../../../index.md#dev) / [App](../../../../index.md#app) / [Routes](../../../index.md#routes) / [Autogen Translator](../../index.md#autogen-translator) / [Autogen Integration](../index.md#autogen-integration) / [Web](./index.md#web) / WithAsyncQueue

> Auto-generated documentation for [dev.app.routes.autogen_translator.autogen_integration.web.with_async_queue](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/with_async_queue.py) module.

- [WithAsyncQueue](#withasyncqueue)
  - [WithAsyncQueue](#withasyncqueue-1)
    - [WithAsyncQueue()._a_populate_reply](#withasyncqueue()_a_populate_reply)
    - [WithAsyncQueue().set_queues](#withasyncqueue()set_queues)

## WithAsyncQueue

[Show source in with_async_queue.py:13](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/with_async_queue.py#L13)

Provide the functionality to store received messages on a queue.

#### Signature

```python
class WithAsyncQueue: ...
```

### WithAsyncQueue()._a_populate_reply

[Show source in with_async_queue.py:19](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/with_async_queue.py#L19)

Will be called each time this agent receives a message.

It will populate the client_receive_queue with the message and information about the sender

#### Arguments

- `messages` *List[Dict]* - The chat history
- `sender` *Agent* - The sender of the current message
- `config` *Any* - Configuration

#### Returns

- `bool` - Indicates the completion of the chat
Union[str, Dict, None]: Chat history

#### Signature

```python
async def _a_populate_reply(
    self, messages: List[Dict], sender: Agent, config: Optional[Any] = None
) -> Tuple[bool, Union[str, Dict, None]]: ...
```

### WithAsyncQueue().set_queues

[Show source in with_async_queue.py:46](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/with_async_queue.py#L46)

Initialize the asyncio queues.

#### Arguments

- [client_receive_queue](#withasyncqueue) *asyncio.Queue* - Queue on which the agents' messages will be saved
- [client_sent_queue](#withasyncqueue) *asyncio.Queue* - Queue on which the user's messages will be read from

#### Signature

```python
def set_queues(
    self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue
) -> None: ...
```
