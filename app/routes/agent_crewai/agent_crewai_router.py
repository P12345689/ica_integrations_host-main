# -*- coding: utf-8 -*-
"""
Author: Popa Adrian
Description: CrewAI integration for blog building
"""

import asyncio
import json
import logging
import os
import threading
from http.client import HTTPException
from queue import Empty as QueueEmpty
from queue import Queue
from typing import Dict, Optional, Tuple
from uuid import uuid4

from crewai import Agent, Crew, Process, Task
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from langchain_core.agents import AgentAction, AgentStep, AgentFinish
from libica import ICAClient
from pydantic import BaseModel, Field, ValidationError

from app.routes.agent_langchain.agent_model import get_model
from app.tools.get_crewai_tools import get_tools
from app.agents.agent_utilities import TOOL_DESCRIPTIONS, clean_message

# Set up logging
log = logging.getLogger(__name__)
os.environ["OTEL_SDK_DISABLED"] = "true"

from langchain.tools import Tool


class InputModel(BaseModel):
    """Model for incoming request data to specify query, optional context, tools to use, model configuration, and prompt template."""

    query: str = Field(description="Query to execute against the agent.")
    context: Optional[str] = Field(default=None, description="Stringified JSON of context items.")
    use_context: bool = Field(default=False, description="Whether to use the provided context.")
    llm_override: Optional[Tuple[str, str]] = Field(
        default=None,
        description="Tuple of (model_host, model_name) to override default model.",
    )
    stream: bool = Field(default=False, description="Whether to use streaming or not.")
    prompt_id: Optional[str] = Field(
        description="The id of a ICA prompt containing the crewAI flow definition as JSON",
        default=None,
    )
    crewai_config: Optional[Dict] = Field(description="The crewAI flow definition as JSON", default=None)


class MyAgentFinish:
    def __init__(self, crew_results):
        self.crew_results = str(crew_results)


class TaskConfigException(Exception):
    pass


class AgentConfigException(Exception):
    pass


class AgentData(BaseModel):
    type: str = Field("Agent")
    role: str
    goal: str
    backstory: str
    verbose: bool
    allow_delegation: bool
    tools: list[str]
    max_rpm: int
    max_iter: int
    max_execution_time: int


class TaskData(BaseModel):
    description: str
    expected_output: str
    agent: str


class AgentConfig(BaseModel):
    agents: list[dict] = Field(...)
    tasks: list[TaskData] = Field(...)


