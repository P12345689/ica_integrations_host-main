# -*- coding: utf-8 -*-

import logging

from fastapi import FastAPI, Request
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
# langchain import
from langchain_community.chat_models import ChatOpenAI
from langchain_google_community.search import GoogleSearchAPIWrapper

from app.routes.docbuilder.tools.generate_docs import (generate_docx,
                                                       generate_pptx)
from app.tools.global_tools.gpt4vision_tool import call_gpt4_vision_api
from app.tools.global_tools.mermaid_tool import syntax_to_image
from app.tools.global_tools.system_time_tool import get_system_time
from app.tools.global_tools.wikipedia_tool import search_wikipedia_entries

# Constants
MODEL_NAME = "gpt-4"
from dev.app.routes.website.tools.website_tools import (is_healthy,
                                                        is_website_up)

# Logging setup
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def add_custom_routes(app: FastAPI):
    @app.post("/qareact/invoke")
    async def qareact(request: Request):
        log.info("\n******** Received a request to invoke the QA ReAct agent. *******\n")

        # search
        search = GoogleSearchAPIWrapper()

        # Tool definitions
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
                name="syntax_to_image",
                func=syntax_to_image,
                description="Generates a mermaid diagram image from mermaid syntax passed, returning a url",
            ),
            Tool(
                name="gpt4vision_image_to_text",
                func=call_gpt4_vision_api,
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
            Tool(
                name="is_website_healthy",
                func=is_healthy,
                description="checks the health given health endpoint url, to see if it's healthy",
            ),
            Tool(
                name="is_website_up",
                func=is_website_up,
                description="checks if a website with the given url is up",
            ),
        ]

        log.info(f"Configured tools: {', '.join(tool.name for tool in tools)}")

        # tools = [get_system_time]

        # get the model
        # model = ChatConsultingAssistants(model="OpenAI GPT 3.5 API")
        # model = ChatConsultingAssistants(model="Granite 13B V2.1")
        # model = ChatConsultingAssistants(model="Llama2 70B Chat")
        # model = ChatConsultingAssistants(model="OpenAI GPT4")

        # Define the LLM
        model = ChatOpenAI(model=MODEL_NAME)
        log.info(f"Using model: {model} with {MODEL_NAME}")

        # Process input data
        data = await request.json()
        query = data["input"]["query"]
        log.info(f"Query received: {query}")

        #         # create the agent prompt
        #         agent_prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

        # {tools}

        # Use the following format:

        # Question: the input question you must answer
        # Thought: you should always think about what to do
        # Action: the action to take, should be one of [{tool_names}]
        # Action Input: the input to the action
        #  the result of the actionObservation:
        # ... (this Thought/Action/Action Input/Observation can repeat N times)
        # Thought: I now know the final answer
        # Final Answer: the final answer to the original input question

        # Begin!

        # Question: {query}
        # Thought:{agent_scratchpad}""")

        # Get the react prompt template
        prompt_template = hub.pull("hwchase17/react")
        log.info(f"Using prompt template: {prompt_template}")

        try:
            # create the agent and agent_executor
            agent = create_react_agent(model, tools, prompt_template)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
            log.debug("Agent and executor created successfully.")

            # invoke the agent
            raw_result = agent_executor.invoke({"input": query})

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
