# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Synthetic Data Generator generates synthetic data based on sample input CSV files
with optional data types JSON
"""

import json
import logging
import os
from io import StringIO
from types import SimpleNamespace
from typing import Any, Dict
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI, Request
from sdv.lite import SingleTablePreset
from sdv.metadata import SingleTableMetadata

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def add_custom_routes(app: FastAPI) -> None:
    """
    Adds custom API routes to a FastAPI application to generate synthetic data based on the provided CSV and metadata.

    Args:
        app (FastAPI): The FastAPI application instance to which the route will be added.
    """

    @app.api_route("/datagenerator/invoke", methods=["POST"])
    async def generate_synthetic_data(request: Request) -> Dict[str, Any]:
        """
        Handles POST requests to generate synthetic data using the provided CSV sample and metadata.

        Args:
            request (Request): The request object containing the payload with 'sample_csv', 'num_rows', and 'data_types'.

        Returns:
            Dict[str, Any]: A dictionary containing the status of the operation, a unique invocation ID, and a response message.
        """
        try:
            body_text = await request.body()
            log.info(f"Received raw request body: {body_text}")

            clean_text = body_text.replace(b"\r\n", b"\n").decode("utf-8")
            # Replace actual newline characters with \n
            formatted_json = clean_text.replace("\n", "\\n")
            clean_text = formatted_json
            log.info(f"Cleaned request text from Windows newlines: {clean_text}")

            data = json.loads(clean_text, strict=False)  # Allow control characters
            log.info(f"Parsed JSON data successfully: {data}")
        except json.JSONDecodeError as e:
            log.error(f"Failed to decode JSON: {str(e)}")
            return debug_message(f"Invalid JSON input. Error: {str(e)}\n\nRaw request: {body_text}")

        parsed_input = SimpleNamespace()
        parsed_input.sample_csv = data.get("sample_csv")
        parsed_input.num_rows = data.get("num_rows")
        parsed_input.data_types = data.get("data_types")

        if not parsed_input.sample_csv or not parsed_input.num_rows:
            log.error("Missing 'sample_csv' or 'num_rows' in data.")
            return debug_message("Missing required fields: 'sample_csv' or 'num_rows'.")

        try:
            real_data = pd.read_csv(StringIO(parsed_input.sample_csv))
            log.info("CSV data loaded successfully into DataFrame.")
        except Exception as e:
            log.error(f"Error loading CSV data: {str(e)}")
            return debug_message(f"Error loading CSV data. Exception: {str(e)}")

        if parsed_input.data_types:
            try:
                metadata_dict = json.loads(parsed_input.data_types)
                log.info("Loaded metadata from JSON data_types.")
            except json.JSONDecodeError:
                data_types_list = [dt.strip() for dt in parsed_input.data_types.split(",")]
                if len(data_types_list) != len(real_data.columns):
                    log.error("Mismatch between the number of columns in CSV and provided data types.")
                    return debug_message("Number of data types does not match the number of columns in the CSV.")
                metadata_dict = {"columns": {column: {"sdtype": sdtype} for column, sdtype in zip(real_data.columns, data_types_list)}}
                log.info(f"Generated metadata dictionary: {json.dumps(metadata_dict)}")
        else:
            metadata = SingleTableMetadata()
            metadata.detect_from_dataframe(real_data)
            metadata_dict = metadata.to_dict()
            log.warning(f"No metadata, detecting... found: {metadata_dict}")
            # return fit(real_data)

        metadata = SingleTableMetadata()
        try:
            metadata_obj = metadata.load_from_dict(metadata_dict)
            log.info("Metadata loaded from dictionary successfully.")
        except Exception as e:
            log.error(f"Error loading metadata from dictionary: {str(e)}")
            return debug_message(f"Error loading metadata from dictionary. Exception: {str(e)}")

        synthesizer = SingleTablePreset(metadata=metadata_obj, name="FAST_ML")
        synthesizer.fit(data=real_data)
        log.info("Data synthesizer fitted successfully.")

        synthetic_data = synthesizer.sample(num_rows=int(parsed_input.num_rows))
        log.info("Synthetic data generated successfully.")

        data_dir = "public/data"
        os.makedirs(data_dir, exist_ok=True)
        unique_filename = f"data_{uuid4()}.csv"
        full_path = os.path.join(data_dir, unique_filename)
        synthetic_data.to_csv(full_path, index=False)
        log.info(f"Synthetic data saved to {full_path}")

        base_url = os.getenv("SERVER_NAME", "https://localhost:8080")
        csv_url = f"{base_url}/public/data/{unique_filename}"
        invocation_id = str(uuid4())
        synthetic_data_str = synthetic_data.head(10).to_string(index=False)

        return {
            "status": "success",
            "invocationId": invocation_id,
            "response": [
                {
                    "message": f"**Generated {parsed_input.num_rows} rows of synthetic data**:\n {csv_url}\n\nDisplaying first 10 rows:\n\n```\n{synthetic_data_str}```\n",
                    "type": "text",
                }
            ],
        }


def fit(real_data) -> Dict[str, Any]:
    """
    Placeholder function for situations where no data types are provided.

    Returns:
        Dict[str, Any]: A dictionary indicating a default process has been executed.
    """
    metadata = SingleTableMetadata()

    metadata.detect_from_dataframe(real_data)
    detected = metadata.to_dict()
    print(real_data, detected)
    log.info("No data types provided, executed fit function as default.")
    return {
        "status": "success",
        "message": "Executed default fit function due to lack of data types input.",
    }


def debug_message(message: str) -> Dict[str, Any]:
    """
    Returns a dictionary with a formatted message for displaying error information on the client UI.

    Args:
        message (str): The error message to be displayed.

    Returns:
        Dict[str, Any]: A dictionary containing the error message.
    """
    log.info(f"Returning error message to client: {message}")
    return {
        "status": "error",
        "response": [
            {
                "message": f"Error: {message}",
                "type": "text",
            }
        ],
    }
