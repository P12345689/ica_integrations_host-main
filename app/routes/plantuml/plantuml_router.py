# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Create UML diagrams with PlantUML

The main functionality includes:
- Validating input data using Pydantic models.
- Making asynchronous API calls to generate UML diagrams using PlantUML.
- Handling errors and providing informative responses to the user.
- Using Jinja2 templates for formatting the response.

The module uses FastAPI for handling HTTP requests, Pydantic for input validation and output structuring,
and Jinja2 for templating the responses.

Example usage:
    # Make a POST request to the /plantuml/invoke endpoint with the following JSON payload:
    {
        "description": "@startuml\nAlice -> Bob: Hello\n@enduml"
    }

Prereq:
    podman run -d -p 9994:8080 docker.io/plantuml/plantuml-server:jetty
"""

import logging
import os
import re
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from app.routes.plantuml.plantuml_utility import generate_uml_image

app = FastAPI()
log = logging.getLogger(__name__)

# Load the PlantUML server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/plantuml/templates"))


class UMLRequest(BaseModel):  # """UML request model"""
    description: str  # UML description in PlantUML syntax


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str
    response: list[ResponseMessageModel]
    invocationId: str  # noqa: N815

def clean_description(description: str) -> str:
    """
    Extract the PlantUML diagram description between '@startuml' and '@enduml'.
    If not found, return the original description.
    """
    pattern = r'@startuml\s*(.*?)\s*@enduml'
    match = re.search(pattern, description, re.DOTALL)
    if match:
        return f'@startuml\n{match.group(1).strip()}\n@enduml'
    return description

def add_custom_routes(app: FastAPI):
    """Add custom routes"""

    @app.post("/plantuml/invoke")
    async def plantuml_invoke_orig(request: Request):
        """
        Original route for invoking PlantUML.

        Args:
            request (Request): The incoming request object.

        Returns:
            The response from the `plantuml_invoke` function.
        """
        return await plantuml_invoke(request)
    
    @app.post("/experience/plantuml/transformers/syntax_to_image/invoke")
    async def plantuml_invoke(request: Request):
        data = await request.json()
        uml_request = UMLRequest(**data)
        clean_text = clean_description(uml_request.description)
        try:
            filename = await generate_uml_image(clean_text)
            url = f"{SERVER_NAME}/public/images/{filename}"
            invocation_id = str(uuid4())

            template = template_env.get_template("plantuml_response.jinja")
            formatted_response = template.render(url=url, description=uml_request.description)

            response = [
                ResponseMessageModel(message=url, type="image"),
                ResponseMessageModel(message=formatted_response, type="text"),
            ]
            log.info(f"Formatted response: {formatted_response}")
            log.info(f"Final response: {response}")

            return {
                "status": "success",
                "response": response,
                "invocationId": invocation_id,
            }
        except HTTPException as e:
            log.error(f"Error generating UML diagram: {str(e.detail)}")
            raise e

    @app.post("/system/plantuml/transformers/syntax_to_image/invoke")
    async def plantuml_invoke(request: Request):
        """
        Handles the POST request to generate UML diagrams using PlantUML.

        This function takes the input data from the request, validates it using Pydantic models,
        makes an asynchronous call to the PlantUML server to generate the UML diagram, and returns
        a structured response.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The response model containing the status, response messages, and invocation ID.

        Raises:
            HTTPException: If there is an error processing the request or generating the UML diagram.

        Example:
            >>> import requests
            >>> url = "http://localhost:8080/plantuml/invoke"
            >>> data = {
            ...     "description": "@startuml\\nAlice -> Bob: Hello\\n@enduml"
            ... }
            >>> headers = {"Content-Type": "application/json"}
            >>> response = requests.post(url, json=data, headers=headers)
            >>> response.json()
            {
                "status": "success",
                "response": [
                    {
                        "message": "http://127.0.0.1:8080/public/images/uml_92f8d7a6-f0b5-4e2a-8d2d-1e9b9f4c6e3e.png",
                        "type": "image"
                    },
                    {
                        "message": "```\\n@startuml\\nAlice -> Bob: Hello\\n@enduml\\n```\\n\\n![UML Diagram](http://127.0.0.1:8080/public/images/uml_92f8d7a6-f0b5-4e2a-8d2d-1e9b9f4c6e3e.png)",
                        "type": "text"
                    }
                ],
                "invocationId": "92f8d7a6-f0b5-4e2a-8d2d-1e9b9f4c6e3e"
            }
        """

        # Get the request data
        data = await request.json()

        # Validate input data using Pydantic model
        uml_request = UMLRequest(**data)

        # Clean the description
        clean_text = clean_description(uml_request.description)

        log.debug(f"Cleaned request text from Windows newlines: {clean_text}")

        # Check if a description is provided
        if not clean_text:
            log.error("No UML description provided.")
            raise HTTPException(status_code=400, detail="No description provided")

        try:
            # Generate the image URL
            filename = await generate_uml_image(clean_text)
            url = f"{SERVER_NAME}/public/images/{filename}"
            log.info(f"UML diagram generated successfully at {url}")

            # Create an invocation ID
            invocation_id = str(uuid4())

            # Format the response using a Jinja2 template
            template = template_env.get_template("plantuml_response.jinja")
            formatted_response = template.render(url=url, description=uml_request.description)

            # Create a structured response using Pydantic model
            response = [
                ResponseMessageModel(message=url, type="image"),
                ResponseMessageModel(message=formatted_response, type="text"),
            ]
            log.info(f"Formatted response: {formatted_response}")
            log.info(f"Final response: {response}")

            return {
                "status": "success",
                "response": response,
                "invocationId": invocation_id,
            }
        except HTTPException as e:
            log.error(f"Error generating UML diagram: {str(e.detail)}")
            invocation_id = str(uuid4())
            return {
                "status": "error",
                "response": [ResponseMessageModel(message="Could not generate image", type="text")],
                "invocationId": invocation_id,
            }