def add_custom_routes(app: FastAPI) -> None:
    """Add custom routes"""

    @app.api_route("/agent_crewai/crewai", methods=["POST"])
    async def process_crewai(request: Request) -> StreamingResponse:
        try:
            data = await request.json()
            log.debug(f"Received {json.dumps(data)}")
            input_data = InputModel(**data)
            log.debug(f"Validated input data: {input_data}")
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            log.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=json.loads(e.json()))
        query = input_data.query
        invocation_id = str(uuid4())

        # JSON loading and validation
        crew_config = {}
        client = ICAClient()
        if input_data.prompt_id:
            prompts = client.get_prompts()
            for prompt in prompts:
                if prompt["promptId"] == input_data.prompt_id:
                    crew_config = json.loads(prompt)
                    break
        else:
            if input_data.crewai_config:
                crew_config = input_data.crewai_config

        stream = input_data.stream
        if input_data.use_context and input_data.context:
                context_json = json.loads(input_data.context)
                formatted_context = "\n".join([f"{item['type']}: {item['content']}" for item in context_json])
                data["context"] = formatted_context

        log.debug(f"Using the crew definition: {crew_config}")

        queue: Queue = Queue()

        llm = get_model(input_data.llm_override)

        def callback_func_step(agent_name: str):
            def step_callback(step_output):
                if isinstance(step_output, AgentFinish):
                    queue.put(([step_output], agent_name))
                else:
                    for step in step_output:
                        if stream:
                            queue.put((step, agent_name))
                log.debug(f"Queue size: {queue.qsize()}")
            return step_callback
        
        def handle_error(error_message):
            """Puts a MyAgentFinish message with the error into the queue."""
            log.exception("An error occurred")
            queue.put(((MyAgentFinish(error_message),), "CrewAI"))

        def initialize_agents(agent_config, llm):
            agents = []
            for agent_data in agent_config:
                agent_role = agent_data.get("role")  # Use .get() to safely retrieve 'role'
                if not agent_role:
                    raise AgentConfigException("Agent is missing 'role' specification.")

                try:
                    tools_list = agent_data["tools"]
                    log.debug(f"Initializing agent {agent_role} with tool_list {tools_list} context {input_data.context}")
                    tools = get_tools(tools_list, input_data.context)
                    agent_data["tools"] = tools
                    agent = Agent(
                        config=agent_data,
                        llm=llm,
                        step_callback=callback_func_step(agent_role),
                    )  # Create Agent object
                    agents.append(agent)
                except Exception as e:
                    log.exception("An error occurred")
                    raise AgentConfigException(f'Error initializing agent {agent_data["role"]}: {e}')

            return agents

        def initialize_tasks(task_config, agents):
            tasks = []
            for task_data in task_config:
                # Find the agent by role
                assigned_agent = next((a for a in agents if a.role == task_data.agent), None)
                if assigned_agent is None:
                    raise TaskConfigException(f"Missing 'agent' role {task_data.agent} specification in task configuration.")

                task = Task(
                    description=task_data.description,
                    expected_output=task_data.expected_output,
                    agent=assigned_agent,
                    human_input=False,
                )

                tasks.append(task)
            return tasks

        def run_crew(task, crew_config_json):
            # Configuring crew

            # Loading config
            try:
                crew_config = AgentConfig(**crew_config_json)
            except TypeError as e:
                handle_error(f"Invalid crew configuration: {e}")
                return

            # Loading Agents
            agents = []
            try:
                agents = initialize_agents(crew_config.agents, llm)
            except AgentConfigException as e:
                handle_error(f"Agent configuration initialization error: {e}")
                return

            # Loading tasks
            tasks = []
            try:
                tasks = initialize_tasks(crew_config.tasks, agents)
            except TaskConfigException as e:
                handle_error(f"Task configuration intialization error: {e}")
                return
            
            try:
                crew = Crew(agents=agents, tasks=tasks, process=Process.sequential)
                # Execute crew
                result = crew.kickoff(inputs=data)
                queue.put(((MyAgentFinish(result),), "CrewAI"))
            except Exception as e:
                handle_error(f"Crew execution error: {e}")
                return

        async def stream_log_events():
            log.debug("Streaming events")
            event_id = 0
            while True:
                try:
                    message, agent_name = queue.get(timeout=1)
                    queue.task_done()
                    action = message[0]
                    log.debug(f"Received action: {action}")
                    if isinstance(action, MyAgentFinish):
                        messages = action.crew_results
                        log.debug(f"Agent Finish {messages}")
                        event_id += 1
                        answer_event = {
                            "status": "success",
                            "event_id": event_id,
                            "invocation_id": invocation_id,
                            "is_final_event": True,
                            "response": [
                                {
                                    "message": f"{messages}",
                                    "type": "text",
                                    "properties": {"response_type": "final_answer", "title": "Final Answer", "generator": "agent_crewai"}
                                }
                            ],
                        }
                        yield json.dumps(answer_event) + "\n"
                        break
                    if isinstance(action, AgentFinish):
                        log.debug(f"Log: {action.log}, \n Return Values: {action.return_values} \n messages: {action.messages}")
                        # answer_event = {
                        #             "status": "success",
                        #             "event_id": event_id,
                        #             "invocation_id": invocation_id,
                        #             "is_final_event": False,
                        #             "response": [
                        #                 {
                        #                     "message": action.return_values,
                        #                     "properties": {
                        #                         "response_type": "action",
                        #                         "title": f"{tool_description}",
                        #                         "generator": f"agent_crewai.{agent_name}"
                        #                     },
                        #                     "type": "text",
                        #                 }
                        #             ],
                        #         }
                        # yield json.dumps(answer_event) + "\n"
                    if isinstance(action, AgentAction) and action.tool != "_Exception":
                        log.debug(f"Agent Action {action}")
                        event_id += 1
                        tool_description = TOOL_DESCRIPTIONS.get(action.tool, f"{action.tool}")
                        original_message = f"Action: {action.tool}\nInput: {action.tool_input}"
                        cleaned_message = clean_message(original_message, 'action')
                        answer_event = {
                            "status": "success",
                            "event_id": event_id,
                            "invocation_id": invocation_id,
                            "is_final_event": False,
                            "response": [
                                {
                                    "message": cleaned_message,
                                    "properties": {
                                        "response_type": "action",
                                        "title": f"{tool_description}",
                                        "tool": f"{action.tool}",
                                        "generator": f"agent_crewai.{agent_name}",
                                    },
                                    "type": "text",
                                }
                            ],
                        }
                        if len(message) == 2:
                            observation = message[1]
                            if observation:
                                tool_description = TOOL_DESCRIPTIONS.get(action.tool, f"{action.tool}")
                                original_message = f"I am providing the following input to this tool:\n{action.tool_input}\nObservation: {observation}"
                                cleaned_message = clean_message(original_message, 'action')
                                answer_event = {
                                    "status": "success",
                                    "event_id": event_id,
                                    "invocation_id": invocation_id,
                                    "is_final_event": False,
                                    "response": [
                                        {
                                            "message": cleaned_message,
                                            "properties": {
                                                "response_type": "action",
                                                "title": f"{tool_description}",
                                                "tool": f"{action.tool}",
                                                "generator": f"agent_crewai.{agent_name}",
                                            },
                                            "type": "text",
                                        }
                                    ],
                                }
                        yield json.dumps(answer_event) + "\n"
                    if isinstance(action, AgentStep):
                        log.debug(f"Agent step {action}")
                    await asyncio.sleep(0.1)
                except QueueEmpty:
                    await asyncio.sleep(0.1)

        log.debug("Before executing CrewAI.")
        thread = threading.Thread(
            target=run_crew,
            args=(query, crew_config),
        )
        thread.start()
        if stream:
            return StreamingResponse(stream_log_events(), media_type="application/x-ndjson")
        else:
            thread.join()
            message, agent_name = queue.get(timeout=1)
            queue.task_done()
            action = message[0]
            log.debug(f"Received result: {action}")
            if isinstance(action, MyAgentFinish):
                messages = action.crew_results
                log.debug(f"Agent Finish {messages}")
                answer = {
                    "status": "success",
                    "invocationId": str(uuid4()),
                    "response": [
                        {
                            "message": f"{messages}",
                            "type": "text",
                        }
                    ],
                }
                return answer
            else:
                raise HTTPException(status_code=500, detail="Error calling Crew")
