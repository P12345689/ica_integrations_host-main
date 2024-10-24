# Ask Docs Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Ask Docs Tool

> Auto-generated documentation for [app.tools.global_tools.ask_docs_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ask_docs_tool.py) module.

- [Ask Docs Tool](#ask-docs-tool)
  - [get_collections_tool](#get_collections_tool)
  - [query_documents_tool](#query_documents_tool)

## get_collections_tool

[Show source in ask_docs_tool.py:18](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ask_docs_tool.py#L18)

Tool for getting the list of available document collections.

#### Arguments

refresh (Union[bool, str]): Whether to refresh the collections data.
                            Can be a boolean or a string 'true'/'false'. Defaults to False.

#### Returns

- `str` - A formatted string containing information about the available collections.

#### Examples

```python
>>> get_collections_tool(refresh=True)
'Available document collections: ...'
>>> get_collections_tool(refresh='true')
'Available document collections: ...'
```

#### Signature

```python
@tool
def get_collections_tool(refresh: Union[bool, str] = False) -> str: ...
```



## query_documents_tool

[Show source in ask_docs_tool.py:56](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ask_docs_tool.py#L56)

Tool for querying documents in specified collections.

#### Arguments

- `input_str` *str* - A JSON string containing the query parameters.
    Required keys:
    - collection_ids (List[str]): List of collection IDs to query.
    - query (str): The query to ask about the documents.
    Optional key:
    - document_names (Optional[List[str]]): List of document names to query within the collections.

#### Returns

- `str` - The response from querying the documents.

#### Examples

```python
>>> query_documents_tool('{"collection_ids": ["id1", "id2"], "query": "What is AI?", "document_names": ["doc1.pdf"]}')
'Response from querying documents: ...'
```

#### Signature

```python
@tool
def query_documents_tool(input_str: str) -> str: ...
```
