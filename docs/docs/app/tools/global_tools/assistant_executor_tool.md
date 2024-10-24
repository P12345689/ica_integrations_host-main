# Assistant Executor Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Assistant Executor Tool

> Auto-generated documentation for [app.tools.global_tools.assistant_executor_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/assistant_executor_tool.py) module.

- [Assistant Executor Tool](#assistant-executor-tool)
  - [assistant_executor_tool](#assistant_executor_tool)

## assistant_executor_tool

[Show source in assistant_executor_tool.py:17](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/assistant_executor_tool.py#L17)

Tool for executing an assistant based on the provided assistant ID and prompt.

#### Arguments

- `input_str` *str* - A JSON string containing the execution parameters.
    Required keys:
    - assistant_id (str): The ID of the assistant to be executed.
    - prompt (str): The prompt to be passed to the assistant.

#### Returns

- `str` - The response from the executed assistant.

#### Examples

```python
>>> assistant_executor_tool('{"assistant_id": "3903", "prompt": "App to open the car trunk using facial recognition"}')
'Response from assistant: ...'
```

#### Signature

```python
@tool
def assistant_executor_tool(input_str: str) -> str: ...
```
