# Request Utilities

[ica_integrations_host Index](../../README.md#ica_integrations_host-index) / [App](../index.md#app) / [Utilities](./index.md#utilities) / Request Utilities

> Auto-generated documentation for [app.utilities.request_utilities](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/request_utilities.py) module.

#### Attributes

- `log` - set the logger: logging.getLogger(__name__)


- [Request Utilities](#request-utilities)
  - [api_wrapper](#api_wrapper)
  - [debug_message](#debug_message)
  - [get_request_data](#get_request_data)

## api_wrapper

[Show source in request_utilities.py:24](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/request_utilities.py#L24)

#### Signature

```python
async def api_wrapper(
    func: Callable[..., Coroutine], request: Request, *args, **kwargs
): ...
```



## debug_message

[Show source in request_utilities.py:51](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/request_utilities.py#L51)

Returns a dictionary with a formatted message for displaying error information on the client UI.

#### Arguments

- `message` *str* - The error message to be displayed.

#### Returns

- `Dict[str,` *Any]* - A dictionary containing the error message.

#### Signature

```python
def debug_message(message: str) -> Dict[str, Any]: ...
```



## get_request_data

[Show source in request_utilities.py:13](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/utilities/request_utilities.py#L13)

#### Signature

```python
async def get_request_data(request: Request): ...
```
