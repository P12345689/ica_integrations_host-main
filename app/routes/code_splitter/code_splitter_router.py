# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Code Splitter API endpoint for splitting code and generating unit tests or business rules.

...

Usage:
    - Send a POST request to the `/code_splitter/invoke` endpoint with the following parameters:
        - code: The code to be split and analyzed.
        - language: The programming language of the code.
        - max_chunk_size: The maximum size of each code chunk (default: 500).
        - model: The name or ID of the model to use for generating unit tests or business rules (optional, default: None).
        - request_type: The type of request, either "unit_test", "business_rules", "split", or "count_tokens" (default: "unit_test").

Example:
    >>> import requests
    >>> url = "http://localhost:8000/code_splitter/invoke"
    >>> data = {
    ...     "code": "def hello_world():\n    print('Hello, World!')",
    ...     "language": "python",
    ...     "max_chunk_size": 1000,
    ...     "model": "Llama3.1 70b Instruct",
    ...     "request_type": "unit_test"
    ... }
    >>> response = requests.post(url, json=data)
    >>> response.json()
    {
        "status": "success",
        "invocationId": "...",
        "response": [
            {
                "message": "The generated unit test files can be downloaded from this URL:",
                "type": "text"
            },
            {
                "message": "/public/unit_tests_....zip",
                "type": "text"
            }
        ]
    }
"""

import json
import logging
import os
import tempfile
import zipfile
from typing import Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated, List

from .ica_code_splitter.code_splitter import code_splitter
from .ica_code_splitter.token_estimation import estimate_tokens
from .genai_code_splitter.splitter.jobs import create_jobs

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/code_splitter/templates"))
log.debug("Jinja2 environment initialized with template directory.")


class InputModel(BaseModel):
    """Model to validate input data."""

    code: str
    language: str
    max_chunk_size: int = 500
    model: Optional[str] = None
    request_type: Literal["unit_test", "business_rules", "split", "count_tokens"] = "unit_test"


class InputModelGenAI(BaseModel):
    """Model to validate input data."""

    code: str
    request_type: str
    response_mode: Literal["chunk_only", "chunk_and_process", "process_only"] = "chunk_only"
    usecase_id: str
    genai_platform: str
    response_format: str
    transport_mode: str
    chunking_mode: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str
    response: Annotated[List[ResponseMessageModel], Field(min_length=1)]


def get_file_extension(language):
    """
    Get the file extension based on the programming language.

    Args:
        language (str): The programming language.

    Returns:
        str: The corresponding file extension.

    Examples:
        >>> get_file_extension("python")
        '.py'
        >>> get_file_extension("java")
        '.java'
        >>> get_file_extension("unknown")
        '.txt'
    """
    if language == "python":
        return ".py"
    if language == "php":
        return ".php"
    elif language == "java":
        return ".java"
    elif language == "sql":
        return ".sql"
    else:
        return ".txt"


def generate_zip_file(file_contents, headers, file_extension, request_type="split", source_file_name=None):
    """
    Generate a ZIP file containing the file contents and headers.

    Args:
        file_contents (List[str]): The contents of the files to be included in the ZIP.
        headers (List[str]): The headers to be included in the ZIP.
        file_extension (str): The file extension for the generated files.
        request_type (str): The type of request (default: "split").
        source_file_name (str): The name of the source file (optional).

    Returns:
        str: The URL of the generated ZIP file.

    Examples:
        >>> file_contents = ["def hello():\n    print('Hello')", "def world():\n    print('World')"]
        >>> headers = ["def hello():", "def world():"]
        >>> generate_zip_file(file_contents, headers, ".py", request_type="unit_test", source_file_name="example")
        'http://127.0.0.1:8080/public/code_splitter/unit_test_....zip'
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        log.info(f"Generating ZIP file for {request_type} with source file name: {source_file_name}")
        zip_file_name = f"{request_type}_{uuid4()}.zip"
        os.makedirs('public/code_splitter', exist_ok=True)
        zip_file_path = os.path.join("public/code_splitter", zip_file_name)
        with zipfile.ZipFile(zip_file_path, "w") as zip_file:
            for i, content in enumerate(file_contents):
                if source_file_name:
                    file_name = f"{source_file_name}_{request_type}_{i}{file_extension}"
                else:
                    file_name = f"{request_type}_{i}{file_extension}"
                zip_file.writestr(file_name, content)

            headers_file_name = "headers.txt"
            zip_file.writestr(headers_file_name, "\n".join(headers))

   
    zip_file_url = f"{SERVER_NAME}/public/code_splitter/{zip_file_name}"
    log.info(f"Generated ZIP file URL: {zip_file_url}")
    return zip_file_url


