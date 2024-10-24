# Ask Prompts Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Ask Prompts Tool

> Auto-generated documentation for [app.tools.global_tools.ask_prompts_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ask_prompts_tool.py) module.

- [Ask Prompts Tool](#ask-prompts-tool)
  - [get_prompts_tool](#get_prompts_tool)

## get_prompts_tool

[Show source in ask_prompts_tool.py:17](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ask_prompts_tool.py#L17)

Tool for retrieving and filtering prompts based on various criteria.

#### Arguments

- `input_str` *str* - A JSON string containing the search criteria.
    Possible keys:
    - tags (Optional[Union[str, List[str]]]): Tag or list of tags to filter prompts.
    - roles (Optional[Union[str, List[str]]]): Role or list of roles to filter prompts.
    - search_term (Optional[str]): Search term for prompt title or description.
    - visibility (Optional[str]): Visibility filter (e.g., 'TEAM', 'PUBLIC').
    - user_email (Optional[str]): Filter by user email.
    - prompt_id (Optional[str]): Specific prompt ID to retrieve.

#### Returns

- `str` - A formatted string containing information about the matching prompts.

#### Examples

```python
>>> get_prompts_tool('{"tags": ["python"], "roles": "developer"}')
'Matching prompts: ...'
```

#### Signature

```python
@tool
def get_prompts_tool(input_str: str) -> str: ...
```
