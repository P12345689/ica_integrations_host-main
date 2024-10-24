# Streaming Test Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Streaming Test](./index.md#streaming-test) / Streaming Test Router

> Auto-generated documentation for [dev.app.routes.streaming_test.streaming_test_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/streaming_test/streaming_test_router.py) module.

- [Streaming Test Router](#streaming-test-router)
  - [InputModel](#inputmodel)
  - [OutputModel](#outputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [file_line_streamer](#file_line_streamer)

## InputModel

[Show source in streaming_test_router.py:19](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/streaming_test/streaming_test_router.py#L19)

Model for incoming request data to specify delay and filename.

#### Signature

```python
class InputModel(BaseModel): ...
```



## OutputModel

[Show source in streaming_test_router.py:24](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/streaming_test/streaming_test_router.py#L24)

Output format for streamed data.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## add_custom_routes

[Show source in streaming_test_router.py:70](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/streaming_test/streaming_test_router.py#L70)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## file_line_streamer

[Show source in streaming_test_router.py:33](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/streaming_test/streaming_test_router.py#L33)

Stream a file line by line with a delay.

#### Signature

```python
async def file_line_streamer(
    filename: str, delay: float, invocation_id: str
) -> asyncio.streams.StreamReader: ...
```
