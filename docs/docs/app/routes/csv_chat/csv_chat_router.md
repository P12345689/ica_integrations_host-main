# Csv Chat Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Csv Chat](./index.md#csv-chat) / Csv Chat Router

> Auto-generated documentation for [app.routes.csv_chat.csv_chat_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py) module.

#### Attributes

- `DEFAULT_MODEL` - Constants: os.getenv('ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME', 'Llama3.1 70b Instruct')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/csv_chat/templates'))


- [Csv Chat Router](#csv-chat-router)
  - [CSVChatInputModel](#csvchatinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [execute_code_with_timeout](#execute_code_with_timeout)
  - [extract_column_unique_values](#extract_column_unique_values)
  - [fix_syntax_errors](#fix_syntax_errors)
  - [load_dataframe](#load_dataframe)
  - [lower_if_string](#lower_if_string)
  - [process_csv_chat](#process_csv_chat)
  - [sanitize_code](#sanitize_code)
  - [sanitize_user_input](#sanitize_user_input)

## CSVChatInputModel

[Show source in csv_chat_router.py:105](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L105)

Model to validate input data for CSV chat queries.

#### Signature

```python
class CSVChatInputModel(BaseModel): ...
```



## OutputModel

[Show source in csv_chat_router.py:116](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L116)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in csv_chat_router.py:111](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L111)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in csv_chat_router.py:308](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L308)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## execute_code_with_timeout

[Show source in csv_chat_router.py:280](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L280)

Execute the code with a timeout.

#### Signature

```python
async def execute_code_with_timeout(exec_func: str, df: pd.DataFrame) -> str: ...
```



## extract_column_unique_values

[Show source in csv_chat_router.py:122](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L122)

Extract unique values for each column in the dataframe.

#### Signature

```python
def extract_column_unique_values(df: pd.DataFrame) -> str: ...
```



## fix_syntax_errors

[Show source in csv_chat_router.py:270](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L270)

Attempt to fix common syntax errors in the generated code.

#### Signature

```python
def fix_syntax_errors(code: str) -> str: ...
```



## load_dataframe

[Show source in csv_chat_router.py:132](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L132)

Load a dataframe from various input sources.

#### Signature

```python
async def load_dataframe(
    csv_content: Optional[str] = None,
    file_url: Optional[str] = None,
    file: Optional[UploadFile] = None,
) -> pd.DataFrame: ...
```



## lower_if_string

[Show source in csv_chat_router.py:172](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L172)

Convert to lowercase if the input is a string.

#### Signature

```python
def lower_if_string(x): ...
```



## process_csv_chat

[Show source in csv_chat_router.py:208](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L208)

Process the CSV chat query using pandas and LLM.

#### Signature

```python
async def process_csv_chat(
    df: pd.DataFrame, query: str, is_retry: bool = False, error_message: str = ""
) -> str: ...
```



## sanitize_code

[Show source in csv_chat_router.py:241](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L241)

Sanitize the code to prevent common issues and ensure safety.

#### Signature

```python
def sanitize_code(code: str) -> str: ...
```



## sanitize_user_input

[Show source in csv_chat_router.py:176](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/csv_chat/csv_chat_router.py#L176)

Sanitize user input to prevent potential security issues.

#### Arguments

- `input_str` *str* - The input string to be sanitized.

#### Returns

- `Optional[str]` - The sanitized input string if it's safe, or None if it contains blocked words.

#### Signature

```python
def sanitize_user_input(input_str: str) -> Optional[str]: ...
```
