# Compare Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Compare](./index.md#compare) / Compare Router

> Auto-generated documentation for [app.routes.compare.compare_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/compare/compare_router.py) module.

#### Attributes

- `LLM_TYPE` - LLM Configuration: os.getenv('LLM_TYPE', 'consulting_assistants')

- `DEFAULT_MAX_THREADS` - Other configuration: int(os.getenv('DEFAULT_MAX_THREADS', 4))

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/compare/templates'))


- [Compare Router](#compare-router)
  - [CompareInputModel](#compareinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [get_llm](#get_llm)

## CompareInputModel

[Show source in compare_router.py:42](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/compare/compare_router.py#L42)

Model to validate input data for document comparison.

#### Signature

```python
class CompareInputModel(BaseModel): ...
```



## OutputModel

[Show source in compare_router.py:56](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/compare/compare_router.py#L56)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in compare_router.py:51](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/compare/compare_router.py#L51)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in compare_router.py:75](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/compare/compare_router.py#L75)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## get_llm

[Show source in compare_router.py:62](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/compare/compare_router.py#L62)

Initialize and return the specified language model.

#### Signature

```python
def get_llm(
    model_name: str, temperature: float, max_tokens: int
) -> BaseLanguageModel: ...
```
