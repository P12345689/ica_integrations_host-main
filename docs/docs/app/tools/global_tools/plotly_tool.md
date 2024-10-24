# Plotly Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Plotly Tool

> Auto-generated documentation for [app.tools.global_tools.plotly_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/plotly_tool.py) module.

- [Plotly Tool](#plotly-tool)
  - [create_plotly_chart](#create_plotly_chart)
  - [get_plotly_info](#get_plotly_info)
  - [plotly_chart_type_helper](#plotly_chart_type_helper)

## create_plotly_chart

[Show source in plotly_tool.py:16](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/plotly_tool.py#L16)

Tool for generating a Plotly chart from the provided data.

#### Arguments

- `chart_type` *str* - The type of chart to generate (e.g., 'bar', 'pie', 'line').
data (Dict[str, List[Any]]): The data for the chart.
- `title` *str, optional* - The title of the chart.

#### Returns

- `str` - The URL of the generated HTML file.

#### Examples

```python
>>> result = create_plotly_chart("bar", {"x": ["A", "B", "C"], "y": [1, 2, 3]}, "Sample Chart")
>>> assert "http" in result and ".html" in result
```

#### Signature

```python
@tool
def create_plotly_chart(
    chart_type: str, data: Dict[str, List[Any]], title: str = ""
) -> str: ...
```



## get_plotly_info

[Show source in plotly_tool.py:35](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/plotly_tool.py#L35)

Tool for getting information about the Plotly integration.

#### Returns

- `str` - Information about the Plotly integration.

#### Examples

```python
>>> info = get_plotly_info()
>>> assert "Plotly" in info
>>> assert "generate interactive charts" in info
```

#### Signature

```python
@tool
def get_plotly_info() -> str: ...
```



## plotly_chart_type_helper

[Show source in plotly_tool.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/plotly_tool.py#L54)

Tool for providing information about different Plotly chart types and their data requirements.

#### Arguments

- `chart_type` *str* - The type of chart (e.g., "bar", "pie", "line").

#### Returns

- `str` - Information about the specified chart type and its data requirements.

#### Examples

```python
>>> result = plotly_chart_type_helper("bar")
>>> assert "bar chart" in result.lower()
>>> assert "x" in result and "y" in result
```

#### Signature

```python
@tool
def plotly_chart_type_helper(chart_type: str) -> str: ...
```
