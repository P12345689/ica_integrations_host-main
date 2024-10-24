# UserProxyAgentWithAsyncQueue

[ica_integrations_host Index](../../../../../../README.md#ica_integrations_host-index) / [Dev](../../../../../index.md#dev) / [App](../../../../index.md#app) / [Routes](../../../index.md#routes) / [Autogen Translator](../../index.md#autogen-translator) / [Autogen Integration](../index.md#autogen-integration) / [Web](./index.md#web) / UserProxyAgentWithAsyncQueue

> Auto-generated documentation for [dev.app.routes.autogen_translator.autogen_integration.web.user_proxy_agent_with_async_queue](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/user_proxy_agent_with_async_queue.py) module.

- [UserProxyAgentWithAsyncQueue](#userproxyagentwithasyncqueue)
  - [UserProxyAgentWithAsyncQueue](#userproxyagentwithasyncqueue-1)
    - [UserProxyAgentWithAsyncQueue().a_check_termination_and_human_reply](#userproxyagentwithasyncqueue()a_check_termination_and_human_reply)
    - [UserProxyAgentWithAsyncQueue().a_get_human_input](#userproxyagentwithasyncqueue()a_get_human_input)

## UserProxyAgentWithAsyncQueue

[Show source in user_proxy_agent_with_async_queue.py:16](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/user_proxy_agent_with_async_queue.py#L16)

Class that inherits autogen's UserProxyAgent to provide async messaging functionality via asyncio queues.

#### Signature

```python
class UserProxyAgentWithAsyncQueue(WithAsyncQueue, UserProxyAgent):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
```

#### See also

- [WithAsyncQueue](./with_async_queue.md#withasyncqueue)

### UserProxyAgentWithAsyncQueue().a_check_termination_and_human_reply

[Show source in user_proxy_agent_with_async_queue.py:32](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/user_proxy_agent_with_async_queue.py#L32)

Check if the conversation should be terminated, and if human reply is provided.

#### Arguments

- `messages` *List[Dict]* - Chat history
- `sender` *Agent* - Sender of the current message
- `config` *Any* - Configuration

#### Returns

- `bool` - Indicates the completion of the chat
Union[str, Dict, None]: Chat history

#### Signature

```python
async def a_check_termination_and_human_reply(
    self,
    messages: Optional[List[Dict]] = None,
    sender: Optional[Agent] = None,
    config: Optional[Any] = None,
) -> Tuple[bool, Union[str, Dict, None]]: ...
```

### UserProxyAgentWithAsyncQueue().a_get_human_input

[Show source in user_proxy_agent_with_async_queue.py:115](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/autogen_translator/autogen_integration/web/user_proxy_agent_with_async_queue.py#L115)

Inherits autogen's method.

Instead of waiting for console input it will read from the client_sent_queue and send the first element of the
queue to autogen.

#### Arguments

- `prompt` *str* - Message received

#### Returns

- `str` - Message to send back to autogen

#### Signature

```python
async def a_get_human_input(self, prompt: str) -> str: ...
```
