# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Batch Execution Integration router.

This module provides routes for processing CSV files and executing batches of prompts.
"""

import asyncio
import csv
import io
import logging
import os
from typing import Any, Dict, List, Optional
from uuid import uuid4

import pandas as pd
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))
MAX_EXECUTIONS_PER_BATCH = int(os.getenv("MAX_EXECUTIONS_PER_BATCH", "100"))
MAX_PROMPT_LENGTH = int(os.getenv("MAX_PROMPT_LENGTH", "1000"))
MAX_CONCURRENT_BATCHES = int(os.getenv("MAX_CONCURRENT_BATCHES", "5"))
EXECUTION_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", "300"))  # 5 minutes

EXECUTION_STORAGE: Dict[str, Dict[str, Any]] = {}
PUBLIC_DIR = "public"
RESULTS_DIR = os.path.join(PUBLIC_DIR, "batch_execution_results")

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Ensure the results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/batch_execution/templates"))


class CSVInputModel(BaseModel):
    """Model to validate input data for CSV processing."""

    csv_content: str = Field(..., description="The CSV content as a string")


class PromptExecutionModel(BaseModel):
    """Model to represent a single prompt execution."""

    prompt: str
    model: Optional[str] = None
    assistant: Optional[str] = None


class BatchExecutionInputModel(BaseModel):
    """Model to validate input data for batch execution."""

    executions: List[PromptExecutionModel]


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


class ResultsModel(BaseModel):
    """Model to structure the results response."""

    status: str
    invocationId: str  # noqa: N815
    message: str
    xlsx_url: Optional[str] = None
    csv_content: Optional[str] = None

class InvocationRequest(BaseModel):
    """Model to validate the invocation ID request."""
    
    invocation_id: str    


def parse_csv(csv_content: str) -> List[Dict[str, Any]]:
    """
    Parse CSV content into a list of dictionaries.

    Args:
        csv_content (str): The CSV content as a string.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the CSV rows.

    Raises:
        ValueError: If the CSV content is invalid or empty.
    """
    try:
        reader = csv.DictReader(io.StringIO(csv_content))
        executions = list(reader)
        if not executions:
            raise ValueError("CSV content is empty")
        return executions
    except csv.Error as e:
        raise ValueError(f"Invalid CSV content: {str(e)}")


async def execute_prompt(
    prompt: str,
    model: Optional[str] = None,
    assistant: Optional[str] = None,
    previous_outputs: Dict[int, str] = {},
) -> str:
    """
    Execute a single prompt, handling variable substitution.

    Args:
        prompt (str): The prompt to execute.
        model (Optional[str]): The model to use for execution.
        assistant (Optional[str]): The assistant to use for execution.
        previous_outputs (Dict[int, str]): A dictionary of previous outputs for variable substitution.

    Returns:
        str: The execution result.

    Raises:
        ValueError: If the prompt is too long.
        TimeoutError: If the execution takes too long.
    """
    if len(prompt) > MAX_PROMPT_LENGTH:
        raise ValueError(f"Prompt exceeds maximum length of {MAX_PROMPT_LENGTH} characters")

    # Perform variable substitution
    for idx, output in previous_outputs.items():
        prompt = prompt.replace(f"${{output.{idx}}}", output)

    client = ICAClient()

    try:
        async with asyncio.timeout(EXECUTION_TIMEOUT):
            if assistant:
                # Use assistant for execution
                response = await asyncio.to_thread(client.chat, assistant_id=assistant, message=prompt)
            else:
                # Use model for execution
                model_to_use = model or DEFAULT_MODEL
                try:
                    response = await asyncio.to_thread(client.prompt_flow, model_id_or_name=model_to_use, prompt=prompt)
                except ValueError as e:
                    log.warning(f"Failed to use specified model '{model_to_use}'. Falling back to default model. Error: {str(e)}")
                    response = await asyncio.to_thread(
                        client.prompt_flow,
                        model_id_or_name=DEFAULT_MODEL,
                        prompt=prompt,
                    )
    except asyncio.TimeoutError:
        raise TimeoutError(f"Execution timed out after {EXECUTION_TIMEOUT} seconds")

    return response


async def process_batch(executions: List[PromptExecutionModel]) -> List[str]:
    """
    Process a batch of prompt executions.

    Args:
        executions (List[PromptExecutionModel]): The list of prompt executions to process.

    Returns:
        List[str]: The list of execution results.

    Raises:
        ValueError: If the number of executions exceeds the maximum allowed.
    """
    if len(executions) > MAX_EXECUTIONS_PER_BATCH:
        raise ValueError(f"Number of executions exceeds maximum of {MAX_EXECUTIONS_PER_BATCH}")

    results = []
    for idx, execution in enumerate(executions):
        try:
            result = await execute_prompt(
                execution.prompt,
                execution.model,
                execution.assistant,
                {i: results[i] for i in range(len(results))},
            )
            results.append(result)
        except Exception as e:
            log.error(f"Error processing execution {idx}: {str(e)}")
            results.append(f"Error: {str(e)}")
    return results


def generate_xlsx(executions: List[Dict[str, Any]], results: List[str]) -> str:
    """
    Generate an XLSX file with execution inputs and outputs and save it in the public directory.

    Args:
        executions (List[Dict[str, Any]]): The list of execution inputs.
        results (List[str]): The list of execution results.

    Returns:
        str: The path to the generated XLSX file.
    """
    df = pd.DataFrame(executions)
    df["result"] = results

    file_name = f"batch_execution_{uuid4()}.xlsx"
    file_path = os.path.join(RESULTS_DIR, file_name)

    df.to_excel(file_path, index=False)

    return file_path


def generate_csv(executions: List[Dict[str, Any]], results: List[str]) -> str:
    """
    Generate a CSV string with execution inputs and outputs.

    Args:
        executions (List[Dict[str, Any]]): The list of execution inputs.
        results (List[str]): The list of execution results.

    Returns:
        str: The CSV content as a string.
    """
    df = pd.DataFrame(executions)
    df["result"] = results

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    return csv_buffer.getvalue()


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/batch_execution/process_csv/invoke")
    async def process_csv(request: Request, background_tasks: BackgroundTasks) -> OutputModel:
        """
        Handle POST requests to process a CSV file and execute prompts.

        Args:
            request (Request): The request object containing the input data.
            background_tasks (BackgroundTasks): FastAPI's BackgroundTasks for async processing.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = CSVInputModel(**data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        try:
            executions = parse_csv(input_data.csv_content)

            async def process_and_store() -> None:
                try:
                    execution_models = [PromptExecutionModel(**execution) for execution in executions]
                    results = await process_batch(execution_models)
                    xlsx_path = generate_xlsx(executions, results)
                    csv_content = generate_csv(executions, results)
                    EXECUTION_STORAGE[invocation_id] = {
                        "status": "completed",
                        "results": results,
                        "xlsx_path": xlsx_path,
                        "csv_content": csv_content,
                    }
                except Exception as e:
                    log.error(f"Error processing batch: {str(e)}")
                    EXECUTION_STORAGE[invocation_id] = {
                        "status": "failed",
                        "error": str(e),
                    }

            background_tasks.add_task(process_and_store)
            EXECUTION_STORAGE[invocation_id] = {"status": "processing"}

            response_message = ResponseMessageModel(
                message=f"CSV processing and execution started. Use invocation ID {invocation_id} to retrieve results.",
                type="text",
            )
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error processing CSV: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

    @app.post("/experience/batch_execution/execute_batch/invoke")
    async def execute_batch(request: Request, background_tasks: BackgroundTasks) -> OutputModel:
        """
        Handle POST requests to execute a batch of prompts.

        Args:
            request (Request): The request object containing the input data.
            background_tasks (BackgroundTasks): FastAPI's BackgroundTasks for async processing.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the maximum concurrent batches limit is reached.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = BatchExecutionInputModel(**data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        if len([execution for execution in EXECUTION_STORAGE.values() if execution["status"] == "processing"]) >= MAX_CONCURRENT_BATCHES:
            raise HTTPException(status_code=429, detail="Maximum number of concurrent batches reached")

        async def process_and_store() -> None:
            try:
                results = await process_batch(input_data.executions)
                xlsx_path = generate_xlsx([exec.dict() for exec in input_data.executions], results)
                csv_content = generate_csv([exec.dict() for exec in input_data.executions], results)
                EXECUTION_STORAGE[invocation_id] = {
                    "status": "completed",
                    "results": results,
                    "xlsx_path": xlsx_path,
                    "csv_content": csv_content,
                }
            except Exception as e:
                log.error(f"Error processing batch: {str(e)}")
                EXECUTION_STORAGE[invocation_id] = {"status": "failed", "error": str(e)}

        background_tasks.add_task(process_and_store)
        EXECUTION_STORAGE[invocation_id] = {"status": "processing"}

        response_message = ResponseMessageModel(
            message=f"Batch execution started. Use invocation ID {invocation_id} to check status and retrieve results.",
            type="text",
        )
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/system/batch_execution/results")
    async def get_execution_results(request: InvocationRequest) -> ResultsModel:
        """
        Handle POST requests to retrieve the status and results of a batch execution.

        Args:
            request (InvocationRequest): The request body containing the invocation ID.

        Returns:
            ResultsModel: The status and results of the batch execution.

        Raises:
            HTTPException: If the invocation ID is not found.
        """
        invocation_id = request.invocation_id
        if invocation_id not in EXECUTION_STORAGE:
            raise HTTPException(status_code=404, detail="Invocation ID not found")

        execution_data = EXECUTION_STORAGE[invocation_id]
        status = execution_data["status"]

        if status == "processing":
            return ResultsModel(
                status=status,
                invocationId=invocation_id,
                message="Execution is still processing.",
            )
        elif status == "failed":
            return ResultsModel(
                status=status,
                invocationId=invocation_id,
                message=f"Execution failed. Error: {execution_data['error']}",
            )
        elif status == "completed":
            xlsx_url = f"{SERVER_NAME}/public/batch_execution_results/{os.path.basename(execution_data['xlsx_path'])}"
            return ResultsModel(
                status=status,
                invocationId=invocation_id,
                message="Execution completed successfully.",
                xlsx_url=xlsx_url,
                csv_content=execution_data["csv_content"],
            )

    @app.get("/public/batch_execution_results/{file_name}")
    async def get_excel_file(file_name: str) -> FileResponse:
        """
        Handle GET requests to download the Excel file.

        Args:
            file_name (str): The name of the Excel file to download.

        Returns:
            FileResponse: The Excel file for download.

        Raises:
            HTTPException: If the file is not found.
        """
        file_path = os.path.join(RESULTS_DIR, file_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=file_name,
        )
