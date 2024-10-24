# Compare Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Compare Tool

> Auto-generated documentation for [app.tools.global_tools.compare_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/compare_tool.py) module.

- [Compare Tool](#compare-tool)
  - [get_compare_info](#get_compare_info)
  - [get_compare_tool](#get_compare_tool)

## get_compare_info

[Show source in compare_tool.py:36](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/compare_tool.py#L36)

Tool for getting information about the compare integration.

#### Returns

- `str` - Information about the compare integration.

#### Examples

```python
>>> info = get_compare_info()
>>> assert "compare" in info
>>> assert "generate timestamps" in info
```

#### Signature

```python
@tool
def get_compare_info() -> str: ...
```



## get_compare_tool

[Show source in compare_tool.py:16](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/compare_tool.py#L16)

Tool for getting the current compare in the specified format.

#### Arguments

- `format` *str, optional* - The format string for the compare. Defaults to "%Y-%m-%d %H:%M:%S".

#### Returns

- `str` - The formatted compare.

#### Examples

```python
>>> result = get_compare_tool()
>>> import re
>>> assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result)
>>> custom_result = get_compare_tool("%Y-%m-%d")
>>> assert re.match(r'\d{4}-\d{2}-\d{2}', custom_result)
```

#### Signature

```python
@tool
def get_compare_tool(format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str: ...
```
