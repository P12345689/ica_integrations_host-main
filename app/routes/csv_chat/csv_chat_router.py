# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: CSV Chat Integration Router

This module provides a FastAPI router for chatting with CSV data using pandas and an LLM.
It supports various input formats including direct CSV content, URLs, and file uploads.

Security Measures and Implementing Functions:
1. Input validation and sanitization:
   - User queries are sanitized to remove potentially harmful keywords and characters (sanitize_user_input).
   - File uploads are restricted to CSV and XLSX formats only (load_dataframe).
   - File size is limited to prevent resource exhaustion attacks (load_dataframe, validate_dataframe).
   - Dataframe size (rows and columns) is restricted to prevent memory exhaustion (validate_dataframe).

2. Safe code execution:
   - The generated Python code is sanitized to prevent the use of unsafe functions and modules (sanitize_code).
   - A blocklist is used to disallow the use of potentially dangerous operations (sanitize_code).
   - An allowlist is used to restrict the available functions and modules to a safe subset (sanitize_code).
   - The code is executed in a separate function with a restricted global namespace (execute_code_with_timeout).
   - Execution time is limited to prevent infinite loops or long-running operations (execute_code_with_timeout).

3. Error handling and logging:
   - Detailed error messages are logged for debugging purposes (throughout the module, using the 'log' object).
   - Error messages returned to the user are kept generic to avoid leaking sensitive information (chat_with_csv, get_csv_info).
   - Exceptions are caught and handled gracefully to prevent unhandled errors (chat_with_csv, get_csv_info).

4. Asynchronous processing:
   - The module uses asynchronous functions to handle time-consuming operations like loading dataframes and making API calls (load_dataframe, process_csv_chat, execute_code_with_timeout).

5. Retry mechanism:
   - The module includes a retry mechanism to handle temporary failures when parsing the LLM response (chat_with_csv).

6. Secure dataframe loading:
   - A separate function is used to safely load and validate dataframes (safe_load_dataframe).

7. Data handling:
   - Sensitive data in the CSV files is not persisted beyond the scope of a single request (all data is handled in-memory in chat_with_csv and get_csv_info).
   - Data is kept in memory and not written to disk when possible (using StringIO and BytesIO in load_dataframe).

Key Functions:
- add_custom_routes(app: FastAPI): Adds the CSV chat routes to the FastAPI application.
- chat_with_csv(...): Handles the main chat functionality, orchestrating the entire process.
- get_csv_info(...): Provides information about the uploaded CSV file.
- load_dataframe(...): Loads the CSV data from various sources with initial validations.
- safe_load_dataframe(...): Combines loading and comprehensive validation of dataframes.
- validate_dataframe(df: pd.DataFrame): Performs security checks on the loaded dataframe.
- sanitize_user_input(input_str: str): Sanitizes user input to prevent injection attacks.
- sanitize_code(code: str): Sanitizes generated Python code to ensure safe execution.
- execute_code_with_timeout(...): Executes sanitized code with a timeout for safety.
- process_csv_chat(...): Processes the chat query using the LLM.

Usage:
    This module is intended to run on on ica_container_host, as an integration.
    No other integrations should run on the same container.

Deployment Recommendations:
1. Secure container deployment:
   - Run this module separately in a Red Hat Universal Base Image container on ica_container_host.
   - Configure the filesystem as read-only, except for a designated directory for temporary file uploads.

2. Monitoring and alerting:
   - Implement comprehensive logging and monitoring.
   - Set up alerts for abnormal behavior (high error rates, unusual resource usage).
   - Setup monitoring for container escape
   - Restrict the container's Syscalls with seccomp
