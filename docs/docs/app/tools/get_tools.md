# Get Tools

[ica_integrations_host Index](../../README.md#ica_integrations_host-index) / [App](../index.md#app) / [Tools](./index.md#tools) / Get Tools

> Auto-generated documentation for [app.tools.get_tools](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/get_tools.py) module.

#### Attributes

- `color_handler` - Add color formatter to logger: logging.StreamHandler()


- [Get Tools](#get-tools)
  - [ColorFormatter](#colorformatter)
    - [ColorFormatter().format](#colorformatter()format)
  - [create_tools_from_definitions](#create_tools_from_definitions)
  - [get_tool_definitions](#get_tool_definitions)
  - [get_tools](#get_tools)
  - [import_function](#import_function)

## ColorFormatter

[Show source in get_tools.py:31](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/get_tools.py#L31)

#### Signature

```python
class ColorFormatter(logging.Formatter): ...
```

### ColorFormatter().format

[Show source in get_tools.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/get_tools.py#L48)

#### Signature

```python
def format(self, record): ...
```



## create_tools_from_definitions

[Show source in get_tools.py:119](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/get_tools.py#L119)

Create tools from definitions.

#### Arguments

- `tool_definitions` *List[dict]* - A list of dictionaries containing tool definitions.

#### Returns

- `List[Tool]` - A list of created Tool objects.

#### Examples

```python
>>> defs = [{'name': 'test_tool', 'function': 'math.sqrt', 'description': 'Test tool'}]
>>> tools = create_tools_from_definitions(defs)
>>> len(tools)
1
>>> tools[0].name
'test_tool'
```

#### Signature

```python
def create_tools_from_definitions(tool_definitions: List[dict]) -> List[Tool]: ...
```



## get_tool_definitions

[Show source in get_tools.py:157](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/get_tools.py#L157)

Get or load tool definitions from a JSON file.

#### Returns

- `List[Tool]` - A list of Tool objects.

#### Notes

This function caches the tool definitions after the first load.

#### Examples

```python
>>> tools = get_tool_definitions()
>>> isinstance(tools, list)
True
>>> all(isinstance(tool, Tool) for tool in tools)
True
```

#### Signature

```python
def get_tool_definitions() -> List[Tool]: ...
```



## get_tools

[Show source in get_tools.py:191](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/get_tools.py#L191)

Returns a list of tools. If tool_names is provided, returns only the tools with the specified names.
Otherwise, returns all tools.

#### Arguments

- `tool_names` *Optional[List[str]]* - A list of tool names to retrieve.

#### Returns

- `List[Tool]` - A list of Tool objects.

#### Examples

```python
>>> all_tools = get_tools()
>>> len(all_tools) > 0
True
>>> specific_tools = get_tools(['tool1', 'tool2'])
>>> all(tool.name in ['tool1', 'tool2'] for tool in specific_tools)
True
```

#### Signature

```python
def get_tools(tool_names: Optional[List[str]] = None) -> List[Tool]: ...
```



## import_function

[Show source in get_tools.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/get_tools.py#L61)

Dynamically import a function or method from a string path.

#### Arguments

- `function_path` *str* - The dot-separated path to the function or class.
- `method_name` *Optional[str]* - The name of the method if importing from a class.

#### Returns

- `Callable` - The imported function or method.

#### Raises

- `ValueError` - If the function path is invalid or the attribute is not callable.
- `ModuleNotFoundError` - If the specified module cannot be found.
- `AttributeError` - If the specified attribute cannot be found in the module.

#### Examples

```python
>>> import_function('math.sqrt')
<built-in function sqrt>
>>> import_function('collections.Counter', 'update')
<bound method Counter.update of Counter()>
```

#### Signature

```python
def import_function(
    function_path: str, method_name: Optional[str] = None
) -> Callable: ...
```
