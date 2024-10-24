# -*- coding: utf-8 -*-
import asyncio
import json
import os
from typing import Any, Dict, List

import aiohttp
import streamlit as st
from pydantic import BaseModel

# Read the environment variables
api_url = os.environ.get("AGENT_API_URL", "http://localhost:8080/agent_langchain/invoke")
api_key = os.environ.get("AGENT_API_KEY", "dev-only-token")

# List of available tools
AVAILABLE_TOOLS = [
    "google_search",
    "retrieve_website_content",
    "mermaid_create_diagram",
    "docbuilder_tool_markdown_to_pptx_docx",
    "summarize_text_tool",
    "get_system_time",
    "get_collections_tool",
    "query_documents_tool",
    "GPT-4 Vision",
    "pii_masker_tool",
    "get_prompts_tool",
    "get_assistants_tool",
    "wikipedia_search",
    "create_chart",
]


class AgentRequest(BaseModel):
    """Model for the agent request payload."""

    query: str
    tools: List[str]


async def send_request(
    session: aiohttp.ClientSession, message: str, selected_tools: List[str]
) -> aiohttp.ClientResponse:
    """Send a request to the agent API."""
    payload = AgentRequest(query=message, tools=selected_tools)
    return await session.post(api_url, json=payload.dict(), headers={"Integrations-API-Key": api_key})


async def process_response_line(line: bytes) -> Dict[str, Any]:
    """Process a line of the API response."""
    if line.strip():
        return json.loads(line.decode("utf-8"))
    return {}


def display_event(event: Dict[str, Any], placeholder, chain_of_thought) -> None:
    """Display an event from the API response."""
    if event.get("is_final_event", False):
        content = event["response"][0]["message"]
        placeholder.markdown(f"**Final Answer:** {content}")
    else:
        message = event["response"][0]["message"]
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                chain_of_thought.append(f"📝 **Message:** {message}")
                return

        thought = ""
        if "thought" in message:
            thought = f"🕵🏻 **Agent:** {message.get('agent_name', 'Unknown')}\n\n💭 **Thought:** {message['thought']}"
            chain_of_thought.append(thought)

        action = ""
        if "action" in message:
            action = f"🎬 **Action:** {message['action']}\n\n📥 **Input:** {message.get('tool_input', 'N/A')}"
            chain_of_thought.append(action)

        observation = ""
        if "observation" in message:
            observation = f"👁️ **Observation:** {message['observation']}"
            chain_of_thought.append(observation)

        # Display the latest step in the main area
        placeholder.markdown(thought + "\n\n" + action + "\n\n" + observation)


async def main_loop(message: str, selected_tools: List[str], placeholder, chain_of_thought):
    """Main loop to handle user messages and interact with the agent."""
    async with aiohttp.ClientSession() as session:
        response = await send_request(session, message, selected_tools)
        async for line in response.content:
            processed_event = await process_response_line(line)
            if processed_event:
                display_event(processed_event, placeholder, chain_of_thought)


def run_async(coroutine):
    """Run an asynchronous coroutine."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)


# Streamlit UI
st.title("LangChain Agent UI")

# Tool selection
selected_tools = st.multiselect("Select tools to use:", AVAILABLE_TOOLS, default=AVAILABLE_TOOLS)

# User input
user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_input:
        # Create a placeholder for the streaming output
        output_placeholder = st.empty()

        # Create a list to store the chain of thought
        chain_of_thought = []

        # Run the main loop
        run_async(main_loop(user_input, selected_tools, output_placeholder, chain_of_thought))

        # Display the full chain of thought in a collapsible element
        with st.expander("View Full Chain of Thought"):
            for step in chain_of_thought:
                st.markdown(step)
                st.markdown("---")
    else:
        st.warning("Please enter a query.")

# Display selected tools
st.sidebar.write("Selected Tools:")
for tool in selected_tools:
    st.sidebar.write(f"- {tool}")
