# Monday Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Monday Tool

> Auto-generated documentation for [app.tools.global_tools.monday_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/monday_tool.py) module.

- [Monday Tool](#monday-tool)
  - [monday_api_tool](#monday_api_tool)

## monday_api_tool

[Show source in monday_tool.py:15](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/monday_tool.py#L15)

Tool for making Monday.com API calls.

#### Arguments

- `query` *str* - The GraphQL query or mutation.
variables (Optional[Dict[str, Any]]): Variables for the GraphQL query.

#### Returns

- `str` - The JSON response from the Monday.com API as a string.

#### Examples

```python
>>> result = monday_api_tool("query { boards { id name } }")
>>> isinstance(result, str)
True
```

#### Signature

```python
@tool
async def monday_api_tool(
    query: str, variables: Optional[Dict[str, Any]] = None
) -> str: ...
```
