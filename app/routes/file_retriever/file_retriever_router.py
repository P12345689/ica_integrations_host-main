# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: File Retriever integration router.

This module provides routes for retrieving files from URLs and converting them to text.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import uuid4
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from langchain_community.document_loaders import (
    PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredHTMLLoader,
    CSVLoader, UnstructuredExcelLoader, UnstructuredPowerPointLoader,
    TextLoader, UnstructuredFileLoader
)
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3 70B Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 30))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/file_retriever/templates"))

class FileRetrieverInputModel(BaseModel):
    """Model to validate input data for file retrieval queries."""
    url: str = Field(..., description="The URL of the file to retrieve and convert")

class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""
    message: str
    type: str = "text"

class OutputModel(BaseModel):
    """Model to structure the output response."""
    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]

async def fetch_file(url: str) -> bytes:
    """
    Fetches a file from the given URL using httpx.

    Args:
        url (str): The URL of the file to fetch.

    Returns:
        bytes: The content of the file.

    Raises:
        HTTPException: If there's an error fetching the file.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.content
    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error occurred while fetching file: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        log.error(f"An error occurred while fetching file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_file_extension(url: str) -> str:
    """
    Extracts the file extension from the URL, ignoring query parameters.

    Args:
        url (str): The URL of the file.

    Returns:
        str: The file extension (including the dot).
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    return os.path.splitext(path)[1].lower()

def convert_to_text(file_content: bytes, url: str) -> str:
    """
    Converts the file content to text using the appropriate langchain loader.

    Args:
        file_content (bytes): The content of the file.
        url (str): The URL of the file, used to determine the file type.

    Returns:
        str: The extracted text from the file.

    Raises:
        ValueError: If the file type is not supported.
    """
    file_extension = get_file_extension(url)
    
    loaders = {
        '.pdf': PyPDFLoader,
        '.docx': UnstructuredWordDocumentLoader,
        '.doc': UnstructuredWordDocumentLoader,
        '.pptx': UnstructuredPowerPointLoader,
        '.ppt': UnstructuredPowerPointLoader,
        '.xlsx': UnstructuredExcelLoader,
        '.xls': UnstructuredExcelLoader,
        '.csv': CSVLoader,
        '.html': UnstructuredHTMLLoader,
        '.htm': UnstructuredHTMLLoader,
        '.txt': TextLoader,
        '.py': TextLoader,
    }

    if file_extension not in loaders:
        raise ValueError(f"Unsupported file type: {file_extension}")

    loader_class = loaders[file_extension]
    
    with NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:
        if loader_class == PyPDFLoader:
            loader = loader_class(temp_file_path)
            documents = loader.load()
        elif loader_class in [CSVLoader, TextLoader]:
            loader = loader_class(temp_file_path)
            documents = loader.load()
        else:
            loader = loader_class(temp_file_path, mode="elements")
            documents = loader.load()
        
        return "\n\n".join(doc.page_content for doc in documents)
    finally:
        os.unlink(temp_file_path)

def add_custom_routes(app: FastAPI):
    @app.post("/system/file_retriever/retrievers/get_file_content/invoke")
    @app.post("/file_retriever/invoke")
    async def get_file_content(request: Request) -> OutputModel:
        """
        Handle POST requests to retrieve and convert files to text.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or file processing fails.
        """
        invocation_id = str(uuid4())
        
        try:
            data = await request.json()
            input_data = FileRetrieverInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {e}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            file_content = await fetch_file(input_data.url)
            
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                text_content_future = executor.submit(convert_to_text, file_content, input_data.url)
                text_content = text_content_future.result()

            response_template = template_env.get_template("file_retriever_response.jinja")
            rendered_response = response_template.render(content=text_content)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        
        except ValueError as e:
            log.error(f"Unsupported file type: {e}")
            error_message = f"Unsupported file type. The file type is not supported for conversion."
            response_message = ResponseMessageModel(message=error_message)
            return OutputModel(status="error", invocationId=invocation_id, response=[response_message])
        
        except Exception as e:
            log.error(f"Error processing file: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/experience/file_retriever/ask_file_content/invoke")
    async def ask_file_content(request: Request) -> OutputModel:
        """
        Handle POST requests to retrieve, convert, and analyze files using an LLM.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or file processing fails.
        """
        invocation_id = str(uuid4())
        
        try:
            data = await request.json()
            input_data = FileRetrieverInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {e}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            file_content = await fetch_file(input_data.url)
            file_extension = os.path.splitext(input_data.url)[1].lower()
            
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                text_content_future = executor.submit(convert_to_text, file_content, file_extension)
                text_content = text_content_future.result()

            prompt_template = template_env.get_template("file_retriever_prompt.jinja")
            rendered_prompt = prompt_template.render(content=text_content)

            client = ICAClient()
            
            async def call_prompt_flow():
                return await asyncio.to_thread(
                    client.prompt_flow,
                    model_id_or_name=DEFAULT_MODEL,
                    prompt=rendered_prompt
                )

            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                llm_response_future = executor.submit(asyncio.run, call_prompt_flow())
                llm_response = llm_response_future.result()

            response_template = template_env.get_template("file_retriever_response.jinja")
            rendered_response = response_template.render(content=llm_response)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        
        except ValueError as e:
            log.error(f"Unsupported file type: {e}")
            error_message = f"Unsupported file type. The file type is not supported for conversion."
            response_message = ResponseMessageModel(message=error_message)
            return OutputModel(status="error", invocationId=invocation_id, response=[response_message])
        
        except Exception as e:
            log.error(f"Error processing file: {e}")
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import doctest
    doctest.testmod()