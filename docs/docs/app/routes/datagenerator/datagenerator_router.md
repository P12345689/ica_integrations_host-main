# Datagenerator Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Datagenerator](./index.md#datagenerator) / Datagenerator Router

> Auto-generated documentation for [app.routes.datagenerator.datagenerator_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/datagenerator/datagenerator_router.py) module.

- [Datagenerator Router](#datagenerator-router)
  - [add_custom_routes](#add_custom_routes)
  - [debug_message](#debug_message)
  - [fit](#fit)

## add_custom_routes

[Show source in datagenerator_router.py:25](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/datagenerator/datagenerator_router.py#L25)

Adds custom API routes to a FastAPI application to generate synthetic data based on the provided CSV and metadata.

#### Arguments

- [App](../../index.md#app) *FastAPI* - The FastAPI application instance to which the route will be added.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## debug_message

[Show source in datagenerator_router.py:149](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/datagenerator/datagenerator_router.py#L149)

Returns a dictionary with a formatted message for displaying error information on the client UI.

#### Arguments

- `message` *str* - The error message to be displayed.

#### Returns

- `Dict[str,` *Any]* - A dictionary containing the error message.

#### Signature

```python
def debug_message(message: str) -> Dict[str, Any]: ...
```



## fit

[Show source in datagenerator_router.py:133](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/datagenerator/datagenerator_router.py#L133)

Placeholder function for situations where no data types are provided.

#### Returns

- `Dict[str,` *Any]* - A dictionary indicating a default process has been executed.

#### Signature

```python
def fit(real_data) -> Dict[str, Any]: ...
```
