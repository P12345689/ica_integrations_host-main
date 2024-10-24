# Xlsx Builder Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Xlsx Builder](./index.md#xlsx-builder) / Xlsx Builder Router

> Auto-generated documentation for [app.routes.xlsx_builder.xlsx_builder_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/xlsx_builder/xlsx_builder_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/xlsx_builder/templates'))


- [Xlsx Builder Router](#xlsx-builder-router)
  - [CSVInputModel](#csvinputmodel)
  - [ExperienceInputModel](#experienceinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [generate_xlsx](#generate_xlsx)
  - [write_csv_to_xlsx](#write_csv_to_xlsx)

## CSVInputModel

[Show source in xlsx_builder_router.py:43](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/xlsx_builder/xlsx_builder_router.py#L43)

Model to validate input data for XLSX generation from CSV.

#### Signature

```python
class CSVInputModel(BaseModel): ...
```



## ExperienceInputModel

[Show source in xlsx_builder_router.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/xlsx_builder/xlsx_builder_router.py#L52)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## OutputModel

[Show source in xlsx_builder_router.py:67](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/xlsx_builder/xlsx_builder_router.py#L67)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in xlsx_builder_router.py:60](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/xlsx_builder/xlsx_builder_router.py#L60)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in xlsx_builder_router.py:120](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/xlsx_builder/xlsx_builder_router.py#L120)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## generate_xlsx

[Show source in xlsx_builder_router.py:89](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/xlsx_builder/xlsx_builder_router.py#L89)

Generate an XLSX file from CSV data.

#### Arguments

- `csv_data` *str* - The CSV data as a string.
- `sheet_name` *str, optional* - The name of the sheet in the XLSX file. Defaults to "Sheet1".

#### Returns

- `str` - The URL of the generated XLSX file.

#### Raises

- `ValueError` - If the CSV data is invalid.

#### Signature

```python
def generate_xlsx(csv_data: str, sheet_name: str = "Sheet1") -> str: ...
```



## write_csv_to_xlsx

[Show source in xlsx_builder_router.py:75](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/xlsx_builder/xlsx_builder_router.py#L75)

Write a CSV to Excel.

#### Arguments

- `df` *DataFrame* - the dataframe to write to excel
- `file_path` *str* - The target folder.
- `sheet_name` *str, optional* - The name of the sheet in the XLSX file. Defaults to "Sheet1".

#### Signature

```python
def write_csv_to_xlsx(df, file_path, sheet_name): ...
```
