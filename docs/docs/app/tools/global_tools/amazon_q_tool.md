# Amazon Q Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Amazon Q Tool

> Auto-generated documentation for [app.tools.global_tools.amazon_q_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/amazon_q_tool.py) module.

- [Amazon Q Tool](#amazon-q-tool)
  - [query_amazon_q_tool](#query_amazon_q_tool)

## query_amazon_q_tool

[Show source in amazon_q_tool.py:18](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/amazon_q_tool.py#L18)

Tool for querying Amazon Q.

#### Arguments

- `username` *str* - Amazon Q username.
- `password` *str* - Amazon Q password.
- `query` *str* - The query to send to Amazon Q.

#### Returns

- `str` - The response from Amazon Q.

#### Signature

```python
@tool
async def query_amazon_q_tool(username: str, password: str, query: str) -> str: ...
```
