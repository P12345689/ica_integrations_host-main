# -*- coding: utf-8 -*-
from typing import List, Optional, Union

from pydantic import UUID4, BaseModel, Field, conint, constr, validator


class MessageObject(BaseModel):
    agent_name: str = Field(..., description="Name of the agent providing the response.")
    thought: Optional[constr(min_length=1, max_length=1000)] = Field(None, description="Agent's thought process or reasoning.")
    action: Optional[constr(min_length=1, max_length=255)] = Field(None, description="Action taken by the agent.")
    tool_input: Optional[constr(min_length=1, max_length=1000)] = Field(None, description="Input provided to the tool by the agent.")
    log: Optional[constr(min_length=1, max_length=2000)] = Field(None, description="Log of the actions taken and observations made.")
    observation: Optional[constr(min_length=1, max_length=2000)] = Field(None, description="Observations made by the agent after performing the action.")
    type: str = Field(
        ...,
        description="The type of message.",
        enum=["text", "image", "url", "code", "html"],
    )


class ResponseItem(BaseModel):
    message: Union[MessageObject, constr(min_length=1)] = Field(
        ...,
        description="The message object containing details of the response or message content for non-streaming responses.",
    )
    type: str = Field(
        ...,
        description="The type of message.",
        enum=["text", "image", "url", "code", "html"],
    )


class ResponseSchema(BaseModel):
    status: str = Field(
        ...,
        description="The status of the response. Should always be 'success' or 'error'.",
        enum=["success", "error"],
    )
    invocation_id: UUID4 = Field(..., description="A unique identifier for the invocation, formatted as a UUID.")
    event_id: Optional[conint(ge=0)] = Field(
        None,
        description="The event ID, should be a non-negative integer, starting from 0. Required for streaming responses.",
    )
    is_final_event: Optional[bool] = Field(
        None,
        description="Indicates whether this is the final event in the sequence. Required for streaming responses.",
    )
    response: List[ResponseItem] = Field(..., description="A list of response objects containing message and type.")

    @validator("event_id", "is_final_event", pre=True, always=True)
    def check_event_fields(cls, v, values, field):
        if values["status"] == "success" and ("invocation_id" in values):
            if field.name in ["event_id", "is_final_event"] and v is None:
                raise ValueError(f"{field.name} is required for streaming responses.")
        return v

    class Config:
        schema_extra = {
            "example": [
                {
                    "status": "success",
                    "invocation_id": "0fb142c2-d1da-43f7-84ad-cbd31890a1fc",
                    "event_id": 0,
                    "is_final_event": False,
                    "response": [
                        {
                            "message": {
                                "agent_name": "agent_langchain",
                                "thought": "Jerry Cuomo is a public figure, so information about him should be available online. I will first need to look up information about him and his skills before I can create a diagram.",
                                "action": "Google Search",
                                "tool_input": "Jerry Cuomo biography",
                                "log": "Jerry Cuomo is a public figure, so information about him should be available online. I will first need to look up information about him and his skills before I can create a diagram.",
                                "observation": 'Jerry Cuomo ... Gennaro "Jerry" Cuomo (born 1962) is an American software engineer who has worked for IBM since 1987. Holding the title of IBM Fellow, Cuomo is...',
                            },
                            "type": "text",
                        }
                    ],
                },
                {
                    "status": "success",
                    "invocation_id": "2d317d1f-5807-4d00-ace8-0a441c6815c9",
                    "response": [
                        {
                            "message": 'Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library. Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language and first released it in 1991 as Python 0.9.0. Python 2.0 was released in 2000. Python 3.0, released in 2008, was a major revision not completely backward-compatible with earlier versions. Python 2.7.18, released in 2020, was the last release of Python 2. Python consistently ranks as one of the most popular programming languages, and has gained widespread use in the machine learning community.',
                            "type": "text",
                        },
                        {
                            "message": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/500px-Python-logo-notext.svg.png",
                            "type": "image",
                        },
                    ],
                },
            ]
        }
