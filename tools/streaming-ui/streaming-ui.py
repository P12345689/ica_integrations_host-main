#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: A Streamlit app for chatting with an AI model or integration.

This application is designed to prototype and test streaming support for integrations.

Edit the integrations list in integrations.json

This app allows users to select an AI model or integration and engage in a conversation with it.
The conversation history is displayed in a scrollable container, and the user input
is always at the bottom.

Pressing "Enter" or clicking the "Send" button sends the
user's message to the AI model or integration and displays the response.

Example:
    To run the app, execute:
        $ streamlit run app.py

Environment Variables:
    API_URL (str): The URL of the API endpoint for generating AI responses.
        Default: "http://localhost:11434/api/generate"
"""

import asyncio
import json
import logging
import os
from typing import AsyncGenerator

import httpx
import streamlit as st
from dotenv import load_dotenv
from jinja2 import Template

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:11434/api/generate")

# Read INTEGRATIONS from an external JSON file
with open("integrations.json", "r") as file:
    INTEGRATIONS = json.load(file)
    log.info(f"Loaded integrations: {INTEGRATIONS}")


def setup_async() -> asyncio.AbstractEventLoop:
    """
    Set up an async event loop.

    Returns:
        asyncio.AbstractEventLoop: The created async event loop.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    log.info("Async event loop set up")
    return loop


async def send_request(model: str, prompt: str) -> AsyncGenerator[str, None]:
    """
    Send a request to the API and stream the response.

    Args:
        model (str): The name of the AI model to use.
        prompt (str): The user's message to send to the AI model.

    Yields:
        str: The AI model's response, streamed in chunks.

    Raises:
        httpx.RequestError: If an error occurs while making the request.
        json.JSONDecodeError: If the received response is not valid JSON.
    """
    log.info(f"Sending request to API with model: {model} and prompt: {prompt}")
    async with httpx.AsyncClient(timeout=90.0) as client:
        full_response = ""  # Initialize an empty string to accumulate the response
        try:
            async with client.stream("POST", API_URL, json={"model": model, "prompt": prompt}) as response:
                log.info(f"Received response from API with status code: {response.status_code}")
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        log.info(f"Received data from API: {data}")
                        if "response" in data:
                            full_response += data["response"]  # Append part of the response
                        if data.get("done", False):
                            yield full_response  # Yield the complete response when done
                            log.info("API response complete and sent to Streamlit")
                            break
        except json.JSONDecodeError as e:
            log.error(f"Received malformed JSON: {e}. JSON: {line}")
            st.error(f"Received malformed JSON: {e}. JSON: {line}")
        except httpx.RequestError as e:
            log.error(f"An error occurred: {type(e).__name__} - {str(e)}")
            st.error(f"An error occurred: {type(e).__name__}")


async def send_integration_request(endpoint: dict, prompt: str) -> AsyncGenerator[str, None]:
    """
    Send a request to the integration endpoint and stream the response.

    Args:
        endpoint (dict): The integration endpoint details.
        prompt (str): The user's message to send to the integration.

    Yields:
        str: The integration's response, streamed in chunks.

    Raises:
        httpx.RequestError: If an error occurs while making the request.
        json.JSONDecodeError: If the received response is not valid JSON.
    """
    log.info(f"Sending request to integration endpoint: {endpoint['path']} with prompt: {prompt}")
    async with httpx.AsyncClient(timeout=90.0) as client:
        try:
            payload = endpoint["payload"].copy() if endpoint["payload"] else {}
            payload_template = Template(json.dumps(payload))
            payload = json.loads(payload_template.render(input=prompt))
            log.info(f"Payload for integration request: {payload}")

            headers = {
                "Content-Type": endpoint["content_type"],
                "Integrations-API-Key": endpoint["authorization"],  # Add authorization header
            }

            async with client.stream(
                "POST",
                f"{INTEGRATIONS['server_url']}{endpoint['path']}",
                json=payload,
                headers=headers,
            ) as response:
                log.info(f"Received response from integration endpoint with status code: {response.status_code}")

                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        log.info(f"Received data from integration endpoint: {data}")

                        if data.get("status") == "success" and "response" in data:
                            for item in data["response"]:
                                if "message" in item:
                                    message_type = item.get("type", "text")
                                    log.info(f"Processing message of type: {message_type}")
                                    if message_type == "text":
                                        yield item["message"]
                                    elif message_type == "image":
                                        yield f"![Image]({item['message']})"
                                    else:
                                        log.warning(f"Unsupported message type: {message_type}")
                                        yield f"Unsupported message type: {message_type}"
                        else:
                            log.error(f"Unexpected response format from integration endpoint: {data}")
                            yield f"Unexpected response format from integration endpoint: {data}"

        except json.JSONDecodeError as e:
            log.error(f"Received malformed JSON: {e}. JSON: {line}")
            st.error(f"Received malformed JSON: {e}. JSON: {line}")
        except httpx.RequestError as e:
            log.error(f"An error occurred: {type(e).__name__} - {str(e)}")
            st.error(f"An error occurred: {type(e).__name__}")


