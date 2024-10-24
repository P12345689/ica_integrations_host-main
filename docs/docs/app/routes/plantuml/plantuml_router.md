# Plantuml Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Plantuml](./index.md#plantuml) / Plantuml Router

> Auto-generated documentation for [app.routes.plantuml.plantuml_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_router.py) module.

#### Attributes

- `SERVER_NAME` - Load the PlantUML server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/plantuml/templates'))


- [Plantuml Router](#plantuml-router)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [UMLRequest](#umlrequest)
  - [add_custom_routes](#add_custom_routes)

## OutputModel

[Show source in plantuml_router.py:56](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_router.py#L56)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in plantuml_router.py:49](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_router.py#L49)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## UMLRequest

[Show source in plantuml_router.py:45](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_router.py#L45)

#### Signature

```python
class UMLRequest(BaseModel): ...
```



## add_custom_routes

[Show source in plantuml_router.py:64](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_router.py#L64)

Add custom routes

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```
