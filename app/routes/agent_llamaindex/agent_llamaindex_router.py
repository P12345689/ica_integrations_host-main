# -*- coding: utf-8 -*-
"""
Author: Chris Hay, Mihai Criveti
Description: Streaming and non-streaming API for Llama-Index agents with tool selection 
and dynamic model configuration.

This module provides a FastAPI application with routes for invoking a LangChain agent 
in streaming and non-streaming modes. The agent can use various tools to process 
queries and generate responses. The API accepts a list of tool names and allows 
for dynamic model and template configuration.

TODO:
- tags (prompt, assistants, collection)
- custom JSON to pass to tools in the format: { "tool_name": "custom_json" }
- add system time to agents as a configurable option
- prettify JSON or code in the action Input.
"""
import logging
import os
from typing import Any, Dict, Generator, List, Union
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from llama_index.core import PromptTemplate
from starlette.responses import JSONResponse, StreamingResponse
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import ChatMessage

# central agent stuff
from app.agents.agent_utilities import build_response, clean_message
from app.agents.input_model import get_input_data
from app.agents.agent_context import ContextItem, format_llamaindex_chat_message, parse_context

# llamaindex specific agent stuff
from .llamaindex_tools import get_selected_tools
from .agent_prompt_template import get_prompt_template
from .agent_model import get_model

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# General Tool Execution Configuration
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))
DEFAULT_MAX_EXECUTION_TIME = 500
MAX_CONSECUTIVE_USES = int(os.getenv("MAX_CONSECUTIVE_USES", "8"))
MAX_TOTAL_USES = int(os.getenv("MAX_TOTAL_USES", "50"))

def generate_finalized_response_from_history(query, model, reasoning_history):        
    # Create a prompt from the gathered reasoning history
    history_summary = "\n".join(
        [f"Thought: {r['thought']}, Action: {r['action']}, Observation: {r['observation']}" for r in reasoning_history if r]
    )

    # Final prompt
    final_prompt = f"Based on the following reasoning steps:\n{history_summary}, answer the original question as best as possible: {query}"

    # Setup messages for the chat
    messages = [
        ChatMessage(
            role="system", content="Answer the original question of the user, focus on the best possible answer with available information but do not breakdown the process taken to achieve the answer.  You will receive the agent's thoughts and actions."
        ),
        ChatMessage(role="user", content=final_prompt),
    ]

    # Hit the LLM with the history and get a final response
    return model.chat(messages)

def generate_response_event(
    invocation_id: str,
    event_counter: int,
    reasoning_step: Dict[str, str]
) -> str:
    """Generate a response event JSON."""
    message = f"Thought: {reasoning_step.get('thought', '')}\n" \
              f"Action: {reasoning_step.get('action', '')}\n" \
              f"Observation: {reasoning_step.get('observation', '')}"
    
    # return the response
    return build_response(
        status="success",
        invocation_id=invocation_id,
        event_counter=event_counter,
        is_final_event=False,
        message=message,
        response_type="agent_response",
        title=f"Event {event_counter}",
        generator="agent_llamaindex"
    )


async def stream_agent_response(
    query: str,
    tools: List['FunctionTool'],
    model: Union['ChatOpenAI', 'WatsonxLLM', 'YourLLM'],
    prompt_template: 'PromptTemplate',
    context_items: List[ContextItem],
    max_iterations: int = 20
) -> Generator[str, None, None]:
    """
    Stream agent responses, ensuring final responses are flagged correctly.

    Args:
        query (str): The user query to process.
        tools (List[FunctionTool]): The list of tools for the agent to use.
        model (Union[ChatOpenAI, 'YourLLM', 'WatsonxLLM']): The model for the LLM.
        prompt_template (PromptTemplate): The prompt used to generate an agent.
        context_items (List[ContextItem]): The context information for generation.
        max_iterations (int): Maximum number of iterations allowed for the agent to run.

    Yields:
        Generator[str]: JSON responses from the agent.
    """
    invocation_id = str(uuid4())
    event_counter = 0
    reasoning_history = []  # Store reasoning history for final response

    try:
        # get the formatted context
        formatted_chat_history = format_llamaindex_chat_message(context_items)

        # create the react agent
        agent = ReActAgent.from_tools(tools, llm=model, verbose=True, chat_history=formatted_chat_history)

        # set the system prompt
        agent.update_prompts({"agent_worker:system_prompt": prompt_template})

        # create the task
        task = agent.create_task(input=query, tool_choice=tools)

        # Run the first step
        step_output = agent.run_step(task.task_id)

        # Loop through the steps
        while not step_output.is_last:
            if event_counter >= max_iterations:
                log.warning("Reached max iterations, synthesizing response with available information.")
                break  # Stop running steps and proceed to final response

            # Capture and clean thought, action, and observation
            cleaned_thought = cleaned_action = cleaned_observation = None

            # Extract the reasoning information from task extra_state
            for item in task.extra_state.get("current_reasoning", []):
                if hasattr(item, "thought"):
                    # clean the thought
                    cleaned_thought = clean_message(item.thought,"thought")

                    # Use `build_response` to yield each thought, action, and observation
                    yield build_response(
                        status="success",
                        invocation_id=invocation_id,
                        event_counter=event_counter,
                        is_final_event=False,
                        message=cleaned_thought,
                        response_type="thought",
                        title=f"{cleaned_thought[:100]}...",
                        generator="agent_llamaindex"
                    )

                # action
                if hasattr(item, "action"):
                    # clean the action
                    cleaned_action = clean_message(item.thought,"action")

                    # Use `build_response` to yield each thought, action, and observation
                    yield build_response(
                        status="success",
                        invocation_id=invocation_id,
                        event_counter=event_counter,
                        is_final_event=False,
                        message=cleaned_action,
                        response_type="action",
                        title=f"Event {event_counter}",
                        generator="agent_llamaindex"
                    )

                if hasattr(item, "action_input"):
                    cleaned_observation = item.action_input
                if hasattr(item, "observation"):
                    # get the observation
                    cleaned_observation = clean_message(item.observation,"observation")

                    # Use `build_response` to yield each thought, action, and observation
                    yield build_response(
                        status="success",
                        invocation_id=invocation_id,
                        event_counter=event_counter,
                        is_final_event=False,
                        message=cleaned_observation,
                        response_type="observation",
                        title=f"{cleaned_observation[:100]}...",
                        generator="agent_llamaindex"
                    )

            # Add reasoning to history
            reasoning_history.append({
                "thought": cleaned_thought,
                "action": cleaned_action,
                "observation": cleaned_observation
            })

            # increase the event counter
            event_counter += 1

            # Run the next step
            step_output = agent.run_step(task.task_id)

        # Handle final answer if `step_output.is_last` is True
        if step_output.is_last:
            # Ensure we capture the final thought and observation from task.extra_state
            final_answer = step_output.output
            final_message = f"{final_answer}"

            # final answer
            yield build_response(
                status="success",
                invocation_id=invocation_id,
                event_counter=event_counter,
                is_final_event=True,
                message=final_message,
                response_type="final_answer",
                title="Final Answer",
                generator="agent_llamaindex"
            )
            return  # Stop further processing

        # Handle the max iteration case by asking the LLM to synthesize a final response
        if event_counter >= max_iterations:
            # log the info
            log.info("Max iterations reached, synthesizing final response using LLM.")
            
            # Hit the LLM with the history and get a final response
            final_response = generate_finalized_response_from_history(query, model, reasoning_history)

            # return the response
            yield build_response(
                status="success",
                invocation_id=invocation_id,
                event_counter=event_counter,
                is_final_event=True,
                message=str(final_response),
                response_type="final_answer",
                title="Final Answer",
                generator="agent_llamaindex"
            )

    except ValueError as e:
        # Handle the max iteration error directly without terminating
        if "Reached max iterations" in str(e):
            log.warning("Max iterations reached, providing best available information.")
            
            # Hit the LLM with the history and get a final response
            final_response = generate_finalized_response_from_history(query, model, reasoning_history)

            # return the response
            yield build_response(
                status="success",
                invocation_id=invocation_id,
                event_counter=event_counter,
                is_final_event=True,
                message=str(final_response),
                response_type="final_answer",
                title="Final Answer",
                generator="agent_llamaindex"
            )

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
    tools: List[str],
    model: Union['ChatOpenAI', 'WatsonxLLM'],
    prompt_template: PromptTemplate,
    context_items: List[ContextItem],
) -> Dict[str, Any]:
    """Gets the final response from an agent based on a given query and context."""
    log.info(f"Getting agent response for query: {query}")

    try:
        # get the formatted context
        formatted_chat_history = format_llamaindex_chat_message(context_items)

        # create the react agent
        agent = ReActAgent.from_tools(tools, llm=model, verbose=True, chat_history=formatted_chat_history)

        # set the system prompt
        agent.update_prompts({"agent_worker:system_prompt": prompt_template})

        # create the task
        task = agent.create_task(input=query, tool_choice=tools)

        # Run the agent until completion or max iterations
        reasoning_history = []
        event_counter = 0
        max_iterations = 20
        step_output = agent.run_step(task.task_id)

        # loop through the steps
        while not step_output.is_last and event_counter < max_iterations:
             # Capture and clean thought, action, and observation
            cleaned_thought = cleaned_action = cleaned_observation = None

            # Extract the reasoning information from task extra_state
            for item in task.extra_state.get("current_reasoning", []):
                if hasattr(item, "thought"):
                    # clean the thought
                    cleaned_thought = clean_message(item.thought,"thought")

                # action
                if hasattr(item, "action"):
                    # clean the action
                    cleaned_action = item.action

                if hasattr(item, "action_input"):
                    cleaned_observation = item.action_input

                if hasattr(item, "observation"):
                    # get the observation
                    cleaned_observation = clean_message(item.observation,"observation")

            # Capture reasoning steps
            reasoning_step = {
                "thought": cleaned_thought,
                "action": cleaned_action,
                "observation": cleaned_observation
            }

            # add reasoning
            reasoning_history.append(reasoning_step)

            # increment
            event_counter += 1
            step_output = agent.run_step(task.task_id)
    
        # Handle final answer if `step_output.is_last` is True
        if step_output.is_last:
            # Ensure we capture the final thought and observation from task.extra_state
            final_answer = step_output.output
            final_message = f"{final_answer}"
            invocation_id = str(uuid4())

            # final answer
            return build_response(
                status="success",
                invocation_id=invocation_id,
                event_counter=event_counter,
                is_final_event=True,
                message=final_message,
                response_type="final_answer",
                title="Final Answer",
                generator="agent_llamaindex"
            )

        # Handle the max iteration case by asking the LLM to synthesize a final response
        if event_counter >= max_iterations:
            # log the info
            log.info("Max iterations reached, synthesizing final response using LLM.")
            
            # Hit the LLM with the history and get a final response
            final_response = generate_finalized_response_from_history(query, model, reasoning_history)

            # return the response
            return build_response(
                status="success",
                invocation_id=invocation_id,
                event_counter=event_counter,
                is_final_event=True,
                message=str(final_response),
                response_type="final_answer",
                title="Final Answer",
                generator="agent_llamaindex"
            )

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
    """Add routes for agent invocation and result retrieval."""

    @app.post("/agent_llamaindex/invoke")
    async def agent_llamaindex(request: Request) -> StreamingResponse:
        # log the request received
        log.info("Received request to invoke agent (streaming).")
        
        # get te input data
        input_data = await get_input_data(request)
        
        # get the model
        model = get_model(input_data.llm_override)

        # parse the context
        context_items = parse_context(input_data.context) if input_data.use_context else []

        # get the prompt template
        prompt_template = get_prompt_template(input_data, "agent_prompt.llamaindex")

        # get the selected tools
        selected_tools = get_selected_tools(input_data.tools)
        log.info(f"Selected tools: {', '.join(tool.metadata.name for tool in selected_tools)}")

        # return a streaming response
        return StreamingResponse(
            stream_agent_response(input_data.query, selected_tools, model, prompt_template, context_items),
            media_type="application/json"
        )

    @app.post("/agent_llamaindex/result")
    async def agent_llamaindex_result(request: Request) -> JSONResponse:
        # log the request received
        log.info("Received a request to get the agent's result (non-streaming).")

        # get te input data
        input_data = await get_input_data(request)
        
        # get the model
        model = get_model(input_data.llm_override)

        # get the context
        context_items = parse_context(input_data.context) if input_data.use_context else []

        # set the prompt template
        prompt_template = get_prompt_template(input_data, "agent_prompt.llamaindex")

        # get selected tools
        selected_tools = get_selected_tools(input_data.tools)
        log.info(f"Selected tools: {', '.join(tool.metadata.name for tool in selected_tools)}")

        # return a non streaming response
        response = await get_agent_response(
            query=input_data.query,
            tools=selected_tools,
            model=model,
            prompt_template=prompt_template,
            context_items=context_items,
        )

        # return the response
        log.info(f"Agent response: {response}")
        return JSONResponse(content=str(response))
