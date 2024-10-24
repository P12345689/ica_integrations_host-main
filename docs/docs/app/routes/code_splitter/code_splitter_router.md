# Code Splitter Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Code Splitter](./index.md#code-splitter) / Code Splitter Router

> Auto-generated documentation for [app.routes.code_splitter.code_splitter_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py) module.

#### Attributes

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/code_splitter/templates'))


- [Code Splitter Router](#code-splitter-router)
  - [InputModel](#inputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [generate_zip_file](#generate_zip_file)
  - [get_file_extension](#get_file_extension)
  - [process_count_tokens](#process_count_tokens)
  - [process_split](#process_split)
  - [process_unit_test_or_business_rules](#process_unit_test_or_business_rules)

## InputModel

[Show source in code_splitter_router.py:73](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L73)

Model to validate input data.

#### Signature

```python
class InputModel(BaseModel): ...
```



## OutputModel

[Show source in code_splitter_router.py:88](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L88)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in code_splitter_router.py:82](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L82)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in code_splitter_router.py:275](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L275)

Add custom routes to the FastAPI app.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## generate_zip_file

[Show source in code_splitter_router.py:125](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L125)

Generate a ZIP file containing the file contents and headers.

#### Arguments

- `file_contents` *List[str]* - The contents of the files to be included in the ZIP.
- `headers` *List[str]* - The headers to be included in the ZIP.
- `file_extension` *str* - The file extension for the generated files.
- `request_type` *str* - The type of request (default: "split").
- `source_file_name` *str* - The name of the source file (optional).

#### Returns

- `str` - The URL of the generated ZIP file.

#### Examples

```python
>>> file_contents = ["def hello():
```

print('Hello')", "def world():
print('World')"]

```python
>>> headers = ["def hello():", "def world():"]
>>> generate_zip_file(file_contents, headers, ".py", request_type="unit_test", source_file_name="example")
'http://127.0.0.1:8080/public/code_splitter/unit_test_....zip'
```

#### Signature

```python
def generate_zip_file(
    file_contents, headers, file_extension, request_type="split", source_file_name=None
): ...
```



## get_file_extension

[Show source in code_splitter_router.py:95](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L95)

Get the file extension based on the programming language.

#### Arguments

- `language` *str* - The programming language.

#### Returns

- `str` - The corresponding file extension.

#### Examples

```python
>>> get_file_extension("python")
'.py'
>>> get_file_extension("java")
'.java'
>>> get_file_extension("unknown")
'.txt'
```

#### Signature

```python
def get_file_extension(language): ...
```



## process_count_tokens

[Show source in code_splitter_router.py:245](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L245)

Process the token counting request.

Args:
    code (str): The original code.
    chunks (List[str]): The code chunks.

Returns:
    ResponseMessageModel: The response message containing the token counts.

Examples:

```python
>>> code = "def hello():
```

print('Hello')

def world():
    print('World')"

```python
>>> chunks = ["def hello():
```

print('Hello')", "def world():
print('World')"]

```python
>>> process_count_tokens(code, chunks)
ResponseMessageModel(message="Total tokens in the code: 12
```

Tokens per chunk:
Chunk 1: 6 tokens
Chunk 2: 6 tokens
", type="text")

#### Signature

```python
def process_count_tokens(code, chunks): ...
```



## process_split

[Show source in code_splitter_router.py:220](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L220)

Process the code splitting request.

#### Arguments

- `chunks` *List[str]* - The code chunks.
- `headers` *List[str]* - The headers extracted from the code.
- `file_extension` *str* - The file extension for the generated files.

#### Returns

- [ResponseMessageModel](#responsemessagemodel) - The response message containing the URL of the generated ZIP file.

#### Examples

```python
>>> chunks = ["def hello():
```

print('Hello')", "def world():
print('World')"]

```python
>>> headers = ["def hello():", "def world():"]
>>> process_split(chunks, headers, ".py")
ResponseMessageModel(message="The split code files can be downloaded from this URL: http://127.0.0.1:8080/public/code_splitter/split_....zip", type="text")
```

#### Signature

```python
def process_split(chunks, headers, file_extension): ...
```



## process_unit_test_or_business_rules

[Show source in code_splitter_router.py:165](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/code_splitter/code_splitter_router.py#L165)

Process unit test or business rules request.

#### Arguments

- `input_data` *InputModel* - The input data for the request.
- `chunks` *List[str]* - The code chunks.
- `headers` *List[str]* - The headers extracted from the code.
- `file_extension` *str* - The file extension for the generated files.
- `filepath` *str* - The path of the temporary file.

#### Returns

- [ResponseMessageModel](#responsemessagemodel) - The response message containing the URL of the generated ZIP file.

#### Examples

```python
>>> input_data = InputModel(code="def hello():
```

print('Hello')", language="python", request_type="unit_test", model="Llama3.1 70b Instruct")

```python
>>> chunks = ["def hello():
```

print('Hello')"]

```python
>>> headers = ["def hello():"]
>>> filepath = "/tmp/example.py"
>>> process_unit_test_or_business_rules(input_data, chunks, headers, ".py", filepath)
ResponseMessageModel(message="The generated unit_test files can be downloaded from this URL: http://127.0.0.1:8080/public/code_splitter/unit_test_....zip", type="text")
```

#### Signature

```python
def process_unit_test_or_business_rules(
    input_data, chunks, headers, file_extension, filepath
): ...
```
