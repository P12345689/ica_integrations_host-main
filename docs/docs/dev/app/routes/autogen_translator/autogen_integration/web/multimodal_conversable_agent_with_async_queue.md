# MultimodalConversableAgentWithAsyncQueue

[ica_integrations_host Index](../../../../../../README.md#ica_integrations_host-index) / [Dev](../../../../../index.md#dev) / [App](../../../../index.md#app) / [Routes](../../../index.md#routes) / [Autogen Translator](../../index.md#autogen-translator) / [Autogen Integration](../index.md#autogen-integration) / [Web](./index.md#web) / MultimodalConversableAgentWithAsyncQueue

> Auto-generated documentation for [dev.app.routes.autogen_translator.autogen_integration.web.multimodal_conversable_agent_with_async_queue](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/multimodal_conversable_agent_with_async_queue.py) module.

- [MultimodalConversableAgentWithAsyncQueue](#multimodalconversableagentwithasyncqueue)
  - [MultimodalConversableAgentWithAsyncQueue](#multimodalconversableagentwithasyncqueue-1)
    - [MultimodalConversableAgentWithAsyncQueue._a_summary_from_nested_chats](#multimodalconversableagentwithasyncqueue_a_summary_from_nested_chats)
    - [MultimodalConversableAgentWithAsyncQueue().register_nested_chats](#multimodalconversableagentwithasyncqueue()register_nested_chats)

## MultimodalConversableAgentWithAsyncQueue

[Show source in multimodal_conversable_agent_with_async_queue.py:15](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/multimodal_conversable_agent_with_async_queue.py#L15)

Class that inherits autogen's MultimodalConversableAgent to provide async messaging functionality via asyncio
queues.

#### Signature

```python
class MultimodalConversableAgentWithAsyncQueue(
    WithAsyncQueue, MultimodalConversableAgent
):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
```

#### See also

- [WithAsyncQueue](./with_async_queue.md#withasyncqueue)

### MultimodalConversableAgentWithAsyncQueue._a_summary_from_nested_chats

[Show source in multimodal_conversable_agent_with_async_queue.py:26](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/multimodal_conversable_agent_with_async_queue.py#L26)

Inherits autogen's method such that nested chats are registered asynchronously.

#### Arguments

chat_queue (List[Dict[str, Any]]): Chat history
recipient (Agent):
messages (Union[str, Callable]): Chat messages of current nested chat
- `sender` *Agent* - Sender of the current message
- `config` *Any* - Configuration

#### Returns

- `bool` - Indicates the completion of the chat
- `str` - Summary of the last chat if any chats were initiated

#### Signature

```python
@staticmethod
async def _a_summary_from_nested_chats(
    chat_queue: List[Dict[str, Any]],
    recipient: Agent,
    messages: List[Dict],
    sender: Agent,
    config: Any,
) -> Tuple[bool, Union[str, None]]: ...
```

### MultimodalConversableAgentWithAsyncQueue().register_nested_chats

[Show source in multimodal_conversable_agent_with_async_queue.py:77](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/multimodal_conversable_agent_with_async_queue.py#L77)

Inherits autogen's method to provide functionality to register nested chats.

#### Arguments

chat_queue (List[Dict[str, Any]]): Chat history
trigger (Union[Type[Agent], str, Agent, Callable[[Agent], bool], List]): Other agent who will trigger a nested chats if sending message to this agent
reply_func_from_nested_chats (Union[str, Callable]): Function used to get summary/reply of nested chat
- `position` *int* - Ref to `register_reply` for details. Default to 2. It means we first check the termination and human reply, then check the registered nested chat reply.

#### Signature

```python
def register_nested_chats(
    self,
    chat_queue: List[Dict[str, Any]],
    trigger: Union[Type[Agent], str, Agent, Callable[[Agent], bool], List],
    reply_func_from_nested_chats: Union[str, Callable] = "summary_from_nested_chats",
    position: int = 2,
    **kwargs: Any
) -> None: ...
```
