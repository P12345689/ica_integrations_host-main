# -*- coding: utf-8 -*-
"""
Ollama-like tool for text generation.

This module provides a tool that uses the text generation functionality from the main router.
"""

from typing import Optional

from langchain.agents import tool

# Import the generate function from the main router
from app.routes.ollama_like.ollama_like_router import GenerateInputModel, generate


@tool
def generate_text(
    model: str,
    prompt: str,
    system: Optional[str] = None,
    template: Optional[str] = None,
    context: Optional[str] = None,
    options: Optional[dict] = None,
) -> str:
    """
    Tool for generating text using an Ollama-like interface.

    Args:
        model (str): The model to use for generation.
        prompt (str): The prompt for text generation.
        system (str, optional): Optional system message.
        template (str, optional): Optional template for formatting.
        context (str, optional): Optional context for generation.
        options (dict, optional): Optional generation options.

    Returns:
        str: The generated text.

    Example:
        >>> result = generate_text("llama2", "Tell me a joke about programming.")
        >>> assert isinstance(result, str)
        >>> assert len(result) > 0
    """
    input_data = GenerateInputModel(
        model=model,
        prompt=prompt,
        system=system,
        template=template,
        context=context,
        options=options,
    )
    result = generate(input_data)
    return result.response[0].message
