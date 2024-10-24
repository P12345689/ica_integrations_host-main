# -*- coding: utf-8 -*-
"""
Author: Dennis Weiss, Stan Furrer
Description: Email Generation Nested Group Chat
"""

import asyncio
import json
import os
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
from typing import Annotated, Any, Dict

from autogen import GroupChat, register_function
from jinja2 import Environment, FileSystemLoader

from dev.app.routes.autogen_translator.autogen_integration.const import (  # pylint: disable=unused-import
    DESC, DISALLOWED, MAIL_IMAGE_PATH_FOOTER, MAIL_IMAGE_PATH_LOGO, NEVER,
    OPENAI_API_VERSION, SENDER, SYS_MSG)
from dev.app.routes.autogen_translator.autogen_integration.web.assistant_agent_with_async_queue import \
    AssistantAgentWithAsyncQueue
from dev.app.routes.autogen_translator.autogen_integration.web.conversable_agent_with_async_queue import \
    ConversableAgentWithAsyncQueue
from dev.app.routes.autogen_translator.autogen_integration.web.group_chat_manager_with_async_queue import \
    GroupChatManagerWithAsyncQueue

# Defining custom type annotations for the send_email() tool function's parameters
Subject = Annotated[str, "The subject of the email"]
Body = Annotated[str, "The body of the email"]
ToEmail = Annotated[str, "The recipient's email addres"]


def template_html(body: str) -> str:
    """
    Generate an HTML template for the email content.

    Args:
        body (str): The body of the email:
    """
    body = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", body)
    body = body.replace("\n", "<br>")
    today_date = datetime.now().strftime("%B %d, %Y")
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 0; margin: 0;">
        <div style="max-width: 600px; margin: 20px auto; border: 1px solid #ddd; background-color: #fff;">
            <div style="display: flex; align-items: center; background-color: #e5e0df; padding: 0;">
                <div style="width: 66.66%; padding: 20px; font-weight: bold; font-size: 1.2em; line-height: 1.5;">
                    IBM Consulting Assistant Generated Newsletter<br>{today_date}
                </div>
                <div style="width: 33.33%; text-align: right;">
                    <img src="cid:top_image" alt="Top Image" style="width: 100%; height: auto; display: block;">
                </div>
            </div>
            <div style="padding: 20px;">
                <p>{body}</p>
            </div>
            <div style="background-color: #f0f0f0; padding: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 0.9em; color: #555;">
                    This is a communication from IBM Consulting Assistant.
                </div>
                <div style="text-align: right;">
                    <img src="cid:footer_image" alt="Footer Image" style="max-width: 50px;">
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def send_mail(subject: Subject, body: Body, to_email: ToEmail) -> str:
    """
    Send an email with a given subject, body, and recipient email.

    Args:
        subject (Subject): The subject of the email.
        body (Body): The body of the email.
        to_email (ToEmail): The recipient's email address.

    Returns:
        str: A success message if the email is sent successfully, or an error message if there's an error.
    """
    # Generate HTML content
    html_body = template_html(body)

    # get email sender
    sender = SENDER

    # setup email content
    message = EmailMessage()
    message.set_content(body)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = to_email

    message.add_alternative(html_body, subtype="html")

    # Add top image as an attachment
    try:
        with open(MAIL_IMAGE_PATH_LOGO, "rb") as img:
            message.get_payload()[-1].add_related(img.read(), "image", "png", cid="top_image")
    except FileNotFoundError:
        return "Error: Top image file not found."

    # Add footer image as an attachment
    try:
        with open(MAIL_IMAGE_PATH_FOOTER, "rb") as footer_img:
            message.get_payload()[-1].add_related(footer_img.read(), "image", "png", cid="footer_image")
    except FileNotFoundError:
        return "Error: Footer image file not found."

    # add audio file as an attachment
    # try:
    #     with open(AUDIO, 'rb') as file:
    #         message.add_attachment(
    #             file.read(), maintype='audio', subtype='mp3', filename=os.path.basename(AUDIO))
    # except FileNotFoundError:
    #     return "Error: Audio file not found."
    # except Exception as e:
    #     return f"Error: {e}"

    try:
        smtp_address = os.environ.get("AUTOGEN_EMAIL_GENERATOR_SMTP_ADDRESS")
        smtp_port = os.environ.get("AUTOGEN_EMAIL_GENERATOR_SMTP_PORT")
        smtp_username = os.environ.get("AUTOGEN_EMAIL_GENERATOR_SMTP_USERNAME")
        smtp_password = os.environ.get("AUTOGEN_EMAIL_GENERATOR_SMTP_PASSWORD")

        if smtp_address is None:
            return "AUTOGEN_EMAIL_GENERATOR_SMTP_ADDRESS env variable is not set."
        if smtp_port is None:
            return "AUTOGEN_EMAIL_GENERATOR_SMTP_PORT env variable is not set."
        if smtp_username is None:
            return "AUTOGEN_EMAIL_GENERATOR_SMTP_USERNAME env variable is not set."
        if smtp_password is None:
            return "AUTOGEN_EMAIL_GENERATOR_SMTP_PASSWORD env variable is not set."

        with smtplib.SMTP(smtp_address, int(smtp_port)) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(message)
    except smtplib.SMTPException as e:
        return f"Error sending email: {e}"
    return "Email sent successfully"


