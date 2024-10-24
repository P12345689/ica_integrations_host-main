# -*- coding: utf-8 -*-
import asyncio
import os
from typing import Any, Dict

import autogen
from autogen.agentchat import GroupChat, register_function
from autogen.agentchat.contrib.web_surfer import WebSurferAgent  # noqa: E402
from jinja2 import Environment, FileSystemLoader

from dev.app.routes.autogen_translator.autogen_integration.const import (
    ALLOWED, NEVER, OPENAI_API_VERSION, VIEWPORTAL_SIZE)
from dev.app.routes.autogen_translator.autogen_integration.web.conversable_agent_with_async_queue import \
    ConversableAgentWithAsyncQueue
from dev.app.routes.autogen_translator.autogen_integration.web.group_chat_manager_with_async_queue import \
    GroupChatManagerWithAsyncQueue

BING_API_KEY = os.getenv("AUTOGEN_WEBSCRAPER_BING_API_KEY")


def scrape_page(**kwargs: Dict[str, Any]) -> str:
    """
    Scrape multiple URLs provided in the kwargs dictionary  and return the scraped content.
    :param kwargs: Dictionary containing headlines and their URLs.
    :type kwargs: dict
    :return: A dictionary with headlines as keys and their summaries as values.
    :rtype: dict
    """
    headlines = kwargs.get("Headlines", {})

    # Configuration for the language model (LLM)
    llm_config = {
        "model": os.environ["AUTOGEN_WEBSCRAPER_AZURE_OPENAI_DEPLOYMENT"],
        "api_key": os.environ["AUTOGEN_WEBSCRAPER_AZURE_OPENAI_API_KEY"],
        "api_type": "azure",
        "base_url": os.environ["AUTOGEN_WEBSCRAPER_AZURE_OPENAI_ENDPOINT"],
        "api_version": OPENAI_API_VERSION,
    }

    summarizer_llm_config = {
        "api_key": os.environ["AUTOGEN_WEBSCRAPER_SUMMARIZER_AZURE_OPENAI_API_KEY"],
        "timeout": 600,
        "cache_seed": 44,
        "config_list": [
            {
                "model": os.environ["AUTOGEN_WEBSCRAPER_SUMMARIZER_AZURE_OPENAI_DEPLOYMENT"],
                "api_key": os.environ["AUTOGEN_WEBSCRAPER_SUMMARIZER_AZURE_OPENAI_API_KEY"],
                "api_type": "azure",
                "base_url": os.environ["AUTOGEN_WEBSCRAPER_SUMMARIZER_AZURE_OPENAI_ENDPOINT"],
                "api_version": OPENAI_API_VERSION,
            }
        ],
        "temperature": 0,
    }
    summary_collection = {}

    user_proxy = autogen.UserProxyAgent(
        "user_proxy",
        human_input_mode=NEVER,
        code_execution_config=False,
        default_auto_reply="",
        is_termination_msg=lambda x: True,
    )

    web_surfer = WebSurferAgent(
        "web_surfer",
        llm_config=llm_config,
        summarizer_llm_config=summarizer_llm_config,
        browser_config={"viewport_size": VIEWPORTAL_SIZE, "bing_api_key": BING_API_KEY},
    )

    for headline, url in headlines.items():
        task1 = f"Go to {url}"
        task2 = "Extract the positive and/or negative impact on the industry as summary of the news article"

        user_proxy.initiate_chat(web_surfer, message=task1, clear_history=True)
        results = user_proxy.initiate_chat(web_surfer, message=task2, clear_history=False)
        summary_collection[headline] = [url, results.summary]

    formatted_output = ""
    for title, details in summary_collection.items():
        url, content = details
        formatted_output += f"**{title}**\n"
        sentences = content.split(". ")
        formatted_output += f"{sentences[0]}. {sentences[1]}. {sentences[2]}. [Read more]({url})\n\n"

    return formatted_output