def main():
    """
    The main function that sets up and runs the Streamlit app.
    """
    log.info("Setting up Streamlit app")
    st.set_page_config(
        page_title="Chat with AI Model or Integration",
        page_icon=":speech_balloon:",
        layout="wide",
    )
    st.title("Discount Sidekick")

    chat_type = st.sidebar.selectbox("Choose Chat Type", ["Model", "Integration"])
    st.sidebar.markdown(
        """
        <style>
            .sidebar .sidebar-content {
                width: 200px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    log.info(f"Selected chat type: {chat_type}")

    if chat_type == "Model":
        model = st.sidebar.selectbox("Choose Model", ["mistral", "phi3", "llama3"], index=1)
        log.info(f"Selected model: {model}")
    else:
        integration = st.sidebar.selectbox(
            "Choose Integration",
            [endpoint["path"] for endpoint in INTEGRATIONS["endpoints"]],
        )
        log.info(f"Selected integration: {integration}")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        log.info("Initialized chat history in session state")

    chat_container = st.container()
    chat_container.markdown(
        '<div style="max-height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">{}</div>'.format(
            "".join(
                [
                    "<div><strong>{role}:</strong> {message}</div>".format(
                        role="User" if role == "User" else "Assistant", message=message
                    )
                    for role, message in st.session_state.chat_history
                ]
            )
        ),
        unsafe_allow_html=True,
    )

    user_input = st.text_input("Your message:", key="user_input", on_change=lambda: None)
    log.info(f"User input: {user_input}")

    if (st.button("Send") or st.session_state.get("user_input_submitted", False)) and user_input:
        log.info("User submitted a message")
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.user_input_submitted = False
        user_input = ""  # Clear input after message is sent

        loop = setup_async()
        response_container = st.empty()
        response_text = ""

        async def display_response():
            nonlocal response_text
            log.info(f"Displaying response for chat type: {chat_type}")
            if chat_type == "Model":
                async for chunk in send_request(model, st.session_state.chat_history[-1][1]):
                    chunk = chunk.replace("\n", "<br>")  # Replace newlines with HTML line breaks
                    response_text += chunk
                    response_container.markdown(
                        f'<div style="background-color: #F0F8FF; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: #000000;">'
                        f"<strong>Assistant:</strong><br/>{response_text}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                endpoint = next(endpoint for endpoint in INTEGRATIONS["endpoints"] if endpoint["path"] == integration)
                async for chunk in send_integration_request(endpoint, st.session_state.chat_history[-1][1]):
                    chunk = chunk.replace("\n", "<br>")  # Replace newlines with HTML line breaks
                    response_text += chunk
                    response_container.markdown(
                        f'<div style="background-color: #F0F8FF; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: #000000;">'
                        f"<strong>Assistant:</strong><br/>{response_text}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

        loop.run_until_complete(display_response())
        st.session_state.chat_history.append(("Assistant", response_text))
        log.info("Response displayed and added to chat history")

    def submit_on_enter(event):
        """
        Submit the user's message when the "Enter" key is pressed.

        Args:
            event: The keypress event.
        """
        if event.key == "Enter":
            st.session_state.user_input_submitted = True
            log.info("User submitted message by pressing Enter")

    st.session_state.user_input_submitted = False
    st.text_input("", key="user_input_submit", on_change=submit_on_enter)


if __name__ == "__main__":
    log.info("Starting the main function")
    main()
