# Gpt4vision Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Gpt4vision](./index.md#gpt4vision) / Gpt4vision Router

> Auto-generated documentation for [app.routes.gpt4vision.gpt4vision_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/gpt4vision/gpt4vision_router.py) module.

- [Gpt4vision Router](#gpt4vision-router)
  - [GPT4VisionRequest](#gpt4visionrequest)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)

## GPT4VisionRequest

[Show source in gpt4vision_router.py:43](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/gpt4vision/gpt4vision_router.py#L43)

Represents the request for the GPT-4 Vision API.

#### Attributes

- `query` *str* - The query to be sent to the GPT-4 Vision API.
- `image_url` *str* - The URL of the image to be processed by the GPT-4 Vision API.

#### Signature

```python
class GPT4VisionRequest(BaseModel): ...
```



## OutputModel

[Show source in gpt4vision_router.py:63](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/gpt4vision/gpt4vision_router.py#L63)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in gpt4vision_router.py:56](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/gpt4vision/gpt4vision_router.py#L56)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in gpt4vision_router.py:71](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/gpt4vision/gpt4vision_router.py#L71)

Adds custom routes to the FastAPI application.

#### Arguments

- [app](#gpt4vision-router) *FastAPI* - The FastAPI application instance.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```