def process_unit_test_or_business_rules(input_data, chunks, headers, file_extension, filepath):
    """
    Process unit test or business rules request.

    Args:
        input_data (InputModel): The input data for the request.
        chunks (List[str]): The code chunks.
        headers (List[str]): The headers extracted from the code.
        file_extension (str): The file extension for the generated files.
        filepath (str): The path of the temporary file.

    Returns:
        ResponseMessageModel: The response message containing the URL of the generated ZIP file.

    Examples:
        >>> input_data = InputModel(code="def hello():\n    print('Hello')", language="python", request_type="unit_test", model="Llama3.1 70b Instruct")
        >>> chunks = ["def hello():\n    print('Hello')"]
        >>> headers = ["def hello():"]
        >>> filepath = "/tmp/example.py"
        >>> process_unit_test_or_business_rules(input_data, chunks, headers, ".py", filepath)
        ResponseMessageModel(message="The generated unit_test files can be downloaded from this URL: http://127.0.0.1:8080/public/code_splitter/unit_test_....zip", type="text")
    """
    if input_data.request_type == "unit_test":
        template_name = "unit_test_template.jinja"
    elif input_data.request_type == "business_rules":
        template_name = "business_rules_template.jinja"
    else:
        raise HTTPException(status_code=400, detail="Invalid request type")

    log.info(f"Processing {input_data.request_type} request")

    generated_files = []

    for i, chunk in enumerate(chunks):
        log.info(f"Processing chunk {i+1}/{len(chunks)}")
        template = template_env.get_template(template_name)
        rendered_code = template.render(code=chunk, headers=headers)

        consulting_assistants_model = ICAClient()
        llm_response = consulting_assistants_model.prompt_flow(model_id_or_name=input_data.model, prompt=rendered_code)

        if llm_response is None:
            llm_response = "No response from LLM"

        log.debug(f"Received from LLM for chunk {i+1}/{len(chunks)}:\n{llm_response}")
        generated_files.append(llm_response)

    source_file_name = os.path.splitext(os.path.basename(filepath))[0]
    zip_file_url = generate_zip_file(
        generated_files,
        headers,
        file_extension,
        request_type=input_data.request_type,
        source_file_name=source_file_name,
    )

    response_dict = ResponseMessageModel(
        message=f"The generated {input_data.request_type} files can be downloaded from this URL: {zip_file_url}",
        type="text",
    )
    log.info(f"Processed {input_data.request_type} request successfully")
    return response_dict


def process_split(chunks, headers, file_extension):
    """
    Process the code splitting request.

    Args:
        chunks (List[str]): The code chunks.
        headers (List[str]): The headers extracted from the code.
        file_extension (str): The file extension for the generated files.

    Returns:
        ResponseMessageModel: The response message containing the URL of the generated ZIP file.

    Examples:
        >>> chunks = ["def hello():\n    print('Hello')", "def world():\n    print('World')"]
        >>> headers = ["def hello():", "def world():"]
        >>> process_split(chunks, headers, ".py")
        ResponseMessageModel(message="The split code files can be downloaded from this URL: http://127.0.0.1:8080/public/code_splitter/split_....zip", type="text")
    """
    log.info("Processing code splitting request")
    zip_file_url = generate_zip_file(chunks, headers, file_extension)
    response_dict = ResponseMessageModel(
        message=f"The split code files can be downloaded from this URL: {zip_file_url}",
        type="text",
    )
    log.info("Processed code splitting request successfully")
    return response_dict


