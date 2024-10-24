# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Prompt defender with multi-model support
"""

import asyncio
import json
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Union
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from langchain.schema import HumanMessage
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import WatsonxLLM
from langchain_consultingassistants import ChatConsultingAssistants
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Constants
MODEL_TYPE = os.getenv("MODEL_TYPE", "CONSULTING_ASSISTANTS")  # OPENAI WATSONX CONSULTING_ASSISTANTS
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4" if MODEL_TYPE == "OPENAI" else "Mixtral 8x7b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_MAX_EXECUTION_TIME = 120
CLEAN_CONTEXT = os.getenv("CLEAN_CONTEXT", "True").lower() == "true"
MAX_INPUT_LENGTH = 1000  # Maximum length of user input query

# WatsonX Configuration
WATSONX_MODEL_ID = os.getenv("WATSONX_MODEL_ID", "mistralai/mistral-large")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", "")
WATSONX_DECODING_METHOD = os.getenv("WATSONX_DECODING_METHOD", "sample")
WATSONX_MAX_NEW_TOKENS = int(os.getenv("WATSONX_MAX_NEW_TOKENS", 8000))
WATSONX_MIN_NEW_TOKENS = int(os.getenv("WATSONX_MIN_NEW_TOKENS", 1))
WATSONX_TEMPERATURE = float(os.getenv("WATSONX_TEMPERATURE", 0.1))
WATSONX_TOP_K = int(os.getenv("WATSONX_TOP_K", 50))
WATSONX_TOP_P = float(os.getenv("WATSONX_TOP_P", 1.0))

# File paths
RULES_DIR = "app/routes/prompt_defender/rules"
TEMPLATES_DIR = "app/routes/prompt_defender/templates"
CONFIG_FILE = "app/routes/prompt_defender/config.json"

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


class DetectionMethod(BaseModel):
    enabled: bool = True
    threshold: float = 0.5  # For LLM method


class PromptDefenderConfig(BaseModel):
    """Configuration model for Prompt Defender."""

    basic: DetectionMethod = DetectionMethod()
    advanced: DetectionMethod = DetectionMethod()
    llm: DetectionMethod = DetectionMethod(threshold=0.7)
    custom_regexes: List[str] = Field(default=[], description="List of custom regex patterns")
    max_retries: int = Field(default=3, description="Maximum number of retries for LLM analysis")


class PromptDefenderInputModel(BaseModel):
    """Model to validate input data for Prompt Defender."""

    prompt: str = Field(..., description="The prompt to be analyzed", max_length=MAX_INPUT_LENGTH)
    config: Optional[PromptDefenderConfig] = Field(None, description="Custom configuration for this request")
    languages: Union[str, List[str]] = Field(
        "all",
        description="Languages to check against. Can be 'all' or a list of language codes.",
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


def get_model() -> Union[ChatOpenAI, ChatConsultingAssistants, WatsonxLLM]:
    """Returns the appropriate model based on the MODEL_TYPE environment variable."""
    log.info(f"Initializing model of type {MODEL_TYPE} with name {MODEL_NAME}")
    if MODEL_TYPE == "OPENAI":
        return ChatOpenAI(model_name=MODEL_NAME)
    elif MODEL_TYPE == "CONSULTING_ASSISTANTS":
        return ChatConsultingAssistants(model=MODEL_NAME)
    elif MODEL_TYPE == "WATSONX":
        parameters = {
            "decoding_method": WATSONX_DECODING_METHOD,
            "max_new_tokens": WATSONX_MAX_NEW_TOKENS,
            "min_new_tokens": WATSONX_MIN_NEW_TOKENS,
            "temperature": WATSONX_TEMPERATURE,
            "top_k": WATSONX_TOP_K,
            "top_p": WATSONX_TOP_P,
        }
        return WatsonxLLM(
            model_id=WATSONX_MODEL_ID,
            url=WATSONX_URL,
            apikey=WATSONX_API_KEY,
            project_id=WATSONX_PROJECT_ID,
            params=parameters,
        )
    else:
        log.error(f"Invalid MODEL_TYPE: {MODEL_TYPE}")
        raise ValueError(f"Invalid MODEL_TYPE: {MODEL_TYPE}")


def load_config() -> PromptDefenderConfig:
    """Load configuration from file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return PromptDefenderConfig(**json.load(f))
    except FileNotFoundError:
        log.warning(f"Configuration file not found at {CONFIG_FILE}. Using default configuration.")
        return PromptDefenderConfig()
    except json.JSONDecodeError:
        log.error(f"Invalid JSON in configuration file {CONFIG_FILE}. Using default configuration.")
        return PromptDefenderConfig()


def load_rules(rule_set: str, languages: Union[str, List[str]] = "all") -> List[str]:
    """Load regex patterns from specified rule set and language(s)."""
    try:
        if rule_set == "multi_language":
            with open(os.path.join(RULES_DIR, "multi_language_rules.json"), "r") as f:
                all_rules = json.load(f)
                if languages == "all":
                    # Flatten all language rules into a single list
                    return [rule for lang_rules in all_rules.values() for rule in lang_rules]
                elif isinstance(languages, list):
                    # Return rules for specified languages
                    return [rule for lang in languages for rule in all_rules.get(f"{lang}_rules", [])]
                else:
                    # Return rules for a single specified language
                    return all_rules.get(f"{languages}_rules", [])
        else:
            with open(os.path.join(RULES_DIR, f"{rule_set}.json"), "r") as f:
                rule_data = json.load(f)
                return rule_data.get("rules", [])
    except FileNotFoundError:
        log.warning(f"Rule set file not found in {RULES_DIR}.")
    except json.JSONDecodeError:
        log.error("Invalid JSON in rule set file.")
    return []


