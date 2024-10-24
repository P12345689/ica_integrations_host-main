# -*- coding: utf-8 -*-
"""
Author: Chris Hay
Description: Configuration module for model initialization and setup

This module provides configurations for initializing various models, including
OpenAI, Azure OpenAI, Watsonx, and Consulting Assistants models.

It sets up logging, defines default model configurations, and retrieves environment-specific settings to
customize model parameters.

The module also includes a function to return the appropriate model instance based on the current configuration
or override parameters.
"""
import logging
import os
from typing import Dict, Optional, Tuple, Union
from llama_index.llms.ollama import Ollama

# Setup logging
log = logging.getLogger(__name__)

# Define a type for the model configurations
ModelConfig = Dict[str, str]

# Define default model configurations with explicit type annotation
DEFAULT_MODEL_CONFIGS: Dict[str, ModelConfig] = {
    "OLLAMA": {"MODEL_NAME": "llama3.1"},
}

# Determine which model to use based on environment variable
MODEL_TYPE = os.getenv("MODEL_TYPE", "OLLAMA")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1:latest")
#MODEL_NAME = os.getenv("MODEL_NAME", DEFAULT_MODEL_CONFIGS[MODEL_TYPE]["MODEL_NAME"])

# OLLAMA
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/v1")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))

def get_model(llm_override: Optional[Tuple[str, str]] = None) -> Union[Ollama]:
    """Returns the appropriate model based on the configuration or override parameters.

    This function selects the model type based on an environment variable or override parameters
    and initializes it with relevant configurations. It logs the initialization details for debugging purposes.

    Args:
        llm_override (Optional[Tuple[str, str]]): A tuple containing (model_host, model_name) to override default settings.

    Raises:
        ValueError: If the specified model type is invalid.

    Returns:
        Union[ChatOpenAI, AzureChatOpenAI, ChatConsultingAssistants, WatsonxLLM]: An instance of the specified model.
    """
    if llm_override:
        model_host, model_name = llm_override
        log.info(f"Using override model: {model_host} - {model_name}")
        if model_host.upper() == "OLLAMA":
            # return the ollama model
            #return Ollama(model=MODEL_NAME, base_url=OLLAMA_URL, temperature=OLLAMA_TEMPERATURE)
            return Ollama(model=MODEL_NAME)
        else:
            error_msg = f"Invalid model_host in override: {model_host}"
            log.error(error_msg)
            raise ValueError(error_msg)

    # If no override, use the default configuration
    if MODEL_TYPE == "OLLAMA":
        # return the ollama model
        #return Ollama(model=MODEL_NAME, base_url=OLLAMA_URL, temperature=OLLAMA_TEMPERATURE)
        return Ollama(model=MODEL_NAME)
    else:
        error_msg = f"Invalid MODEL_TYPE: {MODEL_TYPE}"
        log.error(error_msg)
        raise ValueError(error_msg)
