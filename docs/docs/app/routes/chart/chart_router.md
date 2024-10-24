# Chart Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Chart](./index.md#chart) / Chart Router

> Auto-generated documentation for [app.routes.chart.chart_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/chart/chart_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/chart/templates'))


- [Chart Router](#chart-router)
  - [CSVInputModel](#csvinputmodel)
  - [ChartInputModel](#chartinputmodel)
  - [ExperienceInputModel](#experienceinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [generate_chart](#generate_chart)

## CSVInputModel

[Show source in chart_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/chart/chart_router.py#L48)

Model to validate input data for chart generation from CSV.

#### Signature

```python
class CSVInputModel(BaseModel): ...
```



## ChartInputModel

[Show source in chart_router.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/chart/chart_router.py#L61)

Model to validate input data for chart generation.

#### Signature

```python
class ChartInputModel(BaseModel): ...
```



## ExperienceInputModel

[Show source in chart_router.py:71](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/chart/chart_router.py#L71)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## OutputModel

[Show source in chart_router.py:84](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/chart/chart_router.py#L84)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in chart_router.py:77](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/chart/chart_router.py#L77)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in chart_router.py:136](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/chart/chart_router.py#L136)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## generate_chart

[Show source in chart_router.py:92](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/chart/chart_router.py#L92)

Generate a chart using matplotlib and save it as a PNG file.

#### Arguments

- `chart_type` *str* - The type of chart to generate.
data (Dict[str, List[Any]]): The data for the chart.
- `title` *str, optional* - The title of the chart.

#### Returns

- `str` - The URL of the generated PNG file.

#### Raises

- `ValueError` - If the chart type is not supported or the data is invalid.

#### Signature

```python
def generate_chart(
    chart_type: str, data: Dict[str, List[Any]], title: str = ""
) -> str: ...
```
