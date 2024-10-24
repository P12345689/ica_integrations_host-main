# Watson Discovery Router

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / [Dev](../../../index.md#dev) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Watson Discovery](./index.md#watson-discovery) / Watson Discovery Router

> Auto-generated documentation for [dev.app.routes.watson_discovery.watson_discovery_router](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/watson_discovery/watson_discovery_router.py) module.

#### Attributes

- `DEFAULT_MAX_THREADS` - Environment variables and constants: int(os.getenv('DEFAULT_MAX_THREADS', 4))

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/discovery/templates'))


- [Watson Discovery Router](#watson-discovery-router)
  - [DiscoveryQueryInputModel](#discoveryqueryinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [init_discovery_client](#init_discovery_client)

## DiscoveryQueryInputModel

[Show source in watson_discovery_router.py:70](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/watson_discovery/watson_discovery_router.py#L70)

Model to validate input data for Discovery queries.

#### Signature

```python
class DiscoveryQueryInputModel(BaseModel): ...
```



## OutputModel

[Show source in watson_discovery_router.py:81](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/watson_discovery/watson_discovery_router.py#L81)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in watson_discovery_router.py:76](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/watson_discovery/watson_discovery_router.py#L76)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in watson_discovery_router.py:98](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/watson_discovery/watson_discovery_router.py#L98)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## init_discovery_client

[Show source in watson_discovery_router.py:87](https://github.com/destiny/ica_integrations_host/blob/main/dev/app/routes/watson_discovery/watson_discovery_router.py#L87)

Initialize and return a Watson Discovery V2 client.

#### Signature

```python
def init_discovery_client() -> DiscoveryV2: ...
```
