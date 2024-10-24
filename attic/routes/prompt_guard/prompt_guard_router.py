# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti (Modified)
Description: Prompt Guard integration router.

This module provides routes for evaluating text for potential prompt injections
and jailbreaks using the Prompt Guard model. It includes functionality to split
longer prompts, identify malicious bits, and optionally return responses in JSON format.
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List
from uuid import uuid4

import torch
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field
from torch.nn.functional import softmax
from transformers import AutoModelForSequenceClassification, AutoTokenizer

log = logging.getLogger(__name__)

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_DEVICE = os.getenv("PROMPT_GUARD_DEVICE", "cpu")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/prompt_guard/templates"))

# Set the path to the local model
MODEL_PATH = Path("app/routes/prompt_guard/Prompt-Guard")

# Load model and tokenizer from the local directory
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(DEFAULT_DEVICE)


class PromptGuardInputModel(BaseModel):
    """Model to validate input data for Prompt Guard queries."""

    text: str = Field(..., description="The text to evaluate")
    temperature: float = Field(1.0, description="Temperature for softmax function")
    as_json: bool = Field(False, description="Whether to return the response as JSON")
    include_indirect_injection: bool = Field(
        False,
        description="Whether to include indirect injection score in the evaluation",
    )


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_class_probabilities(text: str, temperature: float = 1.0) -> torch.Tensor:
    """
    Evaluate the model on the given text with temperature-adjusted softmax.

    Args:
        text (str): The input text to classify.
        temperature (float): The temperature for the softmax function.

    Returns:
        torch.Tensor: The probability of each class adjusted by the temperature.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = inputs.to(DEFAULT_DEVICE)
    with torch.no_grad():
        logits = model(**inputs).logits
    scaled_logits = logits / temperature
    probabilities = softmax(scaled_logits, dim=-1)
    return probabilities


def get_jailbreak_score(text: str, temperature: float = 1.0) -> float:
    """
    Evaluate the probability that a given string contains malicious jailbreak or prompt injection.

    Args:
        text (str): The input text to evaluate.
        temperature (float): The temperature for the softmax function.

    Returns:
        float: The probability of the text containing malicious content.
    """
    probabilities = get_class_probabilities(text, temperature)
    return probabilities[0, 2].item()


def get_indirect_injection_score(text: str, temperature: float = 1.0) -> float:
    """
    Evaluate the probability that a given string contains any embedded instructions.

    Args:
        text (str): The input text to evaluate.
        temperature (float): The temperature for the softmax function.

    Returns:
        float: The probability of the text containing embedded instructions.
    """
    probabilities = get_class_probabilities(text, temperature)
    return probabilities[0, 1].item()


def split_text(text: str, max_tokens: int = 512) -> List[str]:
    """
    Split the input text into chunks of maximum token length.

    Args:
        text (str): The input text to split.
        max_tokens (int): The maximum number of tokens per chunk.

    Returns:
        List[str]: A list of text chunks.
    """
    tokens = tokenizer.tokenize(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokenizer.convert_tokens_to_string(tokens[i : i + max_tokens])
        chunks.append(chunk)
    return chunks


def find_malicious_bits(
    text: str,
    temperature: float = 1.0,
    threshold: float = 0.5,
    include_indirect_injection: bool = False,
) -> List[dict]:
    """
    Identify potentially malicious bits in the input text.

    Args:
        text (str): The input text to analyze.
        temperature (float): The temperature for the softmax function.
        threshold (float): The score threshold above which a chunk is considered malicious.
        include_indirect_injection (bool): Whether to include indirect injection score in the evaluation.

    Returns:
        List[dict]: A list of dictionaries containing information about malicious chunks.
    """
    chunks = split_text(text)
    malicious_bits = []
    for i, chunk in enumerate(chunks):
        jailbreak_score = get_jailbreak_score(chunk, temperature)
        indirect_injection_score = (
            get_indirect_injection_score(chunk, temperature) if include_indirect_injection else None
        )
        if jailbreak_score > threshold or (include_indirect_injection and indirect_injection_score > threshold):
            malicious_bit = {
                "chunk_index": i,
                "text": chunk,
                "jailbreak_score": jailbreak_score,
            }
            if include_indirect_injection:
                malicious_bit["indirect_injection_score"] = indirect_injection_score
            malicious_bits.append(malicious_bit)
    return malicious_bits


async def evaluate_text(text: str, temperature: float = 1.0, include_indirect_injection: bool = False) -> dict:
    """
    Evaluate the input text for jailbreak and optionally indirect injection probabilities.

    Args:
        text (str): The input text to evaluate.
        temperature (float): The temperature for the softmax function.
        include_indirect_injection (bool): Whether to include indirect injection score in the evaluation.

    Returns:
        dict: A dictionary containing jailbreak and optionally indirect injection scores, and malicious bits.
    """
    chunks = split_text(text)
    with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
        jailbreak_futures = [executor.submit(get_jailbreak_score, chunk, temperature) for chunk in chunks]
        jailbreak_scores = await asyncio.gather(*[asyncio.to_thread(future.result) for future in jailbreak_futures])

        result = {
            "jailbreak_score": max(jailbreak_scores),
            "malicious_bits": find_malicious_bits(
                text, temperature, include_indirect_injection=include_indirect_injection
            ),
        }

        if include_indirect_injection:
            indirect_futures = [executor.submit(get_indirect_injection_score, chunk, temperature) for chunk in chunks]
            indirect_scores = await asyncio.gather(*[asyncio.to_thread(future.result) for future in indirect_futures])
            result["indirect_injection_score"] = max(indirect_scores)

    return result


def add_custom_routes(app: FastAPI) -> None:
    """
    Add custom routes to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application to add routes to.
    """

    @app.post("/system/prompt_guard/retrievers/evaluate_text/invoke")
    async def evaluate_text_route(request: Request) -> OutputModel:
        """
        Handle POST requests to evaluate text for potential prompt injections and jailbreaks.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or if there's an error during evaluation.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = PromptGuardInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            result = await evaluate_text(
                input_data.text,
                input_data.temperature,
                input_data.include_indirect_injection,
            )

            if input_data.as_json:
                response_template = template_env.get_template("prompt_guard_json_response.jinja")
            else:
                response_template = template_env.get_template("prompt_guard_response.jinja")

            rendered_response = response_template.render(
                result=result,
                include_indirect_injection=input_data.include_indirect_injection,
            )

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error during text evaluation: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
