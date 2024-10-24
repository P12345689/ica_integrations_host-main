# Webex Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Webex Tool

> Auto-generated documentation for [app.tools.global_tools.webex_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/webex_tool.py) module.

- [Webex Tool](#webex-tool)
  - [get_webex_info](#get_webex_info)
  - [summarize_transcript](#summarize_transcript)
  - [webex_action](#webex_action)
  - [webex_action_helper](#webex_action_helper)

## get_webex_info

[Show source in webex_tool.py:35](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/webex_tool.py#L35)

Tool for getting information about the WebEx integration.

#### Returns

- `str` - Information about the WebEx integration.

#### Examples

```python
>>> info = get_webex_info()
>>> assert "WebEx" in info
>>> assert "transcripts" in info
```

#### Signature

```python
@tool
def get_webex_info() -> str: ...
```



## summarize_transcript

[Show source in webex_tool.py:75](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/webex_tool.py#L75)

Tool for summarizing a WebEx transcript using an LLM.

#### Arguments

- `transcript` *str* - The full transcript content.

#### Returns

- `str` - A summary of the transcript.

#### Examples

```python
>>> summary = summarize_transcript("This is a sample transcript of a meeting about project deadlines.")
>>> assert "summary" in summary.lower()
```

#### Signature

```python
@tool
def summarize_transcript(transcript: str) -> str: ...
```



## webex_action

[Show source in webex_tool.py:16](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/webex_tool.py#L16)

Tool for performing various WebEx operations.

#### Arguments

- `action` *str* - Action to perform (e.g., 'list_transcripts', 'get_transcript').
- `params` *Dict* - Additional parameters for the action.
- `webex_token` *str* - WebEx access token.

#### Returns

- `str` - Result of the WebEx operation.

#### Examples

```python
>>> result = webex_action("list_transcripts", {}, "your_webex_token_here")
>>> assert "transcripts" in result.lower()
```

#### Signature

```python
@tool
def webex_action(action: str, params: Dict, webex_token: str) -> str: ...
```



## webex_action_helper

[Show source in webex_tool.py:54](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/webex_tool.py#L54)

Tool for providing information about different WebEx actions and their required parameters.

#### Arguments

- `action` *str* - The WebEx action (e.g., "list_transcripts", "get_transcript").

#### Returns

- `str` - Information about the specified WebEx action and its required parameters.

#### Examples

```python
>>> result = webex_action_helper("get_transcript")
>>> assert "transcript_id" in result
```

#### Signature

```python
@tool
def webex_action_helper(action: str) -> str: ...
```
