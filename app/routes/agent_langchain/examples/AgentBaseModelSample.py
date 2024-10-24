# -*- coding: utf-8 -*-
from typing import Field, List, Optional, Union

from pydantic import BaseModel


class AgentMessage(BaseModel):
    agent_name: str  # Name of the agent, ex: agent_langchain
    thought: Optional[str]  # Think / plan what you're going to do. Reason about the next action to take.
    action: Optional[str]  # What action to perform (ex: call a tool or another agent). Decide on tan action to take.
    tool_input: Optional[str]  # JSON input used as input to the tool.
    observation: Optional[str]  # This is the result of the tool. Observation on the action that was executed.
    log: Optional[str]  # Previous steps


class ResponseItem(BaseModel):
    message: Union[str, AgentMessage]
    type: str


class StreamingOutput(BaseModel):
    status: str = Field(default="success")
    invocation_id: str
    event_id: int
    is_final_event: bool
    response: List[ResponseItem]
