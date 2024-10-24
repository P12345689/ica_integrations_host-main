# -*- coding: utf-8 -*-

"""
See: # https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/agents/react/agent.py
https://github.com/langchain-ai/langchain/discussions/18726
https://huggingface.co/blog/open-source-llms-as-agents

"""

import logging

from fastapi import FastAPI, Request
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_consultingassistants import ChatConsultingAssistants
from langchain_google_community.search import GoogleSearchAPIWrapper

# Import system tools
from ..docbuilder.tools.generate_docs import generate_docx, generate_pptx
from ..gpt4vision.tools.gpt4vision_tool import ask_image
from ..mermaid.tools.mermaid_tool import syntax_to_image
from ..time.tools.system_time_tool import get_system_time
from ..wikipedia.tools.wikipedia_tool import search_wikipedia_entries

# Logging setup
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Configuration
MODEL_NAME = "OpenAI GPT4"  # Could be any other model e.g., "Granite 13B V2.1", "Llama2 70B Chat"


def add_custom_routes(app: FastAPI):
    @app.post("/qareact/invoke")
    async def qareact(request: Request):
        log.info("Received a request to invoke the QA ReAct agent.")
        # Tool definitions
        search = GoogleSearchAPIWrapper()
        tools = [
            Tool(
                name="Google Search",
                func=search.run,
                description="Useful for searching for information on the internet.",
            ),
            Tool(
                name="Wikipedia Search",
                func=search_wikipedia_entries,
                description="Searches Wikipedia and returns entries matching the query",
            ),
            Tool(
                name="get_system_time",
                func=get_system_time,
                description="Returns the current UTC date and time in the specified format e.g. %Y-%m-%dT%H:%M:%S%Z",
            ),
            Tool(
                name="mermaid_syntax_to_image",
                func=syntax_to_image,
                description="Generates a mermaid diagram image from mermaid syntax passed, returning a url",
            ),
            Tool(
                name="gpt4vision_image_to_text",
                func=ask_image,
                description="This allows you to perform image analysis of the image passed in the image_url, the image url must be the full url including prefix with a query such as describe the image, or what's in the image.",
            ),
            Tool(
                name="generate_pptx",
                func=generate_pptx,
                description="Generates a powerpoint (pptx) from the given markdown and returns a url to the powerpoint",
            ),
            Tool(
                name="generate_docx",
                func=generate_docx,
                description="Generates a word document (docx) from the given markdown and returns a url to the document ",
            ),
        ]
        log.debug(f"Configured tools: {', '.join(tool.name for tool in tools)}")

        # Model setup
        # model = ChatOpenAI(model=MODEL_NAME)
        model = ChatConsultingAssistants(model=MODEL_NAME)
        log.info(f"Using model: {model} with {MODEL_NAME}")

        # Data processing
        data = await request.json()
        query = data["input"]["query"]
        log.info(f"Query received: {query}")

        # Create the agent
        prompt_template = hub.pull("hwchase17/react")
        print("Using prompt_template: {prompt_template}")

        agent = create_react_agent(llm=model, tools=tools, prompt=prompt_template, stop_sequence=True)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        log.info("Agent and executor created successfully.")

        # Agent invocation
        try:
            raw_result = agent_executor.invoke({"input": query})
            log.info("Agent invoked successfully.")

            # Process result
            if "output" in raw_result:
                result = raw_result["output"]
            else:
                result = "No response found, please try a different query."
                log.warning("No output found in the agent's result.")
        except Exception as e:
            log.error("Error during agent execution", exc_info=True)
            result = f"Error processing your request: {str(e)}"

        # Formulate response
        response = {
            "status": "success",
            "invocationId": "",
            "response": [{"message": result, "type": "text"}],
        }
        log.info("Response prepared and being sent.")
        return response
