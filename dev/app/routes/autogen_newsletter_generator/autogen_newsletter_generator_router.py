# -*- coding: utf-8 -*-
"""
Authors: Stan Furrer, Dennis Weiss.

Description: This module provides an integration that generate a newsletter about industry of interest in given language and send it by email using a multi-agent setup.

This module provides the /result endpoint of autogen_newsletter_generator to get the newsletter result
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
from dev.app.routes.autogen_translator.autogen_integration.group_chats.newsletter.ngc_newsletter import \
    NewsletterNGC
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
# Default URL as fallback
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("dev/app/routes/autogen_newsletter_generator/templates"))


class NewsletterInputModel(BaseModel):
    """Model to validate input data for timestamp generation."""

    language: str = Field(default="English", description="Language of the newsletter")
    newsUrl: str = Field(description="URL of the new page to scrape from")
    industry: str = Field(description="Industry of interest")
    emailAddress: str = Field(description="Email address to send the newsletter to")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_newsletter_result(
    message_queue: asyncio.Queue,
) -> Tuple[Union[str, None], List[Dict[str, Any]]]:
    """
    Look for the final message of the newsletter-generator and also returns the whole chat history.

    Args:
        message_queue (asyncio.Queue): The queue containing the chat_history

    Returns:
        Union[str, None]: The newsletter
        List[Dict[str, Any]]: The chat history of the agents that worked to generate the newsletter.
    """
    chat_history = []
    newsletter = None

    while not message_queue.empty():
        message = message_queue.get_nowait()
        if "status" in message and message["status"] == MESSAGE_SENT:
            chat_history.append(message)
            if (
                "message" in message
                and "name" in message["message"]
                and message["message"]["name"] == "email_writer_agent"
                and "content" in message["message"]
            ):
                newsletter = message["message"]["content"]
    return newsletter, chat_history


async def get_newsletter(
    language: str, news_url: str, industry: str, email_address: str
) -> Tuple[Union[str, None], List[Dict[str, Any]]]:
    """
    Run the group chat to generate the newsletter.

    Works by using the NGC implementation and storing the agents' outputs in a queue

    Args:
        language: Language of the newsletter.
        news_url: URL of the news page
        industry: Industry of interest.
        email_address: Email address to send the newsletter to.

    Returns:
        Union[str, None]: The newsletter in the language.
        List[Dict[str, Any]]: The chat history of the agents that worked to generate the newsletter.
    """
    receive_queue: asyncio.Queue = asyncio.Queue()
    sent_queue: asyncio.Queue = asyncio.Queue()

    newsletter_ngc = NewsletterNGC(
        receive_queue,
        sent_queue,
        industry=industry,
        recipient_email_address=email_address,
    )

    newsletter_group_chat_manager = newsletter_ngc.get_manager()
    newsletter_proxy = newsletter_ngc.get_proxy()

    newsletter_prompt_template = template_env.get_template("newsletter_generation_prompt.jinja")
    newsletter_prompt = newsletter_prompt_template.render(
        news_url=news_url, language=language, email_address=email_address
    )

    await newsletter_proxy.a_initiate_chat(recipient=newsletter_group_chat_manager, message=newsletter_prompt)

    return get_newsletter_result(receive_queue)


async def do_newsletter_generation_group_chat(
    receive_queue: asyncio.Queue,
    group_chat_manager: GroupChatManagerWithAsyncQueue,
    newsletter_proxy: ConversableAgentWithAsyncQueue,
    newsletter_prompt: str,
) -> None:
    """
    Trigger the newsletter generation group chat.

    Args:
        receive_queue (asyncio.Queue): Queue on which the chat messages will be written onto
        group_chat_manager (GroupChatManagerWithAsyncQueue): Group chat manager of the newsletter generation group chat
        newsletter_proxy (ConversableAgentWithAsyncQueue): Proxy of the newsletter generation group chat
        newsletter_prompt (str): Prompt that acts as the initial message of the group chat
    """
    await newsletter_proxy.a_initiate_chat(recipient=group_chat_manager, message=newsletter_prompt)
    await receive_queue.put({"status": "FINISHED"})


async def stream_newsletter_generator_chat_response(
    language: str, news_url: str, industry: str, email_address: str
) -> AsyncGenerator[str, None]:
    """
    Create the generator which yields the chat messages of the newsletter generator group chat.

    Args:
        language: Language of the newsletter.
        news_url: URL of the news page
        industry: Industry of interest.
        email_address: Email address to send the newsletter to.

    Returns:
        Union[str, None]: The newsletter in the language.
        List[Dict[str, Any]]: The chat history of the agents that worked to generate the newsletter.
    """
    log.debug("Streaming newsletter generator chat response")

    invocation_id = str(uuid4())
    event_counter = 0

    try:
        receive_queue: asyncio.Queue = asyncio.Queue()
        sent_queue: asyncio.Queue = asyncio.Queue()

        log.debug("Creating newsletter NGC")
        newsletter_ngc = NewsletterNGC(receive_queue, sent_queue, industry, email_address)
        log.debug("Created newsletter NGC")

        newsletter_group_chat_manager = newsletter_ngc.get_manager()
        newsletter_proxy = newsletter_ngc.get_proxy()

        newsletter_prompt_template = template_env.get_template("newsletter_generation_prompt.jinja")
        newsletter_prompt = newsletter_prompt_template.render(
            news_url=news_url, language=language, email_address=email_address
        )
        log.debug(f"Got newsletter prompt: {newsletter_prompt}")

        run_in_background(
            do_newsletter_generation_group_chat,
            receive_queue=receive_queue,
            group_chat_manager=newsletter_group_chat_manager,
            newsletter_proxy=newsletter_proxy,
            newsletter_prompt=newsletter_prompt,
        )
        log.debug("Started autogen group chat for newsletter generation")

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
    Add custom routes to the FastAPI application for newsletter agent result retrieval.

    Args:
        app (FastAPI): The FastAPI application to which the routes will be added.

    Returns:
        None

    Example:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> add_custom_routes(app)
        >>> [route.path for route in app.routes]
        ['/autogen_newsletter/result']
    """

    @app.post("/autogen_newsletter_generator/invoke")
    async def autogen_newsletter_generator(request: Request) -> StreamingResponse:
        """
        Handle POST requests to generate the newsletter and return the agents' messages as a stream in real-time.

        Args:
            request (Request): The request object containing the language, industry of interest and email address.

        Returns:
            OutputModel: The structured output response containing the newsletter text.

        Raises:
            HTTPException: If the input is invalid or the newsletter fails.
        """
        log.info("Received a request to invoke the newsletter generation group chat (streaming).")

        try:
            data: Dict[str, Any] = await request.json()
            log.debug(f"Received data: {data}")
            input_data = NewsletterInputModel(**data)
            log.debug(f"Validated input data: {input_data}")

            response = StreamingResponse(
                stream_newsletter_generator_chat_response(
                    input_data.language,
                    input_data.newsUrl,
                    input_data.industry,
                    input_data.emailAddress,
                ),
                media_type="application/json",
            )
            return response
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            log.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=json.loads(e.json()))

    @app.post("/autogen_newsletter_generator/result")
    async def autogen_newsletter_generator_result(request: Request) -> OutputModel:
        """
        Handle POST requests to generate the newsletter.

        Args:
            request (Request): The request object containing the language, industry of interest and email address.

        Returns:
            OutputModel: The structured output response containing the newsletter text.

        Raises:
            HTTPException: If the input is invalid or the newsletter fails.
        """
        log.info("Received request to generate the newsletter")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = NewsletterInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    asyncio.run,
                    get_newsletter(
                        input_data.language,
                        input_data.newsUrl,
                        input_data.industry,
                        input_data.emailAddress,
                    ),
                )

            (
                newsletter,
                chat_history,
            ) = future.result()  # pylint: disable=unused-variable
        except RuntimeError as e:
            log.error(f"Error generating newsletter: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate newsletter")

        log.info(f"{newsletter}")

        response_template = template_env.get_template("response.jinja")
        response_message = ResponseMessageModel(message=response_template.render(newsletter=newsletter))
        return OutputModel(invocationId=invocation_id, response=[response_message])
