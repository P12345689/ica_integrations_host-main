# Chart Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Chart Tool

> Auto-generated documentation for [app.tools.global_tools.chart_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/chart_tool.py) module.

- [Chart Tool](#chart-tool)
  - [chart_type_helper](#chart_type_helper)
  - [create_chart](#create_chart)
  - [get_chart_info](#get_chart_info)

## chart_type_helper

[Show source in chart_tool.py:63](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/chart_tool.py#L63)

Tool for providing information about different chart types and their data requirements from JSON input.

#### Arguments

- `input_json` *str* - JSON string containing the chart type.

#### Returns

- `str` - Information about the specified chart type and its data requirements.

#### Examples

```python
>>> result = chart_type_helper('{"chart_type": "bar"}')
>>> assert "bar chart" in result.lower()
>>> assert "x" in result and "y" in result
```

#### Signature

```python
@tool
def chart_type_helper(input_json: str) -> str: ...
```



## create_chart

[Show source in chart_tool.py:17](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/chart_tool.py#L17)

Tool for generating a chart from the provided JSON data.

#### Arguments

- `input_json` *str* - JSON string containing the chart type, data, and optionally a title.

#### Returns

- `str` - The URL of the generated PNG file.

#### Examples

```python
>>> result = create_chart('{"chart_type": "bar", "data": {"x": ["A", "B", "C"], "y": [1, 2, 3]}, "title": "Sample Chart"}')
>>> assert "http" in result and ".png" in result
```

#### Signature

```python
@tool
def create_chart(input_json: str) -> str: ...
```



## get_chart_info

[Show source in chart_tool.py:43](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/chart_tool.py#L43)

Tool for getting information about the Chart integration.

#### Returns

- `str` - Information about the Chart integration.

#### Examples

```python
>>> info = get_chart_info()
>>> assert "Chart" in info
>>> assert "generate charts" in info
```

#### Signature

```python
@tool
def get_chart_info() -> str: ...
```
