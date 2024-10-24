# Plotly Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Plotly](./index.md#plotly) / Plotly Router

> Auto-generated documentation for [app.routes.plotly.plotly_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plotly/plotly_router.py) module.

#### Attributes

- `log` - Set up logging: logging.getLogger(__name__)

- `DEFAULT_MODEL` - Set default model and max threads from environment variables: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/plotly/templates'))


- [Plotly Router](#plotly-router)
  - [ChartInputModel](#chartinputmodel)
  - [ExperienceInputModel](#experienceinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [generate_chart](#generate_chart)

## ChartInputModel

[Show source in plotly_router.py:40](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plotly/plotly_router.py#L40)

Model to validate input data for chart generation.

#### Signature

```python
class ChartInputModel(BaseModel): ...
```



## ExperienceInputModel

[Show source in plotly_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plotly/plotly_router.py#L48)

Model to validate input data for the experience route.

#### Signature

```python
class ExperienceInputModel(BaseModel): ...
```



## OutputModel

[Show source in plotly_router.py:60](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plotly/plotly_router.py#L60)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in plotly_router.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plotly/plotly_router.py#L54)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in plotly_router.py:140](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plotly/plotly_router.py#L140)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## generate_chart

[Show source in plotly_router.py:67](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plotly/plotly_router.py#L67)

Generate a chart using Plotly and save it as an HTML file or PNG image.

#### Arguments

- `chart_type` *str* - The type of chart to generate.
data (Dict[str, List[Any]]): The data for the chart.
- `title` *str, optional* - The title of the chart.
- `format` *str, optional* - The output format, either "PNG" or "HTML". Defaults to "PNG".

#### Returns

- `str` - The URL of the generated file.

#### Raises

- `ValueError` - If the chart type is not supported or the data is invalid.

#### Signature

```python
def generate_chart(
    chart_type: str, data: Dict[str, List[Any]], title: str = "", format: str = "PNG"
) -> str: ...
```
