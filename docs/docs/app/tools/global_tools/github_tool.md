# Github Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Github Tool

> Auto-generated documentation for [app.tools.global_tools.github_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/github_tool.py) module.

- [Github Tool](#github-tool)
  - [get_github_info](#get_github_info)
  - [github_action](#github_action)
  - [github_action_helper](#github_action_helper)

## get_github_info

[Show source in github_tool.py:36](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/github_tool.py#L36)

Tool for getting information about the GitHub integration.

#### Returns

- `str` - Information about the GitHub integration.

#### Examples

```python
>>> info = get_github_info()
>>> assert "GitHub" in info
>>> assert "repositories" in info
```

#### Signature

```python
@tool
def get_github_info() -> str: ...
```



## github_action

[Show source in github_tool.py:16](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/github_tool.py#L16)

Tool for performing various GitHub operations.

#### Arguments

- `repo` *str* - Repository name (e.g., 'owner/repo').
- `action` *str* - Action to perform (e.g., 'list_issues', 'create_pr').
- `params` *Dict* - Additional parameters for the action.
- `token` *Optional[str]* - GitHub access token (optional).

#### Returns

- `str` - Result of the GitHub operation.

#### Examples

```python
>>> result = github_action("octocat/Hello-World", "list_issues", {})
>>> assert "issues" in result.lower()
```

#### Signature

```python
@tool
def github_action(
    repo: str, action: str, params: Dict, token: Optional[str] = None
) -> str: ...
```



## github_action_helper

[Show source in github_tool.py:55](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/github_tool.py#L55)

Tool for providing information about different GitHub actions and their required parameters.

#### Arguments

- `action` *str* - The GitHub action (e.g., "create_issue", "list_prs").

#### Returns

- `str` - Information about the specified GitHub action and its required parameters.

#### Examples

```python
>>> result = github_action_helper("create_issue")
>>> assert "title" in result and "body" in result
```

#### Signature

```python
@tool
def github_action_helper(action: str) -> str: ...
```
