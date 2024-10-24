# Test Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Test](./index.md#test) / Test Router

> Auto-generated documentation for [app.routes.test.test_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/test/test_router.py) module.

#### Attributes

- `DEFAULT_MAX_THREADS` - Constants: int(os.getenv('DEFAULT_MAX_THREADS', 4))


- [Test Router](#test-router)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [format_curl_command](#format_curl_command)
  - [format_headers](#format_headers)

## OutputModel

[Show source in test_router.py:36](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/test/test_router.py#L36)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in test_router.py:31](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/test/test_router.py#L31)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in test_router.py:83](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/test/test_router.py#L83)

Add custom routes to the FastAPI application.

#### Arguments

- [App](../../index.md#app) *FastAPI* - The FastAPI application instance.

#### Returns

None

```python
>>> from fastapi import FastAPI
>>> app = FastAPI()
>>> add_custom_routes(app)
>>> app.routes[-1].path
'/system/test/debug/invoke'
```

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## format_curl_command

[Show source in test_router.py:57](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/test/test_router.py#L57)

Format a curl command based on the request.

#### Arguments

- `request` *Request* - The FastAPI request object.
data (Dict[str, Any]): The request data.

#### Returns

- `str` - A formatted curl command.

```python
>>> from fastapi.testclient import TestClient
>>> app = FastAPI()
>>> @app.post("/test")
... async def test(request: Request):
...     data = await request.json()
...     return format_curl_command(request, data)
>>> client = TestClient(app)
>>> response = client.post("/test", json={"key": "value"})
>>> "curl -X POST http://testserver/test -H 'Content-Type: application/json' -d '{"key": "value"}'" in response.text
True
```

#### Signature

```python
def format_curl_command(request: Request, data: Dict[str, Any]) -> str: ...
```



## format_headers

[Show source in test_router.py:42](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/test/test_router.py#L42)

Format request headers into a string.

#### Arguments

headers (Dict[str, str]): The request headers.

#### Returns

- `str` - A formatted string of headers.

```python
>>> format_headers({"Content-Type": "application/json", "User-Agent": "curl/7.64.1"})
'Content-Type: application/json\nUser-Agent: curl/7.64.1'
```

#### Signature

```python
def format_headers(headers: Dict[str, str]) -> str: ...
```
