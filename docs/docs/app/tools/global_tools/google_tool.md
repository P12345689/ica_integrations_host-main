# Google Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Google Tool

> Auto-generated documentation for [app.tools.global_tools.google_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/google_tool.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)


- [Google Tool](#google-tool)
  - [google_search](#google_search)
  - [run_async_in_thread](#run_async_in_thread)

## google_search

[Show source in google_tool.py:50](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/google_tool.py#L50)

Searches google and returns entries matching the query.

#### Arguments

- `query` *str* - The search string to look up on Google.

#### Returns

- `dict` - A dictionary containing the search results. Each element of the array contains a dict with fields 'snippet', 'link'

#### Raises

- `Exception` - If there's an error during the Google search process.

#### Signature

```python
@tool
@run_async_in_thread
async def google_search(query: str) -> array: ...
```

#### See also

- [run_async_in_thread](#run_async_in_thread)



## run_async_in_thread

[Show source in google_tool.py:20](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/google_tool.py#L20)

Decorator to run an asynchronous coroutine in a separate thread.

This decorator allows running asynchronous functions in a synchronous context
by executing them in a separate thread with a new event loop.

#### Arguments

- `coro` *Callable* - The asynchronous coroutine to be executed.

#### Returns

- `Callable` - A wrapped function that executes the coroutine in a thread.

#### Signature

```python
def run_async_in_thread(coro): ...
```
