# -*- coding: utf-8 -*-
"""
Authors: Max Belitsky, Dennis Weiss

Description: This module provides an integration that can scrape news articles of a specific industry by using a multi-agent setup

This module provides the /result endpoint of autogen_news_webscraper to get the webscraping result
"""

import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, AsyncGenerator, Dict, List, Tuple, Union
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field, ValidationError
from starlette.responses import StreamingResponse

from dev.app.routes.autogen_translator.autogen_integration.const import \
    MESSAGE_SENT
from dev.app.routes.autogen_translator.autogen_integration.group_chats.webscraping.ngc_webscraping import \
    WebscrapingNGC
from dev.app.routes.autogen_translator.autogen_integration.web.conversable_agent_with_async_queue import \
    ConversableAgentWithAsyncQueue
from dev.app.routes.autogen_translator.autogen_integration.web.group_chat_manager_with_async_queue import \
    GroupChatManagerWithAsyncQueue
from dev.app.utilities.utils import run_in_background

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to INFO in production

# Set default model and max threads from environment variables
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("dev/app/routes/autogen_news_webscraper/templates"))


class NewsWebscrapingInputModel(BaseModel):
    """Model to validate input data for timestamp generation."""

    newsUrl: str = Field(description="News URL")
    industry: str = Field(description="Industry to get articles about")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_webscraping_result(
    message_queue: asyncio.Queue,
) -> Tuple[Union[str, None], List[Dict[str, Any]]]:
    """
    Look for the final message of the translator and also returns the whole chat history.

    Args:
        message_queue (asyncio.Queue): The queue containing the chat_history

    Returns:
        Union[str, None]: The translated text in the target language
        List[Dict[str, Any]]: The chat history of the agents that worked to generate the scraped results
    """
    chat_history = []

    while not message_queue.empty():
        message = message_queue.get_nowait()

        if "status" in message and message["status"] == MESSAGE_SENT:
            chat_history.append(message)

    return (
        (
            chat_history[-1]["message"]["content"]
            if len(chat_history) > 0 and "message" in chat_history[-1] and "content" in chat_history[-1]["message"]
            else ""
        ),
        chat_history,
    )


async def get_text_news_webscraping(news_url: str, industry: str) -> Tuple[Union[str, None], List[Dict[str, Any]]]:
    """
    Run the group chat to generate the webscraping result.

    Works by using the NGC implementation and storing the agents' outputs in a queue

    Args:
        text (str): The text to be translated
        language_from (str): Source language of the text to be translated
        language_to (str): Target language to translate to

    Returns:
        Union[str, None]: The translated text in the target language
        List[Dict[str, Any]]: The chat history of the agents that worked to generate the webscraping result
    """
    receive_queue: asyncio.Queue = asyncio.Queue()
    sent_queue: asyncio.Queue = asyncio.Queue()

    webscraping_ngc = WebscrapingNGC(receive_queue, sent_queue, industry)

    webscraping_group_chat_manager = webscraping_ngc.get_manager()
    webscraping_proxy = webscraping_ngc.get_proxy()

    webscraping_prompt_template = template_env.get_template("news_webscraping_prompt.jinja")
    webscraping_prompt = webscraping_prompt_template.render(news_url=news_url, industry=industry)

    await webscraping_proxy.a_initiate_chat(recipient=webscraping_group_chat_manager, message=webscraping_prompt)

    return get_webscraping_result(receive_queue)


async def do_webscraping_group_chat(
    receive_queue: asyncio.Queue,
    group_chat_manager: GroupChatManagerWithAsyncQueue,
    webscraping_proxy: ConversableAgentWithAsyncQueue,
    webscraping_prompt: str,
) -> None:
    """
    Trigger the news webscraping group chat.

    Args:
        receive_queue (asyncio.Queue): Queue on which the chat messages will be written onto
        group_chat_manager (GroupChatManagerWithAsyncQueue): Group chat manager of the news webscraping group chat
        webscraping_proxy (ConversableAgentWithAsyncQueue): Proxy of the news webscraping group chat
        webscraping_prompt (str): Prompt that acts as the initial message of the group chat
    """
    await webscraping_proxy.a_initiate_chat(recipient=group_chat_manager, message=webscraping_prompt)
    await receive_queue.put({"status": "FINISHED"})