def process_count_tokens(code, chunks):
    """
    Process the token counting request.

    Args:
        code (str): The original code.
        chunks (List[str]): The code chunks.

    Returns:
        ResponseMessageModel: The response message containing the token counts.

    Examples:
        >>> code = "def hello():\n    print('Hello')\n\ndef world():\n    print('World')"
        >>> chunks = ["def hello():\n    print('Hello')", "def world():\n    print('World')"]
        >>> process_count_tokens(code, chunks)
        ResponseMessageModel(message="Total tokens in the code: 12\n\nTokens per chunk:\nChunk 1: 6 tokens\nChunk 2: 6 tokens\n", type="text")
    """
    log.info("Processing token counting request")
    total_tokens = estimate_tokens(code)
    chunk_tokens = [estimate_tokens(chunk) for chunk in chunks]
    response_message = f"Total tokens in the code: {total_tokens}\n\n"
    response_message += "Tokens per chunk:\n"
    for i, tokens in enumerate(chunk_tokens):
        response_message += f"Chunk {i+1}: {tokens} tokens\n"

    response_dict = ResponseMessageModel(message=response_message, type="text")
    log.info("Processed token counting request successfully")
    return response_dict


def add_custom_routes(app: FastAPI) -> None:
    """Add custom routes to the FastAPI app."""

    @app.api_route("/code_splitter/invoke", methods=["POST"])
    async def invoke(request: Request) -> OutputModel:
        """
        Handle POST requests to the invoke endpoint.

        Args:
            request (Request): The incoming request.

        Returns:
            OutputModel: The output response.

        Raises:
            HTTPException: If there is an error during processing.
        """
        invocation_id = str(uuid4())  # Generate a unique invocation ID
        log.info(f"Received request with invocation ID: {invocation_id}")

        try:
            data = await request.json()
            if data.get("request_type", "").startswith("custom_genai"):
                input_data = InputModelGenAI(**data)
                response, *_ = await create_jobs(input_data.code, input_data.usecase_id, input_data.genai_platform, input_data.response_mode)
                
                response_dict = ResponseMessageModel(message=response, type="text")
                response_data = OutputModel(invocationId=invocation_id, response=[response_dict])
                return response_data
            input_data = InputModel(**data)
            log.info(f"Input data: {input_data}")
        except json.JSONDecodeError:
            log.error("Invalid JSON")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            log.error(f"Validation error: {e.errors()}")
            raise HTTPException(status_code=422, detail=e.errors())

        file_extension = get_file_extension(input_data.language)
        filepath = f"/tmp/{uuid4()}{file_extension}"
        output_dir = tempfile.mkdtemp()
        log.info(f"File extension: {file_extension}, Filepath: {filepath}, Output directory: {output_dir}")

        try:
            chunks, headers = code_splitter(
                code=input_data.code,
                filepath=filepath,
                output_dir=output_dir,
                language_str=input_data.language,
                max_tokens=input_data.max_chunk_size,
                estimation_method="max",
                preprocess=True,
            )
            log.info(f"Code splitting completed. Number of chunks: {len(chunks)}")
            log.info(f"Headers: {headers}")

            if input_data.request_type in ["unit_test", "business_rules"]:
                response_dict = process_unit_test_or_business_rules(input_data, chunks, headers, file_extension, filepath)
            elif input_data.request_type == "split":
                response_dict = process_split(chunks, headers, file_extension)
            elif input_data.request_type == "count_tokens":
                response_dict = process_count_tokens(input_data.code, chunks)
            else:
                log.error(f"Invalid request type: {input_data.request_type}")
                raise HTTPException(status_code=400, detail="Invalid request type")

        except Exception as e:
            log.error(f"Error during processing: {str(e)}")
            raise HTTPException(status_code=500, detail="Error during processing")

        response_data = OutputModel(invocationId=invocation_id, response=[response_dict])
        log.info(f"Processed request with invocation ID: {invocation_id} successfully")
        return response_data