class EmailNGC:  # pylint: disable=too-many-instance-attributes
    """
    Class that contains the agents that are setup in an autogen group chat.

    The configuration is loaded automatically from the jinja templates
    It is necessary to call set_queues to populate the asyncio queues used for async input and output of messages.
    """

    def __init__(
        self,
        client_receive_queue: asyncio.Queue,
        client_sent_queue: asyncio.Queue,
        recipient_email_address: str,
    ) -> None:
        """
        Initialize the EmailNGC class.

        Class that contains the agents that are setup in an autogen group chat.

        The configuration is loaded automatically from agents_config.json.
        It is necessary to call set_queues to populate the asyncio queues used for async input and output of messages.
        """
        self.recipient_email_address = recipient_email_address

        # Load Jinja2 environment
        self.__template_env = Environment(loader=FileSystemLoader("dev/app/routes/autogen_mail_generator/templates"))

        agents_config = self.__load_agents_config()
        self.__config = agents_config["ngc_email_generation"]
        self.__llm_config = {
            "model": os.environ["AUTOGEN_EMAIL_GENERATOR_AZURE_OPENAI_DEPLOYMENT"],
            "api_key": os.environ["AUTOGEN_EMAIL_GENERATOR_AZURE_OPENAI_API_KEY"],
            "api_type": "azure",
            "base_url": os.environ["AUTOGEN_EMAIL_GENERATOR_AZURE_OPENAI_ENDPOINT"],
            "api_version": OPENAI_API_VERSION,
        }
        self.__setup_agents(client_receive_queue, client_sent_queue)
        self.__setup_group_chat(client_receive_queue, client_sent_queue)
        self.__register_functions()

    @staticmethod
    def __load_agents_config() -> Dict[str, Any]:
        """
        Load the agents config from the local JSON file.

        Returns:
            Dict[str, Any]: agents configuration
        """
        script_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(script_dir, "agents_config.json")
        with open(json_file_path, encoding="utf-8") as f:
            return json.load(f)

    def __setup_agents(self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue) -> None:
        """
        Set up all the agents.

        Args:
            client_receive_queue (asyncio.Queue): Queue on which the agents' messages will be saved
            client_sent_queue (asyncio.Queue): Queue on which the user's messages will be read from
        """
        self.__email_sender_agent = AssistantAgentWithAsyncQueue(
            name="email_sender_agent",
            system_message=self.__template_env.get_template("email_sender_sys_msg.jinja").render(
                recipient_email_address=self.recipient_email_address
            ),
            description="\n".join(self.__config["email_sender_agent"][DESC]),
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
        )
        self.__email_sender_agent.set_queues(client_receive_queue, client_sent_queue)

        self.__execute_email = ConversableAgentWithAsyncQueue(
            name="execute_email", llm_config=False, human_input_mode=NEVER
        )
        self.__execute_email.set_queues(client_receive_queue, client_sent_queue)

        self.__summary_agent = ConversableAgentWithAsyncQueue(
            name="summary_agent",
            system_message="\n".join(self.__config["summary_agent"][SYS_MSG]),
            description="\n".join(self.__config["summary_agent"][DESC]),
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
        )
        self.__summary_agent.set_queues(client_receive_queue, client_sent_queue)

        self.__email_writer_agent = ConversableAgentWithAsyncQueue(
            name="email_writer_agent",
            system_message="\n".join(self.__config["email_writer_agent"][SYS_MSG]),
            description="\n".join(self.__config["email_writer_agent"][DESC]) + f"The sender is {SENDER}",
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
        )

        self.__email_writer_agent.set_queues(client_receive_queue, client_sent_queue)

        self.__evaluator_agent = ConversableAgentWithAsyncQueue(
            name="evaluator_agent",
            system_message="\n".join(self.__config["evaluator_agent"][SYS_MSG]),
            description="\n".join(self.__config["evaluator_agent"][DESC]) + f"The sender is {SENDER}",
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
        )
        self.__evaluator_agent.set_queues(client_receive_queue, client_sent_queue)

        self.group_chat_proxy = ConversableAgentWithAsyncQueue(
            name="email_proxy",
            code_execution_config=False,
            human_input_mode=NEVER,
            description="\n".join(self.__config["email_proxy"][DESC]),
            is_termination_msg=lambda msg: msg["name"] == self.__execute_email.name,
        )
        self.group_chat_proxy.set_queues(client_receive_queue, client_sent_queue)

    def __setup_group_chat(self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue) -> None:
        """
        Set up the group chat.

        Args:
            client_receive_queue (asyncio.Queue): Queue on which the agents' messages will be saved
            client_sent_queue (asyncio.Queue): Queue on which the user's messages will be read from
        """
        self.__agents = [
            self.group_chat_proxy,
            self.__summary_agent,
            self.__email_writer_agent,
            self.__evaluator_agent,
            self.__email_sender_agent,
            self.__execute_email,
        ]

        self.__disallowed_speaker_transitions_dict = {
            self.group_chat_proxy: [
                self.__email_sender_agent,
                self.__email_writer_agent,
                self.group_chat_proxy,
                self.__execute_email,
                self.__evaluator_agent,
            ],
            self.__summary_agent: [
                self.__summary_agent,
                self.group_chat_proxy,
                self.__evaluator_agent,
                self.__email_sender_agent,
                self.__execute_email,
            ],
            self.__email_writer_agent: [
                self.__email_writer_agent,
                self.__summary_agent,
                self.group_chat_proxy,
                self.__email_sender_agent,
                self.__execute_email,
            ],
            self.__evaluator_agent: [
                self.__evaluator_agent,
                self.__execute_email,
                self.__summary_agent,
                self.group_chat_proxy,
            ],
            self.__email_sender_agent: [
                self.__email_sender_agent,
                self.__evaluator_agent,
                self.__email_writer_agent,
                self.__summary_agent,
                self.group_chat_proxy,
            ],
            self.__execute_email: [
                self.__execute_email,
                self.__email_sender_agent,
                self.__evaluator_agent,
                self.__email_writer_agent,
                self.__summary_agent,
                self.group_chat_proxy,
            ],
        }

        self.__draft_email_group_chat = GroupChat(
            agents=self.__agents,
            allowed_or_disallowed_speaker_transitions=self.__disallowed_speaker_transitions_dict,
            speaker_transitions_type=DISALLOWED,
            messages=[],
            max_round=12,
            send_introductions=True,
        )

        self.group_chat_manager = GroupChatManagerWithAsyncQueue(
            name="draft_email_group_chat_manager",
            groupchat=self.__draft_email_group_chat,
            llm_config=self.__llm_config,
            description="\n".join(self.__config["draft_email_group_chat_manager"][DESC]),
        )
        self.group_chat_manager.set_queues(client_receive_queue, client_sent_queue)

    def __register_functions(self) -> None:
        """Register Functions."""
        register_function(
            send_mail,
            caller=self.__email_sender_agent,
            executor=self.__execute_email,
            name="send_mail",
            description="send emails",
        )

    def get_manager(self) -> GroupChatManagerWithAsyncQueue:
        """
        Retrieve the GroupChatWebManager.

        Returns:
            GroupChatManagerWithAsyncQueue: the group chat manager of the underlying group chat
        """
        return self.group_chat_manager

    def get_proxy(self) -> ConversableAgentWithAsyncQueue:
        """
        Retrieve the proxy of the underlying group chat.

        Returns:
            ConversableAgentWithAsyncQueue: the proxy of the underlying group chat
        """
        return self.group_chat_proxy