async def stream_news_webscraping_chat_response(news_url: str, industry: str) -> AsyncGenerator[str, None]:
    """
    Create the generator which yields the chat messages of the news webscraping group chat.

    Args:
        news_url (str): The URL to scrape and get the news from
        industry (str): The industry of interest

    Returns:
        AsyncGenerator[str, None]: Generator with the JSON strings of the message objects of the news webscraping group chat
    """
    log.debug("Streaming news webscraping chat response")

    invocation_id = str(uuid4())
    event_counter = 0

    try:
        receive_queue: asyncio.Queue = asyncio.Queue()
        sent_queue: asyncio.Queue = asyncio.Queue()

        log.debug("Creating news webscraping NGC")
        webscraping_ngc = WebscrapingNGC(receive_queue, sent_queue, industry)
        log.debug("Created news webscraping NGC")

        webscraping_group_chat_manager = webscraping_ngc.get_manager()
        webscraping_proxy = webscraping_ngc.get_proxy()

        webscraping_prompt_template = template_env.get_template("news_webscraping_prompt.jinja")
        webscraping_prompt = webscraping_prompt_template.render(news_url=news_url, industry=industry)
        log.debug(f"Got webscraping prompt: {webscraping_prompt}")

        run_in_background(
            do_webscraping_group_chat,
            receive_queue=receive_queue,
            group_chat_manager=webscraping_group_chat_manager,
            webscraping_proxy=webscraping_proxy,
            webscraping_prompt=webscraping_prompt,
        )
        log.debug("Started autogen group chat for webscraping")

        while True:
            message = await receive_queue.get()

            if "status" in message and (message["status"] == "WAIT_FOR_USER" or message["status"] == "FINISHED"):
                yield json.dumps(
                    {
                        "status": "success",
                        "invocation_id": invocation_id,
                        "event_id": event_counter,
                        "is_final_event": True,
                        "response": [],
                    }
                )
                break

            sender_agent = message["message"]["name"] if "message" in message and "name" in message["message"] else None
            message_text = (
                message["message"]["content"] if "message" in message and "content" in message["message"] else ""
            )

            yield json.dumps(
                {
                    "status": "success",
                    "invocation_id": invocation_id,
                    "event_id": event_counter,
                    "is_final_event": False,
                    "response": [
                        {
                            "message": (sender_agent + ":\n" if sender_agent is not None else "") + message_text,
                            "type": "text",
                        }
                    ],
                }
            )

            event_counter += 1

    except Exception as e:
        log.exception(f"Error during streaming: {str(e)}")
        yield (
            json.dumps(
                {
                    "status": "error",
                    "invocation_id": invocation_id,
                    "event_id": event_counter,
                    "is_final_event": True,
                    "response": [{"message": str(e), "type": "error"}],
                }
            )
            + "\n"
        )


def add_custom_routes(app: FastAPI) -> None:
    """
    Add custom routes to the FastAPI application for translator agent result retrieval.

    Args:
        app (FastAPI): The FastAPI application to which the routes will be added.

    Returns:
        None

    Example:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> add_custom_routes(app)
        >>> [route.path for route in app.routes]
        ['/autogen_news_webscraper/result']
    """

    @app.post("/autogen_news_webscraper/invoke")
    async def autogen_webscraper(request: Request) -> StreamingResponse:
        """
        Handle POST requests to scrape news pages and return the agents' messages as a stream in real-time.

        Args:
            request (Request): The request object containing the recipient's email address and the content from which the email is based

        Returns:
            OutputModel: The structured output response containing the email sent.

        Raises:
            HTTPException: If the input is invalid or the email generation fails.
        """
        log.info("Received a request to invoke the mail generation group chat (streaming).")

        try:
            data: Dict[str, Any] = await request.json()
            log.debug(f"Received data: {data}")
            input_data = NewsWebscrapingInputModel(**data)
            log.debug(f"Validated input data: {input_data}")

            response = StreamingResponse(
                stream_news_webscraping_chat_response(input_data.newsUrl, input_data.industry),
                media_type="application/json",
            )
            return response
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            log.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=json.loads(e.json()))

    @app.post("/autogen_news_webscraper/result")
    async def autogen_webscraper_result(request: Request) -> OutputModel:
        """
        Handle POST requests to scrape news pages.

        Args:
            request (Request): The request object containing the industry.

        Returns:
            OutputModel: The structured output response containing the translated text.

        Raises:
            HTTPException: If the input is invalid or the webscraping fails.
        """
        log.info("Received request to translate text")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = NewsWebscrapingInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    asyncio.run,
                    get_text_news_webscraping(input_data.newsUrl, input_data.industry),
                )

            (
                news_webscraping_result,
                chat_history,
            ) = future.result()  # pylint: disable=unused-variable
        except RuntimeError as e:
            log.error(f"Error during webscraping: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate translated text")

        log.info(f"The result of the webscraping: {news_webscraping_result}")

        response_template = template_env.get_template("response.jinja")
        response_message = ResponseMessageModel(
            message=response_template.render(news_webscraping_result=news_webscraping_result)
        )
        return OutputModel(invocationId=invocation_id, response=[response_message])
