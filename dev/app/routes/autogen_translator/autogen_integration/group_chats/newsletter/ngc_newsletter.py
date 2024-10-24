# -*- coding: utf-8 -*-
"""
Author: Dennis Weiss, Stan Furrer
Description: Newsletter Nested Group Chat
"""

import asyncio
import json
import os
from typing import Any, Dict

from autogen import GroupChat

from dev.app.routes.autogen_translator.autogen_integration.const import (
    ALLOWED, DESC, NEVER, OPENAI_API_VERSION, SYS_MSG)
from dev.app.routes.autogen_translator.autogen_integration.group_chats.mail_generation.ngc_mail_generation import \
    EmailNGC
from dev.app.routes.autogen_translator.autogen_integration.group_chats.translation.ngc_translation import \
    TranslationNGC
from dev.app.routes.autogen_translator.autogen_integration.group_chats.webscraping.ngc_webscraping import \
    WebscrapingNGC
from dev.app.routes.autogen_translator.autogen_integration.web.conversable_agent_with_async_queue import \
    ConversableAgentWithAsyncQueue
from dev.app.routes.autogen_translator.autogen_integration.web.group_chat_manager_with_async_queue import \
    GroupChatManagerWithAsyncQueue


class NewsletterNGC:
    """
    Class that contains the agents that are setup in an autogen group chat.

    The configuration is loaded automatically from agents_config.json.
    It is necessary to call set_queues to populate the asyncio queues used for async input and output of messages.
    """

    def __init__(
        self,
        client_receive_queue: asyncio.Queue,
        client_sent_queue: asyncio.Queue,
        industry: str,
        recipient_email_address: str,
    ):
        """Initialize Newsletter Nested Group Chat."""
        self.industry = industry
        self.recipient_email_address = recipient_email_address

        agents_config = self.__load_agents_config()
        self.__config = agents_config["ngc_newsletter"]
        self.__llm_config = {
            "model": os.environ["AUTOGEN_NEWSLETTER_AZURE_OPENAI_DEPLOYMENT"],
            "api_key": os.environ["AUTOGEN_NEWSLETTER_AZURE_OPENAI_API_KEY"],
            "api_type": "azure",
            "base_url": os.environ["AUTOGEN_NEWSLETTER_AZURE_OPENAI_ENDPOINT"],
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
        webscraping = WebscrapingNGC(client_receive_queue, client_sent_queue, self.industry)
        self.__scraping_group_chat_manager = webscraping.get_manager()
        self.__webscraper_proxy = webscraping.get_proxy()

        email = EmailNGC(
            client_receive_queue,
            client_sent_queue,
            recipient_email_address=self.recipient_email_address,
        )
        self.__draft_email_group_chat_manager = email.get_manager()
        self.__email_proxy = email.get_proxy()

        translation = TranslationNGC(client_receive_queue, client_sent_queue)
        self.__translation_group_chat_manager = translation.get_manager()
        self.__translation_question_proxy = translation.get_proxy()

        self.group_chat_proxy = ConversableAgentWithAsyncQueue(
            name="newsletter_proxy",
            system_message=self.__config["newsletter_proxy"][SYS_MSG],
            description=self.__config["newsletter_proxy"][DESC],
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
            is_termination_msg=lambda msg: msg["name"] == self.__email_proxy.name,
        )
        self.group_chat_proxy.set_queues(client_receive_queue, client_sent_queue)

    def __setup_group_chat(self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue) -> None:
        """
        Set up the group chat.

        Args:
            client_receive_queue (asyncio.Queue): Queue on which the agents' messages will be saved
            client_sent_queue (asyncio.Queue): Queue on which the user's messages will be read from
        """
        self.allowed_speaker_transitions_dict = {
            self.group_chat_proxy: [self.__webscraper_proxy],
            self.__webscraper_proxy: [
                self.__translation_question_proxy,
                self.__email_proxy,
            ],
            self.__translation_question_proxy: [self.__email_proxy],
            self.__email_proxy: [self.group_chat_proxy],
        }

        self.agents = [
            self.__webscraper_proxy,
            self.__translation_question_proxy,
            self.__email_proxy,
            self.group_chat_proxy,
        ]

        self.__newsletter_group_chat = GroupChat(
            agents=self.agents,
            messages=[],
            allowed_or_disallowed_speaker_transitions=self.allowed_speaker_transitions_dict,
            speaker_transitions_type=ALLOWED,
            max_round=6,
        )

        self.group_chat_manager = GroupChatManagerWithAsyncQueue(
            name="newsletter_group_chat_manager",
            groupchat=self.__newsletter_group_chat,
            llm_config=self.__llm_config,
            description=self.__config["newsletter_group_chat_manager"][DESC],
        )
        self.group_chat_manager.set_queues(client_receive_queue, client_sent_queue)

        self.__webscraper_proxy.register_nested_chats(
            [
                {
                    "recipient": self.__scraping_group_chat_manager,
                    "message": lambda recipient, messages, sender, config: recipient.chat_messages_for_summary(sender)[
                        -1
                    ]["content"],
                    "summary_method": "last_msg",
                }
            ],
            trigger=self.group_chat_manager,
        )

        self.__translation_question_proxy.register_nested_chats(
            [
                {
                    "recipient": self.__translation_group_chat_manager,
                    "message": lambda recipient, messages, sender, config: recipient.chat_messages_for_summary(sender)[
                        -1
                    ]["content"],
                    "summary_method": "reflection_with_llm",
                }
            ],
            trigger=self.group_chat_manager,
        )

        self.__email_proxy.register_nested_chats(
            [
                {
                    "recipient": self.__draft_email_group_chat_manager,
                    "message": lambda recipient, messages, sender, config: recipient.chat_messages_for_summary(sender)[
                        -1
                    ]["content"],
                    "summary_method": "reflection_with_llm",
                }
            ],
            trigger=self.group_chat_manager,
        )

    def __register_functions(self) -> None:
        """Register functions."""
        return

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
