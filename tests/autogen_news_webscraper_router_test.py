# -*- coding: utf-8 -*-
"""
Pytest for autogen_news_webscraper route.

Description: Tests the autogen_news_webscraper route.

Authors: Max Belitsky
"""

import asyncio
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.server import app
from dev.app.routes.autogen_news_webscraper.autogen_news_webscraper_router import (
    get_text_news_webscraping, get_webscraping_result)
from dev.app.routes.autogen_translator.autogen_integration.const import \
    MESSAGE_SENT
from dev.app.routes.autogen_translator.autogen_integration.group_chats.webscraping.ngc_webscraping import \
    WebscrapingNGC

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_webscraping_result_result():
    """Test the get_webscraping_result function."""
    message_queue = asyncio.Queue()
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "webscraper_proxy", "content": "Scrape the news."},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "websurfer", "content": "Websurfer results."},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "url_collector", "content": "URL Collector results."},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {
                "name": "question_answerer",
                "content": "Summary about industry.",
            },
        }
    )

    translation, chat_history = get_webscraping_result(message_queue)

    assert translation == "Summary about industry."
    assert len(chat_history) == 4
    assert chat_history[0] == {
        "status": MESSAGE_SENT,
        "message": {"name": "webscraper_proxy", "content": "Scrape the news."},
    }
    assert chat_history[1] == {
        "status": MESSAGE_SENT,
        "message": {"name": "websurfer", "content": "Websurfer results."},
    }
    assert chat_history[2] == {
        "status": MESSAGE_SENT,
        "message": {"name": "url_collector", "content": "URL Collector results."},
    }
    assert chat_history[3] == {
        "status": MESSAGE_SENT,
        "message": {"name": "question_answerer", "content": "Summary about industry."},
    }


@patch("dev.app.routes.autogen_news_webscraper.autogen_news_webscraper_router.get_text_news_webscraping")
def test_autogen_news_webscraper_endpoint(mocked_get_text_news_webscraping):
    # Define test data
    correct_input = {
        "industry": "Financial",
        "newsUrl": "https://www.swissinfo.ch/eng/bloomberg/",
    }
    incorrect_input = test_input = {
        "query": "Scrape news about Financial industry from https://www.swissinfo.ch/eng/bloomberg/."
    }
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    # Mock get_text_translation to avoid calling autogen
    mocked_get_text_news_webscraping.return_value = "Summary about industry.", []

    # Make the requests and assert
    correct_response = client.post("/autogen_news_webscraper/result", json=correct_input, headers=headers)
    incorrect_response = client.post("/autogen_news_webscraper/result", json=incorrect_input, headers=headers)

    assert correct_response.status_code == 200
    assert incorrect_response.status_code == 422


class MockWebscrapingProxy:
    def __init__(self, receive_queue: asyncio.Queue):
        self.receive_queue = receive_queue

    async def a_initiate_chat(self, *args, **kwargs):
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {"name": "webscraper_proxy", "content": "Scrape the news."},
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {"name": "websurfer", "content": "Websurfer results."},
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {
                    "name": "url_collector",
                    "content": "URL Collector results.",
                },
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {
                    "name": "question_answerer",
                    "content": "Summary about industry.",
                },
            }
        )


class MockWebscrapingNGC:
    def __init__(self, receive_queue: asyncio.Queue, sent_queue: asyncio.Queue, industry: str):
        self.receive_queue = receive_queue
        self.sent_queue = sent_queue
        self.industry = industry

    def get_manager(self):
        return None

    def get_proxy(self) -> MockWebscrapingProxy:
        return MockWebscrapingProxy(self.receive_queue)


@pytest.mark.asyncio
@patch.object(WebscrapingNGC, "__init__", MockWebscrapingNGC.__init__)
@patch.object(WebscrapingNGC, "get_manager", MockWebscrapingNGC.get_manager)
@patch.object(WebscrapingNGC, "get_proxy", MockWebscrapingNGC.get_proxy)
async def test_get_text_news_webscraping():
    news_webscraping_result, chat_history = await get_text_news_webscraping(
        "https://www.swissinfo.ch/eng/bloomberg/", "Financial"
    )

    assert news_webscraping_result == "Summary about industry."
    assert len(chat_history) == 4
