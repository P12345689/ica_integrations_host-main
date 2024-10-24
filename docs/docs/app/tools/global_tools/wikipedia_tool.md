# Wikipedia Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Wikipedia Tool

> Auto-generated documentation for [app.tools.global_tools.wikipedia_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/wikipedia_tool.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)


- [Wikipedia Tool](#wikipedia-tool)
  - [run_async_in_thread](#run_async_in_thread)
  - [search_wikipedia_entries](#search_wikipedia_entries)

## run_async_in_thread

[Show source in wikipedia_tool.py:24](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/wikipedia_tool.py#L24)

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



## search_wikipedia_entries

[Show source in wikipedia_tool.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/wikipedia_tool.py#L54)

Searches Wikipedia and returns entries matching the query.

This function is a langchain tool that performs an asynchronous Wikipedia search.
It creates a WikipediaSearchInput object from the query string and calls the
search_wikipedia function. The asynchronous call is handled by the run_async_in_thread
decorator, allowing it to work within the synchronous context of langchain tools.

#### Arguments

- `query` *str* - The search string to look up on Wikipedia.

#### Returns

- `dict` - A dictionary containing the search results. The structure depends
      on the implementation of the search_wikipedia function, and
      includes keys like 'summary', 'content', 'article_url', and 'image_url'.

#### Raises

- `Exception` - If there's an error during the Wikipedia search process.

#### Signature

```python
@tool
@run_async_in_thread
async def search_wikipedia_entries(query: str) -> dict: ...
```

#### See also

- [run_async_in_thread](#run_async_in_thread)
