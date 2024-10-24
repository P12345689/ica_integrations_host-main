# -*- coding: utf-8 -*-
"""
Authors: Adrian Popa
Description: Returns crewAI specofoc tools

CrewAI can use langchain tools but can use it;s own tools. This module will return crewAI tools based on
other tools that are also agents(use own LLM). result_as_answer crewAI specific variable is set to true
"""

import importlib
import json
import logging
import os
from typing import Callable, List, Optional

from app.tools.global_tools.assistant_executor_tool import assistant_executor_tool
from crewai_tools import BaseTool
from langchain.tools import Tool

from app.tools.get_langchain_tools import get_tool_definitions
from app.tools.global_tools.docbuilder_tool import docbuilder_tool_markdown_to_pptx_docx

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssistantExecutorInput:
    assistant_id: str
    prompt: str


class AssistantExecutorToolForCrewAi(BaseTool):
    name: str = "assistant_executor_tool"
    description: str = (
        'Tool for executing an assistant based on the provided assistant ID and prompt. :param input_str: str a string representation of dictionary as JSON containing the following keys \'assistant_id\' (string) and \'prompt\' (string). Example of input_str: "{"assistant_id": "3903", "prompt": "App to open the car trunk using facial recognition"}".'
    )

    def _run(self, assistant_id: str, prompt: str) -> str:
        logger.info(f"Received the following input {assistant_id}  {prompt}")
        input_str = json.dumps({"assistant_id": assistant_id, "prompt": prompt})
        return assistant_executor_tool(input_str)
    
class DocBuilderForCrewAi(BaseTool):
    name: str = "docbuilder_tool_markdown_to_pptx_docx"
    description: str = (
        "Tool for generating PPTX and DOCX documents from markdown. Receives the markdown document as String and generate a pptx and docx"
    )

    def _run(self, md: str) -> str:
        logger.info(f"Received the following input {md} , type: {type(md)}")
        return docbuilder_tool_markdown_to_pptx_docx(md)


def get_tools(
    tool_names: Optional[List[str]] = None, context: Optional[dict] = None
) -> List[Tool]:
    """
    Returns a list of tools. If tool_names is provided, returns only the tools with the specified names.
    Otherwise, returns all tools.

    Args:
        tool_names (Optional[List[str]]): A list of tool names to retrieve.

    Returns:
        List[Tool]: A list of Tool objects.

    Example:
        >>> all_tools = get_tools()
        >>> len(all_tools) > 0
        True
        >>> specific_tools = get_tools(['tool1', 'tool2'])
        >>> all(tool.name in ['tool1', 'tool2'] for tool in specific_tools)
        True
    """
    tools = get_tool_definitions(context)

    if tool_names is None:
        logger.debug("Returning all tools")
    else:
        logger.debug(f"Returning specific tools: {tool_names}")
        tools = [tool for tool in tools if tool.name in tool_names]
    crew_tools = []
    for tool in tools:
        if tool.name == "docbuilder_tool_markdown_to_pptx_docx":
            new_tool = DocBuilderForCrewAi(result_as_answer=True)
            crew_tools.append(new_tool)
        elif tool.name == "assistant_executor_tool":
            new_tool = AssistantExecutorToolForCrewAi(result_as_answer=False)
            crew_tools.append(new_tool)
        else:
            crew_tools.append(tool)
    logger.info("CrewAi Tools {new_tools}")
    return crew_tools
