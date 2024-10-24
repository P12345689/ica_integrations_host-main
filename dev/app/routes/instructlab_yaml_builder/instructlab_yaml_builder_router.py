# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Generate questions for instructlab
"""

import logging
from uuid import uuid4

import yaml
from fastapi import FastAPI
from pydantic import BaseModel

# Setting up logging
log = logging.getLogger(__name__)


# Defining the data model for incoming requests
class SeedExample(BaseModel):
    question_1: str
    answer_1: str
    question_2: str
    answer_2: str
    question_3: str
    answer_3: str
    skill_type: str  # Assuming this is used elsewhere or for logging


def add_custom_routes(app: FastAPI):
    @app.post("/system/instructlab/generate_yaml/invoke")
    async def generate_yaml(example: SeedExample):
        # Logging the type of skill for debugging purposes
        log.debug(f"Received a request with skill_type: {example.skill_type}")

        # Generating YAML content
        yaml_content = {
            "created_by": "IBM Consulting Assistants: InstructLab Builder",
            "task_description": "To teach a language model about word generation",
            "seed_examples": [
                {"question": example.question_1, "answer": example.answer_1},
                {"question": example.question_2, "answer": example.answer_2},
                {"question": example.question_3, "answer": example.answer_3},
            ],
        }

        # Converting dict to YAML string
        yaml_str = yaml.dump(yaml_content, sort_keys=False)

        # Generate a unique invocation ID
        invocation_id = str(uuid4())

        # Preparing the response
        response = {
            "status": "success",
            "invocationId": invocation_id,
            "response": [
                {
                    "message": yaml_str,
                    "type": "text",
                },
            ],
        }

        log.debug(f"Returning response with invocation ID: {invocation_id}")
        return response


app = FastAPI()
add_custom_routes(app)
