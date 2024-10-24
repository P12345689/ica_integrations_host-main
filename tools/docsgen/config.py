# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
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

from langchain_community.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain_community.llms.watsonxllm import WatsonxLLM
from langchain_consultingassistants import ChatConsultingAssistants
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Setup logging
log = logging.getLogger(__name__)

# Define a type for the model configurations
ModelConfig = Dict[str, str]

# Define default model configurations with explicit type annotation
DEFAULT_MODEL_CONFIGS: Dict[str, ModelConfig] = {
    "OPENAI": {
        "MODEL_NAME": "gpt-4o-mini",
    },
    "AZURE_OPENAI": {
        "MODEL_NAME": "gpt-4o",
        "DEPLOYMENT_NAME": "scribeflowgpt4o",
    },
    "WATSONX": {
        "MODEL_NAME": "mistralai/mistral-large",
    },
    "CONSULTING_ASSISTANTS": {
        "MODEL_NAME": "Consulting Assistants Model",
    },
    "OLLAMA": {"MODEL_NAME": "llama3.1"},
    "NVIDIA_NIM": {"MODEL_NAME": "llama3.1"},
}

# Determine which model to use based on environment variable
MODEL_TYPE = os.getenv("MODEL_TYPE", "AZURE_OPENAI")
MODEL_NAME = os.getenv("MODEL_NAME", DEFAULT_MODEL_CONFIGS[MODEL_TYPE]["MODEL_NAME"])

# Azure OpenAI specific configurations
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://essentials-openai-poc-emea.openai.azure.com")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT_NAME",
    DEFAULT_MODEL_CONFIGS["AZURE_OPENAI"]["DEPLOYMENT_NAME"],
)
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

# WatsonX specific configurations
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", "")
WATSONX_DECODING_METHOD = os.getenv("WATSONX_DECODING_METHOD", "sample")
WATSONX_MAX_NEW_TOKENS = int(os.getenv("WATSONX_MAX_NEW_TOKENS", "4096"))
WATSONX_MIN_NEW_TOKENS = int(os.getenv("WATSONX_MIN_NEW_TOKENS", "1"))
WATSONX_TEMPERATURE = float(os.getenv("WATSONX_TEMPERATURE", "0.1"))
WATSONX_TOP_K = int(os.getenv("WATSONX_TOP_K", "50"))
WATSONX_TOP_P = float(os.getenv("WATSONX_TOP_P", "1.0"))

# OLLAMA
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/v1")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))
# NVIDIA NIM
NVIDIA_NIM_URL = os.getenv("NVIDIA_NIM_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")

# ADD: temperature=0.7, top_p=0.7, max_tokens=1024,

# General Tool Execution Configuration
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))
DEFAULT_MAX_EXECUTION_TIME = 500
MAX_CONSECUTIVE_USES = int(os.getenv("MAX_CONSECUTIVE_USES", "8"))
MAX_TOTAL_USES = int(os.getenv("MAX_TOTAL_USES", "30"))
CLEAN_CONTEXT = os.getenv("CLEAN_CONTEXT", "True").lower() == "true"


def get_model(llm_override: Optional[Tuple[str, str]] = None) -> Union[ChatOpenAI, AzureChatOpenAI, ChatConsultingAssistants, WatsonxLLM]:
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
        if model_host.upper() == "OPENAI":
            return ChatOpenAI(model=model_name)
        if model_host.upper() == "NVIDIA_NIM":
            return ChatNVIDIA(
                model=model_name,
                api_key=NVIDIA_API_KEY,
                temperature=0.6,
                top_p=0.7,
                max_tokens=4096,
            )
        if model_host.upper() == "AZURE_OPENAI":
            return AzureChatOpenAI(
                deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
                model_name=model_name,
                openai_api_version=AZURE_OPENAI_API_VERSION,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_API_KEY,
            )
        elif model_host.upper() == "CONSULTING_ASSISTANTS":
            return ChatConsultingAssistants(model=model_name)
        elif model_host.upper() == "WATSONX":
            return WatsonxLLM(
                model_id=model_name,
                url=WATSONX_URL,
                apikey=WATSONX_API_KEY,
                project_id=WATSONX_PROJECT_ID,
                params={
                    "decoding_method": WATSONX_DECODING_METHOD,
                    "max_new_tokens": WATSONX_MAX_NEW_TOKENS,
                    "min_new_tokens": WATSONX_MIN_NEW_TOKENS,
                    "temperature": WATSONX_TEMPERATURE,
                    "top_k": WATSONX_TOP_K,
                    "top_p": WATSONX_TOP_P,
                },
            )
        elif model_host.upper() == "OLLAMA":
            return ChatOpenAI(model=model_name, base_url=OLLAMA_URL, temperature=OLLAMA_TEMPERATURE)
        else:
            error_msg = f"Invalid model_host in override: {model_host}"
            log.error(error_msg)
            raise ValueError(error_msg)

    # If no override, use the default configuration
    if MODEL_TYPE == "OPENAI":
        log.info(f"Initializing OpenAI model with name {MODEL_NAME}")
        return ChatOpenAI(model=MODEL_NAME)
    if MODEL_TYPE == "AZURE_OPENAI":
        log.info(f"Initializing Azure OpenAI model with name {MODEL_NAME}")
        return AzureChatOpenAI(
            deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
            model_name=MODEL_NAME,
            openai_api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
        )
    elif MODEL_TYPE == "CONSULTING_ASSISTANTS":
        log.info(f"Initializing Consulting Assistants model with name {MODEL_NAME}")
        return ChatConsultingAssistants(model=MODEL_NAME)
    elif MODEL_TYPE == "WATSONX":
        log.info(f"Initializing Watsonx LLM with name {MODEL_NAME}")
        parameters = {
            "decoding_method": WATSONX_DECODING_METHOD,
            "max_new_tokens": WATSONX_MAX_NEW_TOKENS,
            "min_new_tokens": WATSONX_MIN_NEW_TOKENS,
            "temperature": WATSONX_TEMPERATURE,
            "top_k": WATSONX_TOP_K,
            "top_p": WATSONX_TOP_P,
        }
        return WatsonxLLM(
            model_id=MODEL_NAME,
            url=WATSONX_URL,
            apikey=WATSONX_API_KEY,
            project_id=WATSONX_PROJECT_ID,
            params=parameters,
        )
    elif MODEL_TYPE == "OLLAMA":
        return ChatOpenAI(model=MODEL_NAME, base_url=OLLAMA_URL, temperature=OLLAMA_TEMPERATURE)
    else:
        error_msg = f"Invalid MODEL_TYPE: {MODEL_TYPE}"
        log.error(error_msg)
        raise ValueError(error_msg)
