# Mvs Zos Logo Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / `attic` / `routes` / [Mvs Zos Logo](./index.md#mvs-zos-logo) / Mvs Zos Logo Router

> Auto-generated documentation for [attic.routes.mvs_zos_logo.mvs_zos_logo_router](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/mvs_zos_logo/mvs_zos_logo_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/mvs_zos_logo/templates'))


- [Mvs Zos Logo Router](#mvs-zos-logo-router)
  - [LogoInputModel](#logoinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [generate_logo_assembly](#generate_logo_assembly)

## LogoInputModel

[Show source in mvs_zos_logo_router.py:35](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/mvs_zos_logo/mvs_zos_logo_router.py#L35)

Model to validate input data for logo generation.

#### Signature

```python
class LogoInputModel(BaseModel): ...
```



## OutputModel

[Show source in mvs_zos_logo_router.py:46](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/mvs_zos_logo/mvs_zos_logo_router.py#L46)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in mvs_zos_logo_router.py:41](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/mvs_zos_logo/mvs_zos_logo_router.py#L41)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in mvs_zos_logo_router.py:81](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/mvs_zos_logo/mvs_zos_logo_router.py#L81)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## generate_logo_assembly

[Show source in mvs_zos_logo_router.py:52](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/mvs_zos_logo/mvs_zos_logo_router.py#L52)

Generate assembly language code for displaying a logo on MVS/z/OS.

#### Arguments

- `logo_text` *str* - The text-based logo to convert.
- `start_line` *int* - The starting line number for the logo.
- `start_column` *int* - The starting column number for the logo.

#### Returns

- `str` - The generated assembly language code.

#### Examples

```python
>>> logo = "ABC\nDEF"
>>> result = generate_logo_assembly(logo, 7, 15)
>>> assert "$SBA   (7,15)" in result
>>> assert "DC     C'ABC'" in result
>>> assert "$SBA   (8,15)" in result
>>> assert "DC     C'DEF'" in result
```

#### Signature

```python
def generate_logo_assembly(
    logo_text: str, start_line: int, start_column: int
) -> str: ...
```
