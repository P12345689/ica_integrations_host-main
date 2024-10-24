# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Creates charts using Plotly, returning a URL to an interactive HTML or PNG image

This module provides routes for chart generation using Plotly, including a system route
for generating an HTML or PNG from chart data, and an experience route that
uses an LLM to interpret a natural language request and create a chart.
"""

import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List
from uuid import uuid4

import plotly.graph_objects as go
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field, ValidationError

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to INFO in production

# Set default model and max threads from environment variables
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/plotly/templates"))


class ChartInputModel(BaseModel):
    """Model to validate input data for chart generation."""

    chart_type: str = Field(..., description="Type of chart (e.g., 'bar', 'pie', 'line')")
    data: Dict[str, List[Any]] = Field(..., description="Data for the chart")
    title: str = Field(default="", description="Title of the chart")
    format: str = Field(default="PNG", description="Output format: 'PNG' or 'HTML'")


class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""

    query: str = Field(..., description="The input query describing the desired chart")
    format: str = Field(default="PNG", description="Output format: 'PNG' or 'HTML'")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def generate_chart(chart_type: str, data: Dict[str, List[Any]], title: str = "", format: str = "PNG") -> str:
    """
    Generate a chart using Plotly and save it as an HTML file or PNG image.

    Args:
        chart_type (str): The type of chart to generate.
        data (Dict[str, List[Any]]): The data for the chart.
        title (str, optional): The title of the chart.
        format (str, optional): The output format, either "PNG" or "HTML". Defaults to "PNG".

    Returns:
        str: The URL of the generated file.

    Raises:
        ValueError: If the chart type is not supported or the data is invalid.
    """
    if chart_type == "bar":
        fig = go.Figure(data=[go.Bar(x=data["x"], y=data["y"])])
    elif chart_type == "pie":
        fig = go.Figure(data=[go.Pie(labels=data["x"], values=data["y"])])
    elif chart_type == "line":
        fig = go.Figure(data=[go.Scatter(x=data["x"], y=data["y"], mode="lines")])
    elif chart_type == "scatter":
        fig = go.Figure(data=[go.Scatter(x=data["x"], y=data["y"], mode="markers")])
    elif chart_type == "histogram":

        def process_data(data_x: list, data_y: list) -> list:
            """
            Remove duplicates and expand data from data_x based on frequencies from data_y if data_y is not empty.

            Args:
                data_x (list): A list of categories to be displayed.
                data_y (list): A list of frequencies corresponding to each category in data_x.

            Returns:
                list: A list with categories repeated according to their frequencies.

            Example:
                data_x = ["A", "B", "C", "D"]
                data_y = [1, 4, 2, 3]
                expanded = expand_x(data_x, data_y)
                print(expanded)  # Output: ["A", "B", "B", "B", "B", "C", "C", "D", "D", "D"]
            """
            result = []
            # data_y is empty
            if not data_y:
                result = data_x
            else:  # data_x is not empty
                processed_x = list(dict.fromkeys(data_x))  # remove duplicates from data["x"]
                for category, count in zip(processed_x, data_y):
                    result.extend([category] * count)

            return result

        fig = go.Figure(data=[go.Histogram(x=process_data(data["x"], data["y"]))])
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    fig.update_layout(title=title)

    file_name = f"chart_{uuid4()}.{format.lower()}"
    file_path = f"public/plotly/{file_name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if format.upper() == "HTML":
        fig.write_html(file_path, full_html=False, include_plotlyjs="cdn")
    else:  # PNG
        fig.write_image(file_path)

    file_url = f"{SERVER_NAME}/{file_path}"
    log.debug(f"Generated chart URL: {file_url}")
    return file_url


def add_custom_routes(app: FastAPI):
    @app.post("/system/plotly/generate_chart/invoke")
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

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ChartInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    generate_chart,
                    input_data.chart_type,
                    input_data.data,
                    input_data.title,
                    input_data.format,
                )
                chart_url = future.result()
        except ValueError as e:
            log.error(f"Error generating chart: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            log.error(f"Error generating chart: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate chart")

        log.info(f"Generated chart: {chart_url}")
        response_message = ResponseMessageModel(message=f"{chart_url}\n\nChart data:\n\n```\n{input_data.json()}\n```")
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/plotly/generate_chart/invoke")
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
        rendered_prompt = prompt_template.render(query=input_data.query, format=input_data.format)
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
                    input_data.format,
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

        # Render the response
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(chart_url=chart_url, chart_data=chart_data, format=input_data.format)
        log.debug(f"Rendered response: {rendered_response}")

        response_message = ResponseMessageModel(message=rendered_response)
        log.info("Chart generation experience request processed successfully")
        return OutputModel(invocationId=invocation_id, response=[response_message])
