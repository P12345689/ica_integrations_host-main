# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Creates XLSX files from CSV data or from a natural language prompt

This module provides routes for XLSX generation, including a system route
for generating an XLSX from CSV data, and an experience route that
uses an LLM to interpret a natural language request and create an XLSX file.
"""

import asyncio
import csv
import json
import logging
import os
from io import StringIO
from typing import Dict
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient

from .config import DEFAULT_MODEL_PROMPT_PAIRS, LOG_LEVEL, MAX_RETRIES, PUBLIC_DIR, SERVER_NAME, TEMPLATE_DIR
from .models import CSVInputModel, ExperienceInputModel, OutputModel, ResponseMessageModel

# Set up logging
logging.basicConfig(level=LOG_LEVEL)
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def clean_csv_data(csv_string: str) -> str:
    """
    Clean and standardize CSV data while preserving newlines within quoted text.

    Args:
        csv_string (str): The input CSV data as a string.

    Returns:
        str: The cleaned and standardized CSV data as a string.
    """
    output = StringIO()
    reader = csv.reader(StringIO(csv_string), skipinitialspace=True)
    writer = csv.writer(output)

    header = next(reader)  # Read the header
    writer.writerow(header)  # Write the header as is

    for row in reader:
        cleaned_row = []
        for cell in row:
            # Strip leading/trailing whitespace but preserve internal newlines
            cleaned_cell = "\n".join([line.strip() for line in cell.splitlines()])
            cleaned_row.append(cleaned_cell)

        writer.writerow(cleaned_row)

    return output.getvalue().strip()


def validate_csv_data(csv_string: str) -> bool:
    """
    Validate the CSV data to ensure it is well-formed.

    Args:
        csv_string (str): The CSV data to validate.

    Returns:
        bool: True if the CSV data is valid, False otherwise.
    """
    try:
        cleaned_csv = clean_csv_data(csv_string)
        pd.read_csv(StringIO(cleaned_csv), skipinitialspace=True)
        return True
    except pd.errors.ParserError as e:
        log.error(f"CSV validation error: {str(e)}")
        return False


def write_csv_to_xlsx_multiple_sheets(csv_data: Dict[str, str], file_path: str) -> None:
    """
    Write multiple CSVs to Excel with multiple sheets.

    Args:
        csv_data (Dict[str, str]): A dictionary where keys are sheet names and values are CSV data strings.
        file_path (str): The target file path for the XLSX file.

    Raises:
        ValueError: If the CSV data for a sheet is invalid.
        Exception: If there's an error writing the XLSX file.
    """
    try:
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            for sheet_name, csv_string in csv_data.items():
                cleaned_csv = clean_csv_data(csv_string)
                if not validate_csv_data(cleaned_csv):
                    raise ValueError(f"Invalid CSV data for sheet: {sheet_name}")
                df = pd.read_csv(StringIO(cleaned_csv), skipinitialspace=True)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            log.debug("XLSX file with multiple sheets generated successfully")
    except Exception as e:
        log.error(f"Error writing CSV to XLSX with multiple sheets: {str(e)}")
        raise


def generate_xlsx(csv_data: Dict[str, str], input_file_name: str = None) -> str:
    """
    Generate an XLSX file from CSV data.

    Args:
        csv_data (Dict[str, str]): A dictionary where keys are sheet names and values are CSV data strings.
        input_file_name (str): Optional file_name for the excel to be generated

    Returns:
        str: The URL of the generated XLSX file.

    Raises:
        ValueError: If there's an error generating the XLSX file.
    """
    try:
        # Use input_file_name if it's provided, otherwise generate a unique file name
        file_name = input_file_name if input_file_name else f"xlsx_{uuid4()}.xlsx"
        file_path = f"{PUBLIC_DIR}/{file_name}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        write_csv_to_xlsx_multiple_sheets(csv_data, file_path)

        file_url = f"{SERVER_NAME}/{file_path}"
        log.debug(f"Generated XLSX URL: {file_url}")
        return file_url
    except Exception as e:
        log.error(f"Error generating XLSX: {str(e)}")
        raise ValueError(f"Failed to generate XLSX: {str(e)}")


async def call_prompt_flow(prompt: str, model: str) -> str:
    """
    Async wrapper for the LLM call.

    Args:
        prompt (str): The prompt to send to the LLM.
        model (str): The name or ID of the LLM model to use.

    Returns:
        str: The response from the LLM.
    """
    log.debug(f"Calling LLM with model: {model}")
    client = ICAClient()
    return await asyncio.to_thread(
        client.prompt_flow,
        model_id_or_name=model,
        prompt=prompt,
    )


def add_custom_routes(app: FastAPI) -> None:
    """
    Add custom routes to the FastAPI app.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """

    @app.post("/system/xlsx_builder/generate_xlsx/invoke")
    async def generate_xlsx_route(request: Request) -> OutputModel:
        """
        Handle POST requests to generate an XLSX file from CSV data.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error processing the request or generating the XLSX file.
        """
        log.info("Received request to generate XLSX")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = CSVInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        for attempt in range(MAX_RETRIES):
            try:
                cleaned_csv_data = {sheet: clean_csv_data(csv) for sheet, csv in input_data.csv_data.items()}
                xlsx_url = await asyncio.to_thread(generate_xlsx, cleaned_csv_data, input_data.file_name)
                log.info(f"Generated XLSX: {xlsx_url}")
                response_message = ResponseMessageModel(message=f"XLSX file generated successfully. You can download it from: {xlsx_url}")
                return OutputModel(invocationId=invocation_id, response=[response_message])
            except ValueError as e:
                log.error(f"Error generating XLSX (attempt {attempt + 1}): {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                log.error(f"Error generating XLSX (attempt {attempt + 1}): {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    raise HTTPException(status_code=500, detail="Failed to generate XLSX")

    @app.post("/experience/xlsx_builder/generate_xlsx/invoke")
    async def generate_xlsx_experience(request: Request) -> OutputModel:
        """
        Handle POST requests for the XLSX generation experience.

        This route uses an LLM to interpret a natural language request for XLSX content,
        then generates the XLSX file based on the interpretation.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error processing the request or generating the XLSX file.
        """
        log.info("Received request for XLSX generation experience")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ExperienceInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        error_message = ""
        for model, prompt_template in DEFAULT_MODEL_PROMPT_PAIRS:
            try:
                prompt_template = template_env.get_template(prompt_template)
                rendered_prompt = prompt_template.render(query=input_data.query, model=model, error_message=error_message)
                log.debug(f"Rendered prompt: {rendered_prompt}")

                xlsx_data = await call_prompt_flow(rendered_prompt, model)
                log.debug(f"Received LLM response: {xlsx_data}")

                xlsx_data_dict = json.loads(xlsx_data)["csv_data"]
                cleaned_xlsx_data_dict = {sheet: clean_csv_data(csv) for sheet, csv in xlsx_data_dict.items()}
                xlsx_url = await asyncio.to_thread(generate_xlsx, cleaned_xlsx_data_dict)

                response_template = template_env.get_template("response.jinja")
                rendered_response = response_template.render(xlsx_url=xlsx_url, xlsx_data=xlsx_data, model=model)
                log.debug(f"Rendered response: {rendered_response}")

                response_message = ResponseMessageModel(message=rendered_response)
                log.info("XLSX generation experience request processed successfully")
                return OutputModel(invocationId=invocation_id, response=[response_message])

            except json.JSONDecodeError as e:
                error_message = f"Error parsing JSON from LLM response: {str(e)}"
                log.error(f"{error_message} (model: {model})")
            except ValueError as e:
                error_message = f"Error generating XLSX: {str(e)}"
                log.error(f"{error_message} (model: {model})")
            except Exception as e:
                error_message = f"Error in XLSX generation process: {str(e)}"
                log.error(f"{error_message} (model: {model})")

        # If all retries and models fail
        raise HTTPException(status_code=500, detail="Failed to generate XLSX after all attempts")


# Main FastAPI app initialization
app = FastAPI()
add_custom_routes(app)
