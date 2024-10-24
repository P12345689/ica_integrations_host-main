# Graphviz Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Graphviz](./index.md#graphviz) / Graphviz Router

> Auto-generated documentation for [dev.app.routes.graphviz.graphviz_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphviz/graphviz_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/graphviz/templates'))


- [Graphviz Router](#graphviz-router)
  - [ExperienceInputModel](#experienceinputmodel)
  - [GraphvizInputModel](#graphvizinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [generate_png](#generate_png)

## ExperienceInputModel

[Show source in graphviz_router.py:43](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphviz/graphviz_router.py#L43)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## GraphvizInputModel

[Show source in graphviz_router.py:39](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphviz/graphviz_router.py#L39)

Model to validate input data for graphviz generation.

#### Signature

```python
class GraphvizInputModel(BaseModel): ...
```



## OutputModel

[Show source in graphviz_router.py:52](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphviz/graphviz_router.py#L52)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in graphviz_router.py:47](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphviz/graphviz_router.py#L47)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in graphviz_router.py:97](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphviz/graphviz_router.py#L97)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## generate_png

[Show source in graphviz_router.py:58](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/graphviz/graphviz_router.py#L58)

Generate a PNG file from graphviz syntax using the dot command.

#### Arguments

- `syntax` *str* - The graphviz syntax.

#### Returns

- `str` - The URL of the generated PNG file.

#### Raises

- `RuntimeError` - If the PNG generation fails.

#### Signature

```python
def generate_png(syntax: str) -> str: ...
```