class WebscrapingNGC:
    def __init__(
        self,
        client_receive_queue: asyncio.Queue,
        client_sent_queue: asyncio.Queue,
        industry: str,
    ) -> None:
        """
        Initialize the WebscrapingNGC class.
        """
        self.industry = industry

        # Load Jinja2 environment
        self.__template_env = Environment(
            loader=FileSystemLoader(
                "dev/app/routes/autogen_translator/autogen_integration/group_chats/webscraping/templates"
            )
        )

        self.__llm_config = {
            "model": os.environ["AUTOGEN_WEBSCRAPER_AZURE_OPENAI_DEPLOYMENT"],
            "api_key": os.environ["AUTOGEN_WEBSCRAPER_AZURE_OPENAI_API_KEY"],
            "api_type": "azure",
            "base_url": os.environ["AUTOGEN_WEBSCRAPER_AZURE_OPENAI_ENDPOINT"],
            "api_version": OPENAI_API_VERSION,
        }
        self.__setup_agents(client_receive_queue, client_sent_queue)
        self.__setup_group_chat(client_receive_queue, client_sent_queue)
        self.__register_functions()

    def __setup_agents(self, client_receive_queue, client_sent_queue) -> None:
        """
        Setup all the agents
        """
        self.__web_surfer = WebSurferAgent(
            name="websurfer",
            llm_config=self.__llm_config,
            summarizer_llm_config=False,
            browser_config={
                "viewport_size": VIEWPORTAL_SIZE,
                "bing_api_key": BING_API_KEY,
            },
        )

        self.__url_collector = ConversableAgentWithAsyncQueue(
            name="url_collector",
            llm_config=self.__llm_config,
            system_message=self.__template_env.get_template("url_collector_sys_msg.jinja").render(
                industry=self.industry
            ),
            human_input_mode=NEVER,
            description=self.__template_env.get_template("url_collector_description.jinja").render(
                industry=self.industry
            ),
        )
        self.__url_collector.set_queues(client_receive_queue, client_sent_queue)

        self.__scraper_agent = ConversableAgentWithAsyncQueue(
            name="web_scraper",
            llm_config=self.__llm_config,
            human_input_mode=NEVER,
            system_message=self.__template_env.get_template("web_scraper_sys_msg.jinja").render(),
            description=self.__template_env.get_template("web_scraper_description.jinja").render(),
        )
        self.__scraper_agent.set_queues(client_receive_queue, client_sent_queue)

        self.__scrape_executor_agent = ConversableAgentWithAsyncQueue(
            name="scrape_executor",
            llm_config=False,
            human_input_mode=NEVER,
            code_execution_config=False,
            is_termination_msg=lambda x: x.get("content", "") is not None and "terminate" in x["content"].lower(),
            default_auto_reply="Please continue if not finished, otherwise return 'TERMINATE'.",
        )
        self.__scrape_executor_agent.set_queues(client_receive_queue, client_sent_queue)

        self.__question_answerer_agent = ConversableAgentWithAsyncQueue(
            name="question_answerer",
            llm_config=self.__llm_config,
            system_message=self.__template_env.get_template("question_answerer_sys_msg.jinja").render(
                industry=self.industry
            ),
            human_input_mode=NEVER,
            description=self.__template_env.get_template("question_answerer_description.jinja").render(
                industry=self.industry
            ),
        )
        self.__question_answerer_agent.set_queues(client_receive_queue, client_sent_queue)

        self.group_chat_proxy = ConversableAgentWithAsyncQueue(
            name="webscraper_proxy",
            llm_config=False,
            human_input_mode=NEVER,
            description=self.__template_env.get_template("webscraper_proxy_description.jinja").render(),
            is_termination_msg=lambda msg: msg["name"] == self.__question_answerer_agent.name,
        )
        self.group_chat_proxy.set_queues(client_receive_queue, client_sent_queue)

    def __setup_group_chat(self, client_receive_queue, client_sent_queue) -> None:
        """
        Setup The Group Chat based on StateFlow
        """
        self.__agents = [
            self.__web_surfer,
            self.__url_collector,
            self.__scraper_agent,
            self.__scrape_executor_agent,
            self.__question_answerer_agent,
            self.group_chat_proxy,
        ]

        self.__allowed_speaker_transitions_dict = {
            self.group_chat_proxy: [self.__web_surfer],
            self.__web_surfer: [self.__url_collector],
            self.__url_collector: [self.__scraper_agent],
            self.__scraper_agent: [self.__scrape_executor_agent],
            self.__scrape_executor_agent: [self.__question_answerer_agent],
            self.__question_answerer_agent: [self.group_chat_proxy],
        }

        self.__scraping_group_chat = GroupChat(
            agents=self.__agents,
            messages=[],
            allowed_or_disallowed_speaker_transitions=self.__allowed_speaker_transitions_dict,
            speaker_transitions_type=ALLOWED,
        )

        self.group_chat_manager = GroupChatManagerWithAsyncQueue(
            name="scraping_group_chat_manager",
            groupchat=self.__scraping_group_chat,
            llm_config=self.__llm_config,
        )
        self.group_chat_manager.set_queues(client_receive_queue, client_sent_queue)

    def __register_functions(self) -> None:
        """
        Register Functions
        """
        register_function(
            scrape_page,
            caller=self.__scraper_agent,
            executor=self.__scrape_executor_agent,
            name="scrape_page",
            description="""
            This function scrapes multiple web pages to gather textual content based on a provided dictionary of Headlines,
            which contains headline titles as keys and their corresponding URLs as values. The scraped content is then summarized and returned.
            """,
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