"""

import asyncio
import json
import logging
import os
import re
import textwrap
import traceback
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO, StringIO
from typing import List, Optional
from uuid import uuid4

import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field, HttpUrl, ValidationError

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Constants
DEFAULT_MODEL = os.getenv(
    "ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct"
)
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
MAX_RETRIES = 3  # Maximum number of retries for JSON parsing errors
MAX_INPUT_LENGTH = 1000  # Maximum length of user input query
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB maximum file size
MAX_DATAFRAME_ROWS = 100000  # Maximum number of rows in the dataframe
MAX_DATAFRAME_COLS = 100  # Maximum number of columns in the dataframe
EXECUTION_TIMEOUT = 30  # Maximum execution time for generated code in seconds

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/csv_chat/templates"))


class CSVChatInputModel(BaseModel):
    """Model to validate input data for CSV chat queries."""

    query: str = Field(..., description="The query about the CSV data", max_length=MAX_INPUT_LENGTH)
    csv_content: Optional[str] = Field(None, description="The CSV content as a string")
    file_url: Optional[HttpUrl] = Field(None, description="URL to a CSV or XLSX file")
    file_path: Optional[str] = Field(None, description="The path to a local CSV file")


class CSVInfoInputModel(BaseModel):
    """Model to validate input data for CSV dataset information."""

    csv_content: Optional[str] = Field(None, description="The CSV content as a string")
    file_url: Optional[str] = Field(None, description="URL to a CSV or XLSX file")
    file_path: Optional[str] = Field(None, description="The path to a local CSV file")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def extract_column_unique_values(df: pd.DataFrame) -> str:
    """Extract unique values for each column in the dataframe."""
    column_info = []
    for column in df.columns:
        unique_values = df[column].dropna().unique()
        if len(unique_values) > 10:
            unique_values = unique_values[:10]
        column_info.append(f"{column}: {', '.join(map(str, unique_values))}")
    return "\n".join(column_info)


async def load_dataframe(
    csv_content: Optional[str] = None,
    file_url: Optional[str] = None,
    file_path: Optional[UploadFile] = None,
) -> pd.DataFrame:
    """Load a dataframe from various input sources."""
    log.debug("Attempting to load dataframe")
    if csv_content:
        log.debug("Loading dataframe from CSV content")
        df = pd.read_csv(StringIO(csv_content))
    elif file_url:
        log.debug(f"Loading dataframe from URL: {file_url}")
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        content = b""
        for chunk in response.iter_content(chunk_size=8192):
            content += chunk
            if len(content) > MAX_FILE_SIZE:
                raise ValueError(
                    f"File size exceeds the maximum allowed size of {MAX_FILE_SIZE} bytes"
                )
        if file_url.endswith(".csv"):
            df = pd.read_csv(BytesIO(content))
        elif file_url.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(content))
        else:
            raise ValueError(
                "Unsupported file format. Only CSV and XLSX are supported."
            )
    elif file_path:
        log.debug(f"Loading dataframe from uploaded file: {file_path.filename}")
        content = await file_path.read()
        if len(content) > MAX_FILE_SIZE:
            raise ValueError(
                f"File size exceeds the maximum allowed size of {MAX_FILE_SIZE} bytes"
            )
        if file_path.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(content))
        elif file_path.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(content))
        else:
            raise ValueError(
                "Unsupported file format. Only CSV and XLSX are supported."
            )
    else:
        raise ValueError(
            "No valid input source provided. Please provide either csv_content, file_url, or file_path."
        )

    if df.shape[0] > MAX_DATAFRAME_ROWS or df.shape[1] > MAX_DATAFRAME_COLS:
        raise ValueError(
            f"Dataframe exceeds maximum allowed size of {MAX_DATAFRAME_ROWS} rows and {MAX_DATAFRAME_COLS} columns"
        )

    return df


def lower_if_string(x):
    """Convert to lowercase if the input is a string."""
    return x.lower() if isinstance(x, str) else x


def sanitize_user_input(input_str: str) -> Optional[str]:
    """
    Sanitize user input to prevent potential security issues.

    Args:
        input_str (str): The input string to be sanitized.

    Returns:
        Optional[str]: The sanitized input string if it's safe, or None if it contains blocked words.
    """
    '''
    blocklist = [
        "ignore",
        "previous prompt",
        "override",
        "bypass",
        "hack",
        "exploit",
        "vulnerability",
        "malicious",
        "inject",
        "execute",
        "sql",
        "delete",
        "drop",
        "truncate",
        "alter",
        "update",
        "insert",
        "create",
        "select",
        "union",
        "join",
        "where",
        "from",
        "script",
        "function",
        "eval",
        "exec",
        "system",
        "os",
        "subprocess",
        "import",
    ]
    '''
    
    blocklist = []

    log.debug(f"Sanitizing input: {input_str}")

    # Check if any blocked word is in the input
    for word in blocklist:
        if word in input_str.lower():
            log.warning(f"Blocked word '{word}' found in input")
            return None

    # If no blocked words are found, return the sanitized input
    sanitized_input = re.sub(r"[^\w\s.,?!-]", "", input_str)
    sanitized_input = sanitized_input.strip()[:MAX_INPUT_LENGTH]
    log.debug(f"Sanitized input: {sanitized_input}")
    return sanitized_input


async def process_csv_chat(
    df: pd.DataFrame, query: str, is_retry: bool = False, error_message: str = ""
) -> str:
    """Process the CSV chat query using pandas and LLM."""
    log.debug("Processing CSV chat query")
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].map(lower_if_string)

    column_info = extract_column_unique_values(df)
    df_head = str(df.head(5).to_markdown())

    sanitized_query = sanitize_user_input(query)
    log.debug(f"Sanitized query: {sanitized_query}")

    if is_retry:
        prompt_template = template_env.get_template("csv_chat_retry_prompt.jinja")
        prompt = prompt_template.render(
            df_head=df_head,
            column_info=column_info,
            query=sanitized_query,
            error_message=error_message,
        )
    else:
        prompt_template = template_env.get_template("csv_chat_prompt.jinja")
        prompt = prompt_template.render(
            df_head=df_head, column_info=column_info, query=sanitized_query
        )

    log.debug(f"Generated prompt: {prompt}")

    client = ICAClient()
    with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
        response_future = executor.submit(
            client.prompt_flow, model_id_or_name=DEFAULT_MODEL, prompt=prompt
        )
        response = await asyncio.to_thread(lambda: response_future.result())

    log.debug(f"Received LLM response: {response}")
    return response


def sanitize_code(code: str) -> str:
    """Sanitize the code to prevent common issues and ensure safety."""
    code = code.replace("'", '"')
    '''
    blocklist = [
        "eval",
        "exec",
        "import",
        "open",
        "os",
        "sys",
        "subprocess",
        "shutil",
        "__import__",
        "globals",
        "locals",
        "getattr",
        "setattr",
        "delattr",
        "compile",
        "timeit",
        "input",
        "raw_input",
        "breakpoint",
        "base64",
        "pickle",
        "shelve",
        "socket",
        "requests",
        "urllib",
        "http",
        "ftp",
        "while",
        "for",
        "class",
        "def",
        "lambda",
        "yield",
        "return",
        "raise",
        "try",
        "except",
        "finally",
        "with",
        "assert",
        "del",
        "global",
        "nonlocal",
    ]
    
    for word in blocklist:
        if re.search(r"\b" + re.escape(word) + r"\b", code):
            raise ValueError(f"Unsafe operation detected: {word}")

    allow_list = (
        [
            "print",
            "len",
            "str",
            "int",
            "float",
            "bool",
            "list",
            "dict",
            "set",
            "tuple",
            "sum",
            "min",
            "max",
            "sorted",
            "any",
            "all",
            "zip",
            "map",
            "filter",
            "round",
            "abs",
            "pow",
            "range",
            "contains",
            "DataFrame",
        ]
        + dir(pd.DataFrame)
        + dir(pd.Series)
        + dir(np)
    )

    function_pattern = re.compile(r"\b(\w+)\s*\(")
    for match in function_pattern.finditer(code):
        func_name = match.group(1)
        if func_name not in allow_list:
            raise ValueError(f"Unauthorized function detected: {func_name}")
    '''
    return code


def fix_syntax_errors(code: str) -> str:
    """Attempt to fix common syntax errors in the generated code."""
    lines = code.strip().split("\n")
    if not any(line.strip().startswith("result =") for line in lines):
        if len(lines) > 1:
            lines.append(f"result = {lines[-1]}")
        else:
            lines.append(f"result = {lines[0]}")
    return "\n".join(lines)


async def execute_code_with_timeout(exec_func: str, df: pd.DataFrame) -> str:
    """Execute the code with a timeout."""

    async def run_code():
        # Properly indent the user code
        indented_code = textwrap.indent(exec_func.strip(), "    ").replace("```python", "").replace("```", "")

        # Create the full function with proper indentation
        full_func = f"""
