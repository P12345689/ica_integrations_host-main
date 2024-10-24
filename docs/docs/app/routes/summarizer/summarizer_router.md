# Summarizer Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Summarizer](./index.md#summarizer) / Summarizer Router

> Auto-generated documentation for [app.routes.summarizer.summarizer_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/summarizer/summarizer_router.py) module.

#### Attributes

- `LLM_TYPE` - LLM Configuration: os.getenv('LLM_TYPE', 'consulting_assistants')

- `DEFAULT_MAX_THREADS` - Other configuration: int(os.getenv('DEFAULT_MAX_THREADS', 4))

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/summarizer/templates'))


- [Summarizer Router](#summarizer-router)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [SummarizeInputModel](#summarizeinputmodel)
  - [add_custom_routes](#add_custom_routes)
  - [get_llm](#get_llm)

## OutputModel

[Show source in summarizer_router.py:74](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/summarizer/summarizer_router.py#L74)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in summarizer_router.py:69](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/summarizer/summarizer_router.py#L69)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## SummarizeInputModel

[Show source in summarizer_router.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/summarizer/summarizer_router.py#L54)

Model to validate input data for text summarization.

#### Signature

```python
class SummarizeInputModel(BaseModel): ...
```



## add_custom_routes

[Show source in summarizer_router.py:95](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/summarizer/summarizer_router.py#L95)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## get_llm

[Show source in summarizer_router.py:80](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/summarizer/summarizer_router.py#L80)

Initialize and return the specified language model.

#### Signature

```python
def get_llm(model_name: str, temperature: float) -> BaseLanguageModel: ...
```
