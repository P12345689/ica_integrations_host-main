# -*- coding: utf-8 -*-
"""
Author: Dennis Weiss, Stan Furrer
Description: Translation Nested Group Chat
"""

import asyncio
import json
import os
from typing import Any, Dict

from autogen import GroupChat

from dev.app.routes.autogen_translator.autogen_integration.const import (
    ALLOWED, DESC, NEVER, OPENAI_API_VERSION, SYS_MSG)
from dev.app.routes.autogen_translator.autogen_integration.web.conversable_agent_with_async_queue import \
    ConversableAgentWithAsyncQueue
from dev.app.routes.autogen_translator.autogen_integration.web.group_chat_manager_with_async_queue import \
    GroupChatManagerWithAsyncQueue


class TranslationNGC:
    """
    Class that contains the agents that are setup in an autogen group chat.

    The configuration is loaded automatically from the jinja templates
    It is necessary to call set_queues to populate the asyncio queues used for async input and output of messages.
    """

    def __init__(self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue):
        """Initialize Translation Nested Group Chat."""
        agents_config = self.__load_agents_config()
        self.__config = agents_config["ngc_translation"]
        self.__llm_config = {
            "model": os.environ["AUTOGEN_TRANSLATOR_AZURE_OPENAI_DEPLOYMENT"],
            "api_key": os.environ["AUTOGEN_TRANSLATOR_AZURE_OPENAI_API_KEY"],
            "api_type": "azure",
            "base_url": os.environ["AUTOGEN_TRANSLATOR_AZURE_OPENAI_ENDPOINT"],
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
        self.__translator = ConversableAgentWithAsyncQueue(
            name="translator",
            system_message=self.__config["translator"][SYS_MSG],
            description=self.__config["translator"][DESC],
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
        )
        self.__translator.set_queues(client_receive_queue, client_sent_queue)

        self.__critic = ConversableAgentWithAsyncQueue(
            name="critic",
            system_message=self.__config["critic"][SYS_MSG],
            description=self.__config["critic"][DESC],
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
        )
        self.__critic.set_queues(client_receive_queue, client_sent_queue)

        self.__translator_with_critic = ConversableAgentWithAsyncQueue(
            name="translator_with_critic",
            system_message=self.__config["translator_with_critic"][SYS_MSG],
            description=self.__config["translator_with_critic"][DESC],
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
        )
        self.__translator_with_critic.set_queues(client_receive_queue, client_sent_queue)

        self.group_chat_proxy = ConversableAgentWithAsyncQueue(
            name="translation_group_chat_proxy",
            human_input_mode=NEVER,
            is_termination_msg=lambda msg: msg["name"] == self.__translator_with_critic.name,
        )
        self.group_chat_proxy.set_queues(client_receive_queue, client_sent_queue)

    def __setup_group_chat(self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue) -> None:
        """
        Set up the group chat.

        Args:
            client_receive_queue (asyncio.Queue): Queue on which the agents' messages will be saved
            client_sent_queue (asyncio.Queue): Queue on which the user's messages will be read from
        """
        self.__allowed_speaker_transitions_dict = {
            self.group_chat_proxy: [self.__translator],
            self.__translator: [self.__critic],
            self.__critic: [self.__translator_with_critic],
            self.__translator_with_critic: [self.group_chat_proxy],
        }

        self.__agents = [
            self.__translator,
            self.__critic,
            self.__translator_with_critic,
            self.group_chat_proxy,
        ]

        self.__translation_group_chat = GroupChat(
            agents=self.__agents,
            messages=[],
            allowed_or_disallowed_speaker_transitions=self.__allowed_speaker_transitions_dict,
            max_round=5,
            speaker_transitions_type=ALLOWED,
        )

        self.group_chat_manager = GroupChatManagerWithAsyncQueue(
            name="translation_group_chat_manager",
            groupchat=self.__translation_group_chat,
            llm_config=self.__llm_config,
            description=self.__config["translation_group_chat_manager"][DESC],
        )
        self.group_chat_manager.set_queues(client_receive_queue, client_sent_queue)

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