def regex_check(prompt: str, patterns: List[str]) -> bool:
    """
    Check if the prompt matches any of the given regex patterns.
    This function is case-insensitive and ignores variations in whitespace.
    """
    # Normalize the prompt: convert to lowercase and replace all whitespace with a single space
    normalized_prompt = " ".join(prompt.lower().split())

    for pattern in patterns:
        try:
            # Modify the pattern to be flexible with whitespace
            flexible_pattern = re.sub(r"\s+", r"\\s+", pattern.lower())
            if re.search(flexible_pattern, normalized_prompt, re.IGNORECASE | re.DOTALL):
                log.debug(f"Matched pattern: {pattern}")
                return True
        except re.error:
            log.error(f"Invalid regex pattern: {pattern}")

    log.debug("No patterns matched")
    return False


async def llm_analysis(prompt: str, threshold: float) -> bool:
    """Perform LLM-based analysis to detect potential prompt injection."""
    model = get_model()

    try:
        prompt_template = template_env.get_template("prompt_injection_analysis.jinja")
        analysis_prompt = prompt_template.render(user_prompt=prompt)
    except Exception as e:
        log.error(f"Error rendering analysis prompt template: {str(e)}")
        return False

    try:
        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            response_future = executor.submit(
                asyncio.run,
                asyncio.to_thread(lambda: model.invoke([HumanMessage(content=analysis_prompt)])),
            )
            result = response_future.result()
            response = result if isinstance(result, str) else result.content
    except Exception as e:
        log.error(f"Error calling LLM: {str(e)}")
        return False

    try:
        analysis_result = json.loads(response)
        injection_probability = analysis_result.get("injection_probability", 0)
        return injection_probability > threshold
    except json.JSONDecodeError:
        log.error("Failed to parse LLM response as JSON")
        return False


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/prompt_defender/analyze/invoke")
    async def analyze_prompt(request: Request) -> OutputModel:
        """Handle POST requests to analyze prompts for potential injection."""
        invocation_id = str(uuid4())
        log.info(f"Analyzing prompt with invocation ID: {invocation_id}")

        try:
            data = await request.json()
            input_data = PromptDefenderInputModel(**data)
            languages = data.get("languages", "all")  # Default to all languages if not specified
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        config = input_data.config or load_config()

        results: Dict[str, bool] = {}

        # Perform basic regex check
        if config.basic.enabled:
            basic_rules = load_rules("basic")
            results["basic"] = regex_check(input_data.prompt, basic_rules)

        # Perform advanced regex check
        if config.advanced.enabled:
            advanced_rules = load_rules("advanced")
            results["advanced"] = regex_check(input_data.prompt, advanced_rules)

        # Perform multi-language regex check
        multi_language_rules = load_rules("multi_language", languages)
        results["multi_language"] = regex_check(input_data.prompt, multi_language_rules)
        log.info(f"Multi-language check result: {results['multi_language']} for prompt: {input_data.prompt}")

        # Perform custom regex check
        if config.custom_regexes:
            results["custom"] = regex_check(input_data.prompt, config.custom_regexes)
            log.info(f"Custom check result: {results['custom']} for prompt: {input_data.prompt}")

        # Perform LLM-based analysis
        if config.llm.enabled:
            retry_count = 0
            while retry_count < config.max_retries:
                llm_result = await llm_analysis(input_data.prompt, config.llm.threshold)
                if llm_result:
                    results["llm"] = True
                    break
                retry_count += 1
            if "llm" not in results:
                results["llm"] = False

        # Determine if there's a potential injection
        is_potential_injection = any(results.values())

        try:
            response_template = template_env.get_template("analysis_response.jinja")
            rendered_response = response_template.render(is_potential_injection=is_potential_injection, results=results)
        except Exception as e:
            log.error(f"Error rendering response template: {str(e)}")
            rendered_response = "Error generating analysis response."

        log.info(f"Analysis complete for invocation ID {invocation_id}")

        return OutputModel(
            status="success",
            invocationId=invocation_id,
            response=[ResponseMessageModel(message=rendered_response)],
        )

    @app.post("/system/prompt_defender/update_config/invoke")
    async def update_config(request: Request) -> OutputModel:
        """Handle POST requests to update the Prompt Defender configuration."""
        invocation_id = str(uuid4())
        log.info(f"Updating configuration with invocation ID: {invocation_id}")

        try:
            data = await request.json()
            new_config = PromptDefenderConfig(**data)
        except Exception as e:
            log.error(f"Invalid configuration: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(new_config.dict(), f, indent=2)
            log.info(f"New configuration saved to {CONFIG_FILE}")
        except Exception as e:
            log.error(f"Error saving configuration: {str(e)}")
            raise HTTPException(status_code=500, detail="Error saving configuration")

        return OutputModel(
            status="success",
            invocationId=invocation_id,
            response=[ResponseMessageModel(message="Configuration updated successfully")],
        )
