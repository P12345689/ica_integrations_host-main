# -*- coding: utf-8 -*-
"""
Authors: Dennis Weiss, Max Belitsky, Alexandre Carlhammar, Stan Furrer.

Description: This module provides This module provides an integration that can generate and send
              a newsletter email and its attached audio version based on input content to a specified
              recipient's email address, using a multi-agent setup.

This module provides the /result endpoint of autogen_mail_generator to get the sent email
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
from dev.app.routes.autogen_translator.autogen_integration.group_chats.mail_generation.ngc_mail_generation import \
    EmailNGC
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
template_env = Environment(loader=FileSystemLoader("dev/app/routes/autogen_mail_generator/templates"))


class EmailGenarationInputModel(BaseModel):
    """Model to validate input data for timestamp generation."""

    text: str = Field(description="Content from which to base the email")
    recipientEmailAddress: str = Field(description="Email recipient's email address")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_email_generation_result(
    message_queue: asyncio.Queue,
) -> Tuple[Union[str, None], List[Dict[str, Any]]]:
    """
    Look for the final message of the mail generator and also returns the whole chat history.

    Args:
        message_queue (asyncio.Queue): The queue containing the chat_history

    Returns:
        Union[str, None]: The sent email text
        List[Dict[str, Any]]: The chat history of the agents that worked to generate the email
    """
    chat_history = []
    email_generation = None

    while not message_queue.empty():
        message = message_queue.get_nowait()
        chat_history.append(message)
        if "status" in message and message["status"] == MESSAGE_SENT:
            if (
                "message" in message
                and "name" in message["message"]
                and message["message"]["name"] == "evaluator_agent"
                and "content" in message["message"]
            ):
                email_generation = message["message"]["content"]

    return email_generation, chat_history


async def get_email_generation(
    text: str, recipient_email_address: str
) -> Tuple[Union[str, None], List[Dict[str, Any]]]:
    """
    Run the group chat to generate the email.

    Works by using the NGC implementation and storing the agents' outputs in a queue

    Args:
        text (str): Content from which to base the email
        recipient_email_address (str): Recipient's email address

    Returns:
        Union[str, None]: The sent email text
        List[Dict[str, Any]]: The chat history of the agents that worked to generate the email
    """
    receive_queue: asyncio.Queue = asyncio.Queue()
    sent_queue: asyncio.Queue = asyncio.Queue()

    email_generation_ngc = EmailNGC(receive_queue, sent_queue, recipient_email_address=recipient_email_address)

    mail_generation_group_chat_manager = email_generation_ngc.get_manager()
    mail_generation_proxy = email_generation_ngc.get_proxy()

    mail_generation_prompt_template = template_env.get_template("email_generation_prompt.jinja")
    mail_generation_prompt = mail_generation_prompt_template.render(
        text=text,
        recipientEmailAddress=recipient_email_address,
    )

    await mail_generation_proxy.a_initiate_chat(
        recipient=mail_generation_group_chat_manager, message=mail_generation_prompt
    )

    return get_email_generation_result(receive_queue)


async def do_mail_generation_group_chat(
    receive_queue: asyncio.Queue,
    group_chat_manager: GroupChatManagerWithAsyncQueue,
    mail_generation_proxy: ConversableAgentWithAsyncQueue,
    mail_generation_prompt: str,
) -> None:
    """
    Trigger the mail generation group chat.

    Args:
        receive_queue (asyncio.Queue): Queue on which the chat messages will be written onto
        group_chat_manager (GroupChatManagerWithAsyncQueue): Group chat manager of the mail generation group chat
        mail_generation_proxy (ConversableAgentWithAsyncQueue): Proxy of the mail generation group chat
        mail_generation_prompt (str): Prompt that acts as the initial message of the group chat
    """
    await mail_generation_proxy.a_initiate_chat(recipient=group_chat_manager, message=mail_generation_prompt)
    await receive_queue.put({"status": "FINISHED"})


async def stream_mail_generation_chat_response(text: str, recipient_email_address: str) -> AsyncGenerator[str, None]:
    """
    Create the generator which yields the chat messages of the email generation group chat.

    Works by using the NGC implementation and storing the agents' outputs in a queue

    Args:
        text (str): Content from which to base the email
        recipient_email_address (str): Recipient's email address

    Returns:
        AsyncGenerator[str, None]: Generator with the JSON strings of the message objects of the email generation group chat
    """
    log.debug("Streaming email generation chat response")

    invocation_id = str(uuid4())
    event_counter = 0

    try:
        receive_queue: asyncio.Queue = asyncio.Queue()
        sent_queue: asyncio.Queue = asyncio.Queue()

        log.debug("Creating email generation NGC")
        email_ngc = EmailNGC(receive_queue, sent_queue, recipient_email_address=recipient_email_address)
        log.debug("Created email generation NGC")

        mail_generation_group_chat_manager = email_ngc.get_manager()
        mail_generation_proxy = email_ngc.get_proxy()

        mail_generation_prompt_template = template_env.get_template("email_generation_prompt.jinja")
        mail_generation_prompt = mail_generation_prompt_template.render(
            text=text,
            recipientEmailAddress=recipient_email_address,
        )
        log.debug(f"Got mail generation prompt: {mail_generation_prompt}")

        run_in_background(
            do_mail_generation_group_chat,
            receive_queue=receive_queue,
            group_chat_manager=mail_generation_group_chat_manager,
            mail_generation_proxy=mail_generation_proxy,
            mail_generation_prompt=mail_generation_prompt,
        )
        log.debug("Started autogen group chat for mail generation")

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
    Add custom routes to the FastAPI application for email generator agent result retrieval.

    Args:
        app (FastAPI): The FastAPI application to which the routes will be added.

    Returns:
        None

    Example:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> add_custom_routes(app)
        >>> [route.path for route in app.routes]
        ['/autogen_mail_generator/result']
    """

    @app.post("/autogen_mail_generator/invoke")
    async def autogen_mail_generator(request: Request) -> StreamingResponse:
        """
        Handle POST requests to generate an email given a newsletter content and return the agents' messages as a stream in real-time.

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
            input_data = EmailGenarationInputModel(**data)
            log.debug(f"Validated input data: {input_data}")

            response = StreamingResponse(
                stream_mail_generation_chat_response(input_data.text, input_data.recipientEmailAddress),
                media_type="application/json",
            )
            return response
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            log.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=json.loads(e.json()))

    @app.post("/autogen_mail_generator/result")
    async def autogen_mail_generator_result(request: Request) -> OutputModel:
        """
        Handle POST requests to generate an email given a newsletter content.

        Args:
            request (Request): The request object containing the recipient's email address and the content from which the email is based

        Returns:
            OutputModel: The structured output response containing the email sent.

        Raises:
            HTTPException: If the input is invalid or the email generation fails.
        """
        log.info("Received request to generate an email")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = EmailGenarationInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    asyncio.run,
                    get_email_generation(input_data.text, input_data.recipientEmailAddress),
                )

            (
                email_sent,
                chat_history,
            ) = future.result()  # pylint: disable=unused-variable
        except RuntimeError as e:
            log.error(f"Error generating email: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate email")

        log.info(f"Generated email: {email_sent}")

        response_template = template_env.get_template("response.jinja")
        response_message = ResponseMessageModel(
            message=response_template.render(
                recipientEmailAddress=input_data.recipientEmailAddress,
                emailSent=email_sent,
            )
        )
        return OutputModel(invocationId=invocation_id, response=[response_message])
