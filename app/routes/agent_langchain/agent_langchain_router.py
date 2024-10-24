# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti, Chris Hay
Description: Streaming and non-streaming API for LangChain agents with tool selection and dynamic model configuration and template configuration.

This module provides a FastAPI application with routes for invoking a LangChain agent
both in streaming and non-streaming modes. The agent can use various tools to process
queries and generate responses. The API accepts a list of tool names to use and allows
for dynamic model configuration and dynamic template configuration.

TODO:
- tags (prompt, assistants, collection)

- custom JSON to pass to various tools, in this format:
{ "tool_name": "custom_json" }

TODO: add the system time to the agents... -> as an option... configurable
TODO: pretty up the json or code in the action Input...

"""

import json
import logging
import os
from typing import Any, Dict, Generator, List, Optional, Union
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from libica import ICAClient
from jinja2 import Environment, FileSystemLoader
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms.watsonxllm import WatsonxLLM
from langchain_consultingassistants import ChatConsultingAssistants
from starlette.responses import JSONResponse, StreamingResponse

# central agent stuff
from app.agents.input_model import get_input_data
from app.agents.agent_context import ContextItem, format_context, parse_context
from app.agents.agent_utilities import clean_message, build_response

# langchain specific agent stuff
from .agent_model import DEFAULT_MAX_EXECUTION_TIME, DEFAULT_MAX_THREADS
from .agent_prompt_template import get_prompt_template
from .langchain_tools import TOOL_DESCRIPTIONS, get_selected_tools
from .agent_model import get_model

# Constants
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Load Jinja2 environment
TEMPLATES_DIRECTORY = "app/routes/agent_langchain/templates"
template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))

def _handle_error(error: str) -> str:
    """Custom Error Function"""
    log.error(f"ERROR PARSING: {error}")
    return "Check your output and make sure it conforms! Do not output an action and a final answer at the same time."

async def stream_agent_response(
    query: str,
    tools: List[Tool],
    model: Union[ChatOpenAI, ChatConsultingAssistants, WatsonxLLM],
    prompt_template: PromptTemplate,
    context_items: List[ContextItem],
) -> Generator[str, None, None]:
    """
    Represents the agent response as a stream.

    Attributes:
        query (str): The query of the user to be processed.
        tools (List[Tool]): The list of tools to be used by the agent.
        model (Union[ChatOpenAI, ChatConsultingAssistants, WatsonxLLM]): The LLM model to be used in generation.
        prompt_template (PromptTemplate): The prompt to use in generating an agent.
        context_items (List[ContextItem]): The context to be used in generation.
    """
    log.debug(f"Streaming agent response for query: {query}")
    invocation_id = str(uuid4())
    event_counter = 0
    context_cache = {}

    try:
        # get the context
        formatted_context = format_context(context_items)

        # create the react agent
        agent = create_react_agent(llm=model, tools=tools, prompt=prompt_template, stop_sequence=True)

        # setup the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=_handle_error,
            max_execution_time=DEFAULT_MAX_EXECUTION_TIME,
        )

        async for response in agent_executor.astream({"input": query, "context": formatted_context}):
            log.debug(f"Received response: {response}")

            # Final event
            if isinstance(response, dict) and "output" in response:
                log.info("Returning final event")

                output = response["output"]
                if "Agent stopped due to iteration limit or time limit." in output:
                    client = ICAClient()
                    summary = client.prompt_flow(prompt=f"{str(context_cache)}",
                                                 model_id_or_name="Mistral Large",
                                                 system_prompt='''You will receive the agent's thoughts and actions and
                                                                you must generate a summary. Do not list each step taken.
                                                                Write the summary in a style resembling an output.
                                                                ''')
                    output = output + "\n" + summary

                yield (
                    json.dumps(
                        {
                            "status": "success",
                            "invocation_id": invocation_id,
                            "event_id": event_counter,
                            "is_final_event": True,
                            "response": [
                                {
                                    "message": output,
                                    "properties": {
                                        "response_type": "final_answer",
                                        "title": "Final Answer",
                                        "generator": "agent_langchain",
                                    },
                                    "type": "text",
                                }
                            ],
                        }
                    )
                    + "\n"
                )
            else:
                # Handle intermediate steps
                if "steps" in response:
                    for step in response["steps"]:
                        if step.action.tool == "_Exception":
                            log.debug(f"Ignored step with _Exception tool: {step}")
                            continue
                        tool_description = TOOL_DESCRIPTIONS.get(step.action.tool, f"🔨 {step.action.tool}")
                        original_message = f"I am providing the following input to this tool:\n{step.action.tool_input}\nObservation: {step.observation}"
                        cleaned_message = clean_message(original_message, 'action')
                        yield (
                            json.dumps(
                                {
                                    "status": "success",
                                    "invocation_id": invocation_id,
                                    "event_id": event_counter,
                                    "is_final_event": False,
                                    "response": [
                                        {
                                            "message": cleaned_message,
                                            "properties": {
                                                "response_type": "action",
                                                "title": f"{tool_description}",
                                                "tool": f"{step.action.tool}",
                                                "generator": "agent_langchain",
                                            },
                                            "type": "text",
                                        }
                                    ],
                                }
                            )
                            + "\n"
                        )
                        event_counter += 1
                        context_cache[event_counter] = cleaned_message

                # Thought
                if "messages" in response:
                    thought = " ".join(
                        [message.content for message in response["messages"] if hasattr(message, "content")])
                    if thought == "Check your output and make sure it conforms! Do not output an action and a final answer at the same time.":
                        log.debug("Ignored conform thought.")
                        continue
                    cleaned_thought = clean_message(thought, 'thought')
                    yield (
                        json.dumps(
                            {
                                "status": "success",
                                "invocation_id": invocation_id,
                                "event_id": event_counter,
                                "is_final_event": False,
                                "response": [
                                    {
                                        "message": cleaned_thought,
                                        "properties": {
                                            "response_type": "thought",
                                            "title": f"{cleaned_thought[:100]}...",
                                            "generator": "agent_langchain",
                                        },
                                        "type": "text",
                                    }
                                ],
                            }
                        )
                        + "\n"
                    )
                    
                    # increment the event counter
                    event_counter += 1

                    # add the thought to the context cache
                    context_cache[event_counter] = cleaned_thought
    except Exception as e:
        # log the exception
        log.exception(f"Error during streaming: {str(e)}")

        # return the exception
        yield build_response(
            status="error",
            invocation_id=invocation_id,
            event_counter=event_counter,
            is_final_event=True,
            message=str(e),
            response_type="error",
            title="Error",
            generator="agent_llamaindex"
        )



async def get_agent_response(
    query: str,
    tools: List[Tool],
    model: Union[ChatOpenAI, ChatConsultingAssistants, WatsonxLLM],
    prompt_template: PromptTemplate,
    context_items: List[ContextItem],
) -> Dict[str, Any]:
    """Gets the final response from an agent based on a given query and context."""
    log.info(f"Getting agent response for query: {query}")

    try:
        # format the context
        formatted_context = format_context(context_items)

        # create the react agent
        agent = create_react_agent(model, tools, prompt_template)

        # execture the agent
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=_handle_error,
            max_execution_time=DEFAULT_MAX_EXECUTION_TIME,
        )

        # final response
        final_response = ""

        # chunk it
        async for chunk in agent_executor.astream({"input": query, "context": formatted_context}):
            if isinstance(chunk, dict):
                if "output" in chunk:
                    final_response += chunk["output"]
                elif "intermediate_step" in chunk:
                    # Log intermediate steps if needed
                    log.debug(f"Intermediate step: {chunk['intermediate_step']}")

        # return the final response
        if final_response:
            log.info(f"Agent response: {final_response}")
            return {
                "status": "success",
                "invocationId": str(uuid4()),
                "response": [{"message": final_response, "type": "text"}],
            }
        
        # always return a message, in this case, no final answer
        return {
            "status": "error",
            "invocationId": str(uuid4()),
            "response": [
                {
                    "message": "Agent did not produce a final response",
                    "type": "error",
                }
            ],
        }

    except Exception as e:
        # exception
        log.exception(f"Error during agent execution: {str(e)}")

        # return the error
        return {
            "status": "error",
            "invocationId": str(uuid4()),
            "response": [{"message": str(e), "type": "error"}],
        }


def add_custom_routes(app: FastAPI) -> None:
    """Adds custom routes to the FastAPI application for agent invocation and result retrieval."""

    @app.post("/agent_langchain/invoke")
    async def agent_langchain(request: Request) -> StreamingResponse:
        log.info("Received a request to invoke the agent (streaming).")

        # get the input data
        input_data = await get_input_data(request)

        # get the model
        model = get_model(input_data.llm_override)

        # set the prompt template
        prompt_template = get_prompt_template(input_data, "agent_prompt.langchain")

        # get the context
        context_items = parse_context(input_data.context) if input_data.use_context else []

        # get the selected tools
        selected_tools = get_selected_tools(input_data.tools)
        log.info(f"Selected tools: {', '.join(tool.name for tool in selected_tools)}")

        # get the streaming response
        response = StreamingResponse(
            stream_agent_response(input_data.query, selected_tools, model, prompt_template, context_items),
            media_type="application/json",
        )

        # return the streamed response
        return response

    @app.post("/agent_langchain/result")
    async def agent_langchain_result(request: Request) -> JSONResponse:
        log.info("Received a request to get the agent's result (non-streaming).")

        # get te input data
        input_data = await get_input_data(request)

        # get the model
        model = get_model(input_data.llm_override)

        # set the prompt template
        prompt_template = get_prompt_template(input_data, "agent_prompt.langchain")

        # get the context
        context_items = parse_context(input_data.context) if input_data.use_context else []

        # get selected tools
        selected_tools = get_selected_tools(input_data.tools)
        log.info(f"Selected tools: {', '.join(tool.name for tool in selected_tools)}")

        # get the non streaming response
        response = await get_agent_response(
            query=input_data.query,
            tools=selected_tools,
            model=model,
            prompt_template=prompt_template,
            context_items=context_items,
        )

        # return the non streaming response
        log.info(f"Agent response: {response}")
        return JSONResponse(content=response)
