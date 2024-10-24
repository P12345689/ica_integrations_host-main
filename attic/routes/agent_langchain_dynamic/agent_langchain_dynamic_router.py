# -*- coding: utf-8 -*-
import json
import logging
import os
from typing import Any, Dict, Union

from fastapi import FastAPI, HTTPException, Request
# langchain
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
# ais
from langchain_consultingassistants import ChatConsultingAssistants
from pydantic import BaseModel, Field, ValidationError
from starlette.responses import StreamingResponse

from app.tools.get_langchain_tools import get_tools
from app.tools.prompt_template import get_prompt_template

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Constants
MODEL_TYPE = "OLLAMA"  # "OPENAI"#"CONSULTING_ASSISTANTS" #os.getenv("MODEL_TYPE", "OPENAI")  # CONSULTING_ASSISTANTS with "OpenAI GPT4" or OPENAI
MODEL_NAME = "Gemma2:9b"  # gpt-4"#"Mixtral 8x7b Instruct"#os.getenv("MODEL_NAME", "gpt-4" if MODEL_TYPE == "OPENAI" else "OpenAI GPT4")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_MAX_EXECUTION_TIME = 120

# get the tools
TOOLS_2 = get_tools(["get_system_time"])


class InputModel(BaseModel):
    """Model for incoming request data to specify query."""

    query: str = Field(description="Query to execute against the agent.")


def get_model() -> Union[ChatOpenAI, ChatConsultingAssistants]:
    """Returns the appropriate model based on the MODEL_TYPE environment variable."""
    log.info(f"Initializing model of type {MODEL_TYPE} with name {MODEL_NAME}")
    if MODEL_TYPE == "OPENAI":
        return ChatOpenAI(model=MODEL_NAME)
    if MODEL_TYPE == "OLLAMA":
        return Ollama(model=MODEL_NAME)
    elif MODEL_TYPE == "CONSULTING_ASSISTANTS":
        return ChatConsultingAssistants(model=MODEL_NAME)
    elif MODEL_TYPE == "CONSULTING_ASSISTANTS":
        return ChatConsultingAssistants(model=MODEL_NAME)
    else:
        log.error(f"Invalid MODEL_TYPE: {MODEL_TYPE}")
        raise ValueError(f"Invalid MODEL_TYPE: {MODEL_TYPE}")


def add_custom_routes(app: FastAPI) -> None:
    """Adds custom routes to the FastAPI application for agent invocation and result retrieval."""

    @app.post("/agent_langchain_dynamic/invoke")
    async def agent_langchain_dynamic(request: Request) -> StreamingResponse:
        # log the request
        log.info("Received a request to invoke the agent (streaming).")

        # log the tools
        log.info(f"Configured tools: {', '.join(tool.name for tool in TOOLS_2)}")

        # get the model
        model = get_model()

        try:
            data: Dict[str, Any] = await request.json()
            log.debug(f"Received data: {data}")
            input_data = InputModel(**data)
            log.debug(f"Validated input data: {input_data}")
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            log.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=json.loads(e.json()))

        # get the prompt template
        prompt_template = get_prompt_template()

        try:
            # create the agent and agent_executor
            agent = create_react_agent(model, TOOLS_2, prompt_template)
            agent_executor = AgentExecutor(agent=agent, tools=TOOLS_2, verbose=True, handle_parsing_errors=True)
            log.debug("Agent and executor created successfully.")

            # invoke the agent
            raw_result = agent_executor.invoke({"input": input_data.query})

            # Check if the output is in the raw_result dictionary
            if "output" in raw_result:
                result = raw_result["output"]
                log.info(f"Found result = {result}")
            else:
                result = "I'm sorry but i couldn't find a response, please try with a different query"
                log.warning("No output found in the agent's result.")

        except Exception as e:
            # handle any other unexpected errors
            log.error(f"Error during agent execution: {e}")
            result = "I'm sorry but i couldn't find a response, please try with a different query"

        # return the result
        response = {
            "status": "success",
            "invocationId": "",
            "response": [{"message": result, "type": "text"}],
        }
        log.info(f"Response prepared and being sent: {response}")
        return response


app = FastAPI()
add_custom_routes(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
