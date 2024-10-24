# -*- coding: utf-8 -*-
"""
Authors: Adrian Popa
Description: Google tool that returns snipet + URL

"""

import json
import logging

import requests
from langchain.tools import Tool
from langchain_core.pydantic_v1 import BaseModel as BaseModel_v1
from langchain_core.pydantic_v1 import create_model

# Set up logging
log = logging.getLogger(__name__)


def create_integration_tool(name: str, definition: dict, description: str, context: dict = None):
    """Creates a LangChain tool from an integration definition.

     This function takes the name, integration definition, and description of a tool
     and returns a LangChain tool object ready for use.  It assumes that the integration
     definition is defined, in the format specified, in `global_tools.json`.

     Args:
         name (str): The name of the tool (e.g., "research_agent").
         definition (dict): A dictionary containing the integration definition. Coresponds to integration_defintion documented below
         description (str): A human-readable description of the tool's functionality. It must contain also a definition of the tool paramters(just string type for parameters is supported at this time)
         context (dict, optional): Additional context to be passed to the tool during execution. Defaults to None.

     Returns:
         LangChainTool: A LangChain tool object representing the defined integration.

      **A configuration JSON entry must be created in  `global_tools.json`: **
      integration_definition will contain a HTTP request definion
      - url - Url of the integration
      - payload - to be send to integration. During the call if a context if provided the context will be substituted in http request body in
      field contex.
      - headers - must contain the http request headers
      - params - An array of input params that the Agent must generate in order to invoke the tool. At present just params of string type are supported. At HTTP invocation the http json body will include paramter name and value as was invoked by agent.
      - description -  A human-readable description of the tool's functionality. It must contain also a definition of the tool parameters. The name of the paramters must match the name given in description.


     ```json
    {
     "name": "research_agent",
     "integration_defintion": {
         "url": "http://localhost:8080/agent_crewai/crewAI",
         "payload": {
             "use_context": "False",
             "context": "{}",
             "stream": "False",
             "llm_override": ["OLLAMA", "llama3.1:8b"],
             "crewai_config": {
                 "agents": [
                     {
                         "type": "Agent",
                         "role": "Researcher",
                         "goal": "Uncover the real meaning of information based on the user intent",
                         "backstory": "You are a Senior Research Analyst. Your expertise lies in identifying significant facts and trends. You have a knack for dissecting complex data and presenting actionable insights.",
                         "verbose": true,
                         "allow_delegation": false,
                         "tools": [
                             "wikipedia_search",
                             "get_website_content",
                             "google_search"
                         ],
                         "max_rpm": 60,
                         "max_iter": 40,
                         "max_execution_time": 4200
                     }
                 ],
                 "tasks": [
                     {
                         "description": "Conduct a comprehensive analysis on {query}. If search collections tools is available use it to identify available collections and  extract the most apropriate document. Use the query document tool to query for facts that are usefull about the task . If an internet search tool is available use it to find up-to-date information and new trends. Identify main facts. Compile your findings in a detailed report. Make sure to check with a human if the draft is good before finalizing your answer.",
                         "expected_output": "A summary document about {query}",
                         "agent": "Researcher"
                     }
                 ]
             }
         },
         "headers": {
             "Content-Type": "application/json",
             "Integrations-API-Key": "dev-only-token"
         },
         "params": [
             "query"
         ]
     },
     "description": "Receives a user query and use different research tools to identify significant facts and trends.  \nArgs:\n query (str): user query"
     }
     ```
    """

    def IntegrationsFunc(*args, **inputs) -> str:
        log.debug("Executing with args {args}")

        url = definition["url"]
        headers = definition["headers"]
        payload = definition["payload"]
        if context:
            payload["context"] = json.dumps(context)
        for index, param in enumerate(definition["params"]):
            payload[param] = args[index]
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            payload = {}
            return result["response"][0]["message"]
        except requests.RequestException as e:
            raise Exception(f"Error calling Integration API: {str(e)}")

    struct = {}
    for param in definition["params"]:
        struct[param] = (str, ...)
    params = create_model("MultipleStringParams", **struct, __base__=BaseModel_v1)

    itool = Tool.from_function(func=IntegrationsFunc, name=name, description=description, args_schema=params)

    return itool
