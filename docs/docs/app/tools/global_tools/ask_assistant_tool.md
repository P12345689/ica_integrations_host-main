# Ask Assistant Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Ask Assistant Tool

> Auto-generated documentation for [app.tools.global_tools.ask_assistant_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ask_assistant_tool.py) module.

- [Ask Assistant Tool](#ask-assistant-tool)
  - [get_assistants_tool](#get_assistants_tool)

## get_assistants_tool

[Show source in ask_assistant_tool.py:17](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ask_assistant_tool.py#L17)

Tool for getting assistant information based on specified criteria.

#### Arguments

- `input_str` *str* - A JSON string containing the search criteria.
    Possible keys:
    - tags (Optional[Union[str, List[str]]]): Tag or list of tags to filter assistants.
    - roles (Optional[Union[str, List[str]]]): Role or list of roles to filter assistants.
    - search_term (Optional[str]): Search term for assistant title or description.
    - assistant_id (Optional[str]): Specific assistant ID to retrieve.
    - refresh (Optional[bool]): Whether to refresh the assistants data.

#### Returns

- `str` - A formatted string containing information about the matching assistants.

#### Examples

```python
>>> get_assistants_tool('{"tags": ["unified"]}')
'Matching assistants: ...'
```

#### Signature

```python
@tool
def get_assistants_tool(input_str: str) -> str: ...
```
