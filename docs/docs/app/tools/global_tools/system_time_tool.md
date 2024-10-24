# System Time Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / System Time Tool

> Auto-generated documentation for [app.tools.global_tools.system_time_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/system_time_tool.py) module.

- [System Time Tool](#system-time-tool)
  - [get_system_time_tool](#get_system_time_tool)

## get_system_time_tool

[Show source in system_time_tool.py:16](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/system_time_tool.py#L16)

Tool for getting the current system time in the specified format.

#### Arguments

- `format` *str, optional* - The format string for the time. Defaults to "%Y-%m-%dT%H:%M:%S%Z".

#### Returns

- `str` - The formatted current time.

#### Signature

```python
@tool
def get_system_time_tool(format: Optional[str] = "%Y-%m-%dT%H:%M:%S%Z") -> str: ...
```
