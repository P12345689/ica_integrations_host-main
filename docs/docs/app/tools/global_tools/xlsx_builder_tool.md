# Xlsx Builder Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Xlsx Builder Tool

> Auto-generated documentation for [app.tools.global_tools.xlsx_builder_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/xlsx_builder_tool.py) module.

- [Xlsx Builder Tool](#xlsx-builder-tool)
  - [create_xlsx_from_csv](#create_xlsx_from_csv)
  - [get_xlsx_builder_info](#get_xlsx_builder_info)
  - [xlsx_format_helper](#xlsx_format_helper)

## create_xlsx_from_csv

[Show source in xlsx_builder_tool.py:15](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/xlsx_builder_tool.py#L15)

Tool for generating an XLSX file from CSV data.

Args:
    csv_data (str): The CSV data as a string.
    sheet_name (str, optional): The name of the sheet in the XLSX file. Defaults to "Sheet1".

Returns:
    str: The URL of the generated XLSX file.

Example:

```python
>>> result = create_xlsx_from_csv("Name,Age
```

John,30
Jane,25", "Employee Data")

```python
>>> assert "http" in result and ".xlsx" in result
```

#### Signature

```python
@tool
def create_xlsx_from_csv(csv_data: str, sheet_name: str = "Sheet1") -> str: ...
```



## get_xlsx_builder_info

[Show source in xlsx_builder_tool.py:33](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/xlsx_builder_tool.py#L33)

Tool for getting information about the XLSX builder integration.

#### Returns

- `str` - Information about the XLSX builder integration.

#### Examples

```python
>>> info = get_xlsx_builder_info()
>>> assert "XLSX" in info
>>> assert "generate spreadsheets" in info
```

#### Signature

```python
@tool
def get_xlsx_builder_info() -> str: ...
```



## xlsx_format_helper

[Show source in xlsx_builder_tool.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/xlsx_builder_tool.py#L52)

Tool for providing information about XLSX file format and capabilities.

#### Returns

- `str` - Information about XLSX file format and capabilities.

#### Examples

```python
>>> result = xlsx_format_helper()
>>> assert "XLSX" in result
>>> assert "Microsoft Excel" in result
```

#### Signature

```python
@tool
def xlsx_format_helper() -> str: ...
```
