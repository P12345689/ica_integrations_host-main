# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Creates charts using matplotlib, returning a PNG

This module provides routes for chart generation, including a system route
for generating a PNG from chart data, and an experience route that
uses an LLM to interpret a natural language request and create a chart.
"""

import asyncio
import json
import os
import io
import base64
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from typing import Any, Dict, List
from uuid import uuid4
from pydantic import BaseModel, Field

import matplotlib
import pandas as pd

matplotlib.use("Agg")  # Set the backend to Agg (a non-interactive backend)
import logging

import matplotlib.pyplot as plt
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import ValidationError
from typing import Optional

from .config import (
    LOG_LEVEL,
    DEFAULT_MODEL_PROMPT_PAIRS,
    DEFAULT_MODEL,
    DEFAULT_MAX_THREADS,
    SERVER_NAME,
    MAX_RETRIES,
    PUBLIC_DIR,
    TEMPLATE_DIR,
)

from .models import (
    CSVInputModel,
    ChartInputModel,
    ExperienceInputModel,
    # ResponseMessageModel,
    OutputModel,
)

class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""
    message: Optional[str] = None  # Text message (optional if sending an image)
    type: str = "text"  # Type could be 'text' or 'image'
    image: Optional[str] = None  # Base64-encoded image data (optional)

template_env = Environment(loader=FileSystemLoader("app/routes/chart/templates"))

# Set up logging
log = logging.getLogger(__name__)


def generate_chart(chart_type: str, data: Dict[str, List[Any]], title: str = "",
                    x_label: Optional[str] = "", y_label: Optional[str] = "") -> str:
    """
    Generate a chart using matplotlib and save it as a PNG file.

    Args:
        chart_type (str): The type of chart to generate.
        data (Dict[str, List[Any]]): The data for the chart.
        title (str, optional): The title of the chart.

    Returns:
        str: The URL of the generated PNG file.

    Raises:
        ValueError: If the chart type is not supported or the data is invalid.
    """
    plt.figure(figsize=(10, 6))

    try:
        if chart_type == "bar":
            plt.bar(data["x"], data["y"])
            if x_label:
                plt.xlabel(x_label)
            if y_label:
                plt.ylabel(y_label)
        elif chart_type == "pie":
            plt.pie(data["values"], labels=data["labels"], autopct="%1.1f%%")
        elif chart_type == "line":
            plt.plot(data["x"], data["y"])
            if x_label:
                plt.xlabel(x_label)
            if y_label:
                plt.ylabel(y_label)
        elif chart_type == "scatter":
            plt.scatter(data["x"], data["y"])
            if x_label:
                plt.xlabel(x_label)
            if y_label:
                plt.ylabel(y_label)
        elif chart_type == "histogram":
            plt.hist(data["values"], bins=len(data["values"]))
            if x_label:
                plt.xlabel(x_label)
            plt.ylabel("Frequency")
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        plt.title(title)

        png_file_path = f"public/chart/chart_{uuid4()}.png"
        os.makedirs(os.path.dirname(png_file_path), exist_ok=True)
        plt.savefig(png_file_path)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', transparent=True)
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')

        png_url = f"{SERVER_NAME}/{png_file_path}"
        log.debug(f"Generated chart URL: {png_url}")
        return png_url, img_str
    finally:
        plt.close()  # Ensure the figure is closed


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/chart/generate_chart/invoke")
    async def generate_chart_route(request: Request) -> OutputModel:
        """
        Handle POST requests to generate a chart from provided data.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or chart generation fails.
        """
        log.info("Received request to generate chart")
        invocation_id = str(uuid4())
        log.info("Input data validation in progress")
        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ChartInputModel(**data)
            log.info(f"input_data: {input_data}")
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        log.info("Input data passed")
        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    generate_chart,
                    input_data.chart_type,
                    input_data.data,
                    input_data.title,
                    input_data.x_label,
                    input_data.y_label,
                )
                chart_result = future.result()
                log.info("chart_result output success")
                try:
                    # If chart generation is successful
                    chart_url, img_str = chart_result
                    log.info("chart_url output success")
                except Exception as e:
                    # Handle exception and return error message
                    log.error(f"Error generating chart: {str(e)}")
                    return ResponseMessageModel(message=f"Error generating chart: {str(e)}")
        except ValueError as e:
            log.error(f"Error generating chart: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            log.error(f"Error generating chart: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate chart")

        log.info(f"Generated chart: {chart_url}")
        response_message = [
            ResponseMessageModel(message=f"{chart_url}\n\nChart data:\n\n```\n{input_data.json()}\n```"),
            ResponseMessageModel(message=img_str, type="image")
        ]
        return OutputModel(invocationId=invocation_id, response=[msg.model_dump() for msg in response_message])

    @app.post("/system/chart/generate_csv_chart/invoke")
    async def generate_chart_csv(request: Request) -> OutputModel:
        """
        Handle POST requests to generate a chart from CSV data.

        Args:
            request (Request): The request object containing the input data as CSV.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or chart generation fails.
        """
        log.info("Received request to generate XLSX")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = CSVInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        try:
            df = pd.read_csv(StringIO(input_data.csv_data))
            dfx = df.iloc[:, 0].to_list()
            dfy = df.iloc[:, 1].to_list()
            csv_data = {"x": dfx, "y": dfy}
        except Exception as e:
            log.error(f"Invalid CSV data {str(e)}")

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    generate_chart,
                    input_data.chart_type,
                    csv_data,
                    input_data.title,
                )
                chart_url = future.result()
        except ValueError as e:
            log.error(f"Error generating chart: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            log.error(f"Error generating chart: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate chart")

        log.info(f"Generated chart: {chart_url}")
        response_message = ResponseMessageModel(
            message=f"{chart_url}\n\nChart data:\n\n```\n{input_data.json()}\n```"
        )
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/chart/generate_chart/invoke")
    async def generate_chart_experience(request: Request) -> OutputModel:
        """
        Handle POST requests for the chart generation experience.

        This route uses an LLM to interpret a natural language request for a chart,
        then generates the chart based on the interpretation.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        log.info("Received request for chart generation experience")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ExperienceInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        # Render the prompt using Jinja2
        prompt_template = template_env.get_template("prompt.jinja")
        rendered_prompt = prompt_template.render(query=input_data.query)
        log.debug(f"Rendered prompt: {rendered_prompt}")

        # Call the LLM
        client = ICAClient()

        async def call_prompt_flow():
            """Async wrapper for the LLM call."""
            log.debug("Calling LLM")
            return await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt,
            )

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                chart_data_future = executor.submit(asyncio.run, call_prompt_flow())
                chart_data = chart_data_future.result()
            log.debug(f"Received LLM response: {chart_data}")
        except Exception as e:
            log.error(f"Error calling LLM: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing request")

        # Generate chart from the interpreted data
        try:
            chart_data_dict = json.loads(chart_data)
            chart_input = ChartInputModel(**chart_data_dict)
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                chart_url_future = executor.submit(
                    generate_chart,
                    chart_input.chart_type,
                    chart_input.data,
                    chart_input.title,
                )
                chart_url = chart_url_future.result()
        except json.JSONDecodeError as e:
            log.error(f"Error parsing JSON from LLM response: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing LLM response")
        except ValidationError as e:
            log.error(f"Error validating chart input data: {str(e)}")
            raise HTTPException(status_code=500, detail="Invalid chart data format")
        except ValueError as e:
            log.error(f"Error generating chart: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            log.error(f"Error generating chart: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate chart")
        finally:
            plt.close("all")  # Ensure all figures are closed

        # Render the response
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(
            chart_url=chart_url, chart_data=chart_data
        )
        log.debug(f"Rendered response: {rendered_response}")

        response_message = ResponseMessageModel(message=rendered_response)
        log.info("Chart generation experience request processed successfully")
        return OutputModel(invocationId=invocation_id, response=[response_message])