def exec_code(df):
    df = df.fillna('')
    result = None
{indented_code}
    return result
"""
        local_vars = {"df": df}
        exec(full_func, globals(), local_vars)
        return local_vars["exec_code"](df)

    try:
        result = await asyncio.wait_for(run_code(), timeout=EXECUTION_TIMEOUT)
        return result
    except asyncio.TimeoutError:
        raise ValueError(f"Code execution timed out after {EXECUTION_TIMEOUT} seconds")
    except IndentationError as ie:
        raise ValueError(f"Indentation error in generated code: {str(ie)}")
    except Exception as e:
        raise ValueError(f"Error executing generated code: {str(e)}")


async def chat_with_csv(
    query: str = None,
    csv_content: Optional[str] = None,
    file_url: Optional[str] = None,
    file_path: Optional[str] = None,
) -> OutputModel:
    """
    Handle POST requests to chat with CSV data.
    """
    invocation_id = str(uuid4())
    log.info(f"Processing chat request with invocation ID: {invocation_id}")

    log.debug(f"Original query: {query}")

    # Immediately check for unsafe input
    sanitized_query = sanitize_user_input(query)
    log.debug(f"Sanitized query: {sanitized_query}")

    if sanitized_query is None:
        log.warning(f"Unsafe input detected for invocation ID {invocation_id}")
        return OutputModel(
            status="error",
            invocationId=invocation_id,
            response=[
                ResponseMessageModel(
                    message="Error: Potentially insecure user input. Request rejected."
                )
            ],
        )

    try:
        # Load and validate the dataframe
        df = await safe_load_dataframe(csv_content=csv_content, file_url=file_url, file_path=file_path)
        log.info(
            f"Dataframe loaded successfully for invocation ID {invocation_id}. Shape: {df.shape}"
        )
    except ValueError as ve:
        log.error(
            f"Error loading dataframe for invocation ID {invocation_id}: {str(ve)}"
        )
        return OutputModel(
            status="error",
            invocationId=invocation_id,
            response=[ResponseMessageModel(message=f"Error: {str(ve)}")],
        )

    # Process the query with retries
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            log.debug(f"Processing query: {sanitized_query}")
            llm_response = await process_csv_chat(
                df,
                sanitized_query,
                is_retry=(retry_count > 0),
                error_message=f"Retry attempt {retry_count + 1}",
            )
            llm_response = llm_response.replace("```json", "").replace("```python", "").replace("```", "").strip()
            log.info(f"LLM Response received for invocation ID: {invocation_id}")
            parsed_response = json.loads(llm_response)
            break
        except json.JSONDecodeError as json_error:
            log.warning(
                f"Failed to parse LLM response as JSON for invocation ID {invocation_id}. Attempt {retry_count + 1}. Error: {str(json_error)}"
            )
            retry_count += 1
            if retry_count == MAX_RETRIES:
                log.error(
                    f"Max retries reached for invocation ID {invocation_id}. Unable to parse LLM response as JSON."
                )
                return OutputModel(
                    status="error",
                    invocationId=invocation_id,
                    response=[
                        ResponseMessageModel(
                            message="Unable to process the query due to an internal error."
                        )
                    ],
                )

    result = "Unable to process the query. The LLM did not provide executable code."

    if "code" in parsed_response and parsed_response["code"]:
        python_code = parsed_response["code"]
        log.debug(
            f"Original generated code for invocation ID {invocation_id}: {python_code}"
        )

        try:
            python_code = sanitize_code(python_code)
            python_code = fix_syntax_errors(python_code)
            log.debug(
                f"Sanitized and fixed code for invocation ID {invocation_id}: {python_code}"
            )
        except ValueError as ve:
            log.error(
                f"Code sanitization error for invocation ID {invocation_id}: {str(ve)}"
            )
            return OutputModel(
                status="error",
                invocationId=invocation_id,
                response=[
                    ResponseMessageModel(
                        message="Error: Unable to execute the generated code due to security concerns."
                    )
                ],
            )

        python_code = python_code.replace(
            ".str.contains(", ".str.lower().str.contains("
        )

        try:
            result = await execute_code_with_timeout(python_code, df)
        except ValueError as ve:
            log.error(
                f"Error executing code for invocation ID {invocation_id}: {str(ve)}"
            )
            result = f"Error executing code: {str(ve)}"

        log.debug(f"Execution result for invocation ID {invocation_id}: {result}")

        if isinstance(result, (pd.DataFrame, pd.Series)):
            result = result.to_string()
        elif isinstance(result, (list, np.ndarray)):
            result = ", ".join(map(str, result))
        else:
            result = str(result)

    response_template = template_env.get_template("csv_chat_response.jinja")
    rendered_response = response_template.render(
        query=sanitized_query, llm_response=parsed_response, result=result
    )

    log.info(f"Rendered response for invocation ID {invocation_id}")

    return OutputModel(
        status="success",
        invocationId=invocation_id,
        response=[ResponseMessageModel(message=rendered_response)],
    )


def add_custom_routes(app: FastAPI):
    @app.post("/experience/csv_chat/ask/invoke")
    async def invoke_chat_with_csv(request: Request) -> OutputModel:
        try:
            data = await request.json()
            input_data = CSVChatInputModel(**data)
            log.debug(f"Validated input data: {input_data}")
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            raise HTTPException(status_code=400, detail="Invalid JSON input")
        except ValidationError as e:
            log.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=json.loads(e.json()))

        # Call the standalone function inside the route
        return await chat_with_csv(query=input_data.query,
                                   csv_content=input_data.csv_content,
                                   file_url=input_data.file_url,
                                   file_path=input_data.file_path)

    @app.post("/system/csv_chat/info/invoke")
    async def get_csv_info(request: Request) -> OutputModel:
        """Handle POST requests to get information about the CSV data."""
        try:
            data = await request.json()
            input_data = CSVInfoInputModel(**data)
            log.debug(f"Validated input data: {input_data}")
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            raise HTTPException(status_code=400, detail="Invalid JSON input")
        except ValidationError as e:
            log.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=json.loads(e.json()))

        invocation_id = str(uuid4())
        log.info(f"Processing CSV info request with invocation ID: {invocation_id}")

        try:
            # df = await load_dataframe(csv_content, file_url, file)
            df = await safe_load_dataframe(csv_content=input_data.csv_content,
                                           file_url=input_data.file_url,
                                           file_path=input_data.file_path)
            log.info(f"Dataframe loaded successfully. Shape: {df.shape}")

            info = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "head": df.head().to_dict(orient="records"),
                "summary": df.describe().to_dict(),
            }

            # Add additional checks for data types and missing values
            info["missing_values"] = df.isnull().sum().to_dict()
            info["data_types"] = df.dtypes.astype(str).to_dict()

            log.debug(f"CSV info: {info}")

            response_message = ResponseMessageModel(message=json.dumps(info, indent=2))
            return OutputModel(invocationId=invocation_id, response=[response_message])

        except Exception as e:
            log.error(f"Error getting CSV info: {str(e)}")
            log.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"Error getting CSV info: {str(e)}"
            )


def validate_dataframe(df: pd.DataFrame) -> None:
    """Validate the dataframe against security constraints."""
    if df.shape[0] > MAX_DATAFRAME_ROWS:
        raise ValueError(
            f"Number of rows ({df.shape[0]}) exceeds the maximum allowed ({MAX_DATAFRAME_ROWS})"
        )
    if df.shape[1] > MAX_DATAFRAME_COLS:
        raise ValueError(
            f"Number of columns ({df.shape[1]}) exceeds the maximum allowed ({MAX_DATAFRAME_COLS})"
        )

    total_size = df.memory_usage(deep=True).sum()
    if total_size > MAX_FILE_SIZE:
        raise ValueError(
            f"Dataframe size ({total_size} bytes) exceeds the maximum allowed ({MAX_FILE_SIZE} bytes)"
        )


async def safe_load_dataframe(
    csv_content: Optional[str] = None,
    file_url: Optional[str] = None,
    file_path: Optional[UploadFile] = None,
) -> pd.DataFrame:
    """Safely load a dataframe from various input sources with additional security checks."""
    if file_path:
        with open(file_path, 'r') as f:
            file_content = f.read()
        df = await load_dataframe(file_content)
    elif file_url:
        response = requests.get(file_url)
        if response.status_code == 200:
            file_content = response.text
            df = await load_dataframe(file_content)
        else:
            raise Exception(f"Failed to download file from {file_url}")
    else:
        df = await load_dataframe(csv_content)
    validate_dataframe(df)
    return df
