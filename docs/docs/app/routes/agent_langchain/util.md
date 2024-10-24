# Util

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Agents](./index.md#agents) / Util

> Auto-generated documentation for [app.routes.agent_langchain.util](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/util.py) module.

- [Util](#util)
  - [ContextItem](#contextitem)
  - [format_context](#format_context)
  - [parse_context](#parse_context)
  - [unescape_string](#unescape_string)

## ContextItem

[Show source in util.py:22](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/util.py#L22)

Model for a single context item.

#### Signature

```python
class ContextItem(BaseModel): ...
```



## format_context

[Show source in util.py:97](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/util.py#L97)

Formats the context items into a string for the prompt.

#### Arguments

- `context_items` *List[ContextItem]* - A list of ContextItem objects.

#### Returns

- `str` - A formatted string representing the context items.

#### Signature

```python
def format_context(context_items: List[ContextItem]) -> str: ...
```

#### See also

- [ContextItem](#contextitem)



## parse_context

[Show source in util.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/util.py#L52)

Parses the stringified JSON context into a list of ContextItem objects.

#### Arguments

- `context_str` *Optional[str]* - The JSON string of context items.

#### Returns

- `List[ContextItem]` - A list of ContextItem objects.

#### Raises

- `ValueError` - If the context JSON is invalid or if context items are in an invalid format.

#### Signature

```python
def parse_context(context_str: Optional[str]) -> List[ContextItem]: ...
```

#### See also

- [ContextItem](#contextitem)



## unescape_string

[Show source in util.py:27](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/util.py#L27)

Unescape a string that may contain various levels of escaping,
while preserving regular characters.

#### Arguments

- `s` *str* - The escaped string.

#### Returns

- `str` - The unescaped string.

#### Signature

```python
def unescape_string(s: str) -> str: ...
```
