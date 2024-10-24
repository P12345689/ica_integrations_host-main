# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti, Santhana Krishnan, Thomas Chang, Kasra Amirtahmasebi
Description: Autogen Integration

Fastapi integration for code splitting using autogen
API key in config/DEMYSTIFIERTEAM_LLM_CONFIG
"""

import os
import logging
import time
from uuid import uuid4
from pydantic import BaseModel,Field
from typing import Union, Any, Dict, List, Optional
from fastapi import FastAPI
from app.routes.icaat_demystifierteam.icaat_agents.DemystifierTeam import DemystifierTeam
import app.routes.icaat_demystifierteam.utilities.RouteController as RouteController
from starlette.responses import JSONResponse
from copy import deepcopy

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


AGENT_NAME = "DymystifierTeam"

class AgentConfig(BaseModel):
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    max_round: Optional[int] = None

class RequestMessage(BaseModel):
    query: str
    agent_config: Optional[AgentConfig] = None
    autogen_config: Optional[Dict] = Field(description="The crewAI flow definition as JSON", default=None)

class DemystifyResponseMessage(BaseModel):
    user_prompt: str
    agent_response: List[Dict[str, Any]]
    conversation_history: Optional[List[Dict[str, Any]]] = None

class Error(BaseModel):
    error_code: int
    message: str

class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"

class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: list[ResponseMessageModel] = Field(min_items=1)

def get_random_seed():
    return str(round(time.time()))


def get_dymystifierteam_config():
    dymystifier_config_list = [
        {
            'model': os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "scribeflowgpt4o"),
            'api_key': os.getenv("AZURE_OPENAI_API_KEY", ""),
            'base_url': os.getenv("AZURE_OPENAI_ENDPOINT", "https://essentials-openai-poc-emea.openai.azure.com"),
            'api_type': 'azure',
            'api_version': os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            'cache_seed': get_random_seed()
        }
    ]
    print(f"Santhana dymystifier_config_list: {dymystifier_config_list}")
    
    docReviewer_config_list = [
        {
            'model': os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "scribeflowgpt4o"),
            'api_key': os.getenv("AZURE_OPENAI_API_KEY", ""),
            'base_url': os.getenv("AZURE_OPENAI_ENDPOINT", "https://essentials-openai-poc-emea.openai.azure.com"),
            'api_type': 'azure',
            'api_version': os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            'cache_seed': get_random_seed()
        }
    ]
    
    docOptimizer_config_list = [
        {
            'model': os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "scribeflowgpt4o"),
            'api_key': os.getenv("AZURE_OPENAI_API_KEY", ""),
            'base_url': os.getenv("AZURE_OPENAI_ENDPOINT", "https://essentials-openai-poc-emea.openai.azure.com"),
            'api_type': 'azure',
            'api_version': os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            'cache_seed': get_random_seed()
        }
    ]
    return dymystifier_config_list,docReviewer_config_list,docOptimizer_config_list


def add_custom_routes(app: FastAPI) -> None:
    @app.api_route("/experience/demystifier/invoke", methods=["POST"])
    @RouteController.validateAgentIsEnabled(agent_name=AGENT_NAME)
    async def post_ibmaas_demystifier(body: RequestMessage,) -> Union[DemystifyResponseMessage, Error]:        
        try:
            dymystifier_config_list,docReviewer_config_list,docOptimizer_config_list=get_dymystifierteam_config()
            result = DemystifierTeam().execute(
                config_list=dymystifier_config_list,
                user_prompt=body.query,
                demystifier_config_list=dymystifier_config_list,
                docreviewer_config_list=docReviewer_config_list,
                docoptimizer_config_list=docOptimizer_config_list,
                demystifier_temperature=body.agent_config.temperature,
                max_tokens=body.agent_config.max_tokens,
                max_round=body.agent_config.max_round,
                system_message=body.autogen_config
            )
        except Exception as e:
            logger.error(f"Error while calling DemystifierTeam  : {e}")
            error=Error(error_code="500", message="Error while executing request. Try after some time.")
            return error
        
        logger.debug(f"Converstation history from agent: {result} , Last conversation from history: {result[-1]}")
        response = DemystifyResponseMessage(
            user_prompt=body.query, agent_response=[result[-1]],conversation_history=result
        )
        return response

    @app.api_route("/experience/demystifier/split/invoke", methods=["POST"])
    @RouteController.validateAgentIsEnabled(agent_name=AGENT_NAME)
    async def post_ibmaas_demystifier(body: RequestMessage,) -> Union[OutputModel, Error]:        
        invocation_id = str(uuid4())
        try:
            dymystifier_config_list,docReviewer_config_list,docOptimizer_config_list=get_dymystifierteam_config()
            result = DemystifierTeam().execute(
                config_list=dymystifier_config_list,
                user_prompt=body.query,
                demystifier_config_list=dymystifier_config_list,
                docreviewer_config_list=docReviewer_config_list,
                docoptimizer_config_list=docOptimizer_config_list,
                demystifier_temperature=body.agent_config.temperature,
                max_tokens=body.agent_config.max_tokens,
                max_round=body.agent_config.max_round,
                system_message=body.autogen_config
            )
        except Exception as e:
            logger.error(f"Error while calling DemystifierTeam  : {e}")
            error=Error(error_code="500", message="Error while executing request. Try after some time.")
            return error
        logger.info(f"Result from agent: {result}")
        last_conversation = '\n'.join(entry['content'] for entry in result if 'content' in entry)
        logger.info(f"last conversation: {last_conversation}")

        logger.info(f"Result from agent for testing: {result[-1]}")
        test_conversation = '\n'.join(entry['content'] for entry in [result[-1]] if 'content' in entry)
        logger.info(f"test conversation: {test_conversation}")
        
        # logger.debug(f"Converstation history from agent: {result} , Last conversation from history: {result[-1]}")
        result_final = [ResponseMessageModel(message=str(f"{last_conversation}\n{test_conversation}"))]
        return OutputModel(invocationId=invocation_id, response=result_final)
    
    @app.api_route("/experience/demystifier/split/json/invoke", methods=["POST"])
    @RouteController.validateAgentIsEnabled(agent_name=AGENT_NAME)
    async def post_ibmaas_demystifier(body: RequestMessage,) -> JSONResponse:        
        invocation_id = str(uuid4())
        try:
            dymystifier_config_list,docReviewer_config_list,docOptimizer_config_list=get_dymystifierteam_config()
            result = DemystifierTeam().execute(
                config_list=dymystifier_config_list,
                user_prompt=body.query,
                demystifier_config_list=dymystifier_config_list,
                docreviewer_config_list=docReviewer_config_list,
                docoptimizer_config_list=docOptimizer_config_list,
                demystifier_temperature=body.agent_config.temperature,
                max_tokens=body.agent_config.max_tokens,
                max_round=body.agent_config.max_round,
                system_message=body.autogen_config
            )
        except Exception as e:
            logger.error(f"Error while calling DemystifierTeam  : {e}")
            error=Error(error_code="500", message="Error while executing request. Try after some time.")
            return error
        logger.info(f"Result from agent: {result}")
        historical_conversation = '\n'.join(entry['content'] for entry in result if 'content' in entry)
        last_conversation = '\n'.join(entry['content'] for entry in [result[-1]] if 'content' in entry)
        
        logger.debug(f"Converstation history from agent: {result} , Last conversation from history: {result[-1]}")
        result_final = {
            "invocationId": invocation_id,
            "response": {
                "result_final": last_conversation,
                "conversation_history": historical_conversation
            },
        }
        return JSONResponse(result_final)
