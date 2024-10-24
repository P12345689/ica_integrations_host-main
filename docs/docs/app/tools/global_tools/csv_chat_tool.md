# Csv Chat Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Csv Chat Tool

> Auto-generated documentation for [app.tools.global_tools.csv_chat_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/csv_chat_tool.py) module.

- [Csv Chat Tool](#csv-chat-tool)
  - [csv_chat_tool](#csv_chat_tool)

## csv_chat_tool

[Show source in csv_chat_tool.py:17](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/csv_chat_tool.py#L17)

Tool for querying CSV data using natural language.

#### Arguments

- `query` *str* - The natural language query about the CSV data.
- `csv_content` *Optional[str]* - The CSV content as a string.
- `file_url` *Optional[str]* - URL to a CSV or XLSX file.
- `file` *Optional[UploadFile]* - Uploaded CSV or XLSX file.

#### Returns

- `str` - The response to the query based on the CSV data.

#### Signature

```python
@tool
async def csv_chat_tool(
    query: str,
    csv_content: Optional[str] = None,
    file_url: Optional[str] = None,
    file: Optional[UploadFile] = None,
) -> str: ...
```
