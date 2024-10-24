# Agent Copilot Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Agent Copilot Tool

> Auto-generated documentation for [app.tools.global_tools.agent_copilot_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/agent_copilot_tool.py) module.

- [Agent Copilot Tool](#agent-copilot-tool)
  - [agent_copilot_tool](#agent_copilot_tool)

## agent_copilot_tool

[Show source in agent_copilot_tool.py:14](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/agent_copilot_tool.py#L14)

Tool for interacting with the Agent Copilot integration.

#### Arguments

- `assistant` *str* - The name of the assistant to invoke (e.g., "appmod" or "migration")
- `message` *str* - The message to send to the assistant
- `api_key` *str, optional* - The API key for the integration. If not provided, it should be set in the environment.

#### Returns

- `str` - The response from the assistant

#### Raises

- `Exception` - If there's an error in the API call

#### Signature

```python
@tool
def agent_copilot_tool(
    assistant: str, message: str, api_key: Optional[str] = None
) -> str: ...
```
