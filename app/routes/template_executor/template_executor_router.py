# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Template Executor Route

This module provides routes for executing assistants from a Jinja template.
"""
import asyncio
import logging
import os
from typing import List, Dict, Optional, Tuple
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from jinja2 import Environment, FileSystemLoader

# Import the get_model function from models.py
from .models import get_model

# Setup logging
log = logging.getLogger(__name__)

# Set the template directory
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

# Jinja2 environment setup
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Set default model and max threads from environment variables
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Mixtral Large")

class TemplateInput(BaseModel):
    """Model to validate input data for a single template execution."""
    template_name: str = Field(..., description="The name of the template file (without .j2 extension)")
    variables: Dict[str, str] = Field(default_factory=dict, description="Variables to be used in the template")

class TemplateExecutionInput(BaseModel):
    """Model to validate input data for template execution."""
    templates: List[TemplateInput] = Field(..., description="List of templates to execute")
    execution_mode: str = Field(default="parallel", description="Execution mode: 'parallel' or 'series'")
    llm_override: Optional[Tuple[str, str]] = Field(None, description="Optional LLM override (model_host, model_name)")

class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""
    message: str
    type: str = "text"

class OutputModel(BaseModel):
    """Model to structure the output response."""
    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]

async def execute_template(template_input: TemplateInput, model) -> str:
    """
    Execute a single template with the given LLM.
    
    Args:
        template_input (TemplateInput): The template name and its variables.
        model: The language model to use.
    
    Returns:
        str: The result of the template execution.
    """
    try:
        log.info(f"Executing template: {template_input.template_name}")
        template = jinja_env.get_template(f"{template_input.template_name}.j2")
        
        rendered_template = template.render(**template_input.variables)
        log.debug(f"Rendered template: {rendered_template}")
        
        # Use the LLM to process the rendered template
        if hasattr(model, 'predict'):
            result = await asyncio.to_thread(model.predict, rendered_template)
        elif hasattr(model, 'invoke'):
            result = await asyncio.to_thread(model.invoke, rendered_template)
        else:
            raise ValueError("Unsupported model type")
        
        log.info(f"Template {template_input.template_name} executed successfully")
        return result
    except Exception as e:
        log.error(f"Error executing template {template_input.template_name}: {str(e)}")
        raise

async def execute_templates_parallel(templates: List[TemplateInput], model) -> List[str]:
    """Execute templates in parallel."""
    log.info("Executing templates in parallel")
    tasks = [execute_template(template, model) for template in templates]
    return await asyncio.gather(*tasks)

async def execute_templates_series(templates: List[TemplateInput], model) -> List[str]:
    """Execute templates in series."""
    log.info("Executing templates in series")
    results = []
    for template in templates:
        result = await execute_template(template, model)
        results.append(result)
    return results

def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/templates/execute/invoke")
    async def execute_templates(request: Request) -> OutputModel:
        """
        Handle POST requests for executing templates.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or template execution fails.
        """
        log.info("Received request for template execution")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = TemplateExecutionInput(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            # Get the model using the get_model function from models.py
            model = get_model(input_data.llm_override)
            
            log.info(f"Using model: {type(model).__name__}")
            
            # Execute templates based on the execution mode
            if input_data.execution_mode == "parallel":
                results = await execute_templates_parallel(input_data.templates, model)
            elif input_data.execution_mode == "series":
                results = await execute_templates_series(input_data.templates, model)
            else:
                raise ValueError(f"Invalid execution mode: {input_data.execution_mode}")

            # Combine results into a single string
            final_result = "\n".join(results)

        except ValueError as e:
            log.error(f"Error in template execution: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            log.error(f"Unexpected error during template execution: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to execute templates: {str(e)}")

        log.info("Template execution completed successfully")
        response_message = ResponseMessageModel(message=final_result)
        return OutputModel(invocationId=invocation_id, response=[response_message])