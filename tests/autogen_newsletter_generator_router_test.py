# -*- coding: utf-8 -*-
"""
Pytest for autogen_nwesletter_generator route.

Description: Tests the autogen_nwesletter_generator route.

Authors: Max Belitsky
"""

import asyncio
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.server import app
from dev.app.routes.autogen_newsletter_generator.autogen_newsletter_generator_router import (
    get_newsletter, get_newsletter_result)
from dev.app.routes.autogen_translator.autogen_integration.const import \
    MESSAGE_SENT
from dev.app.routes.autogen_translator.autogen_integration.group_chats.newsletter.ngc_newsletter import \
    NewsletterNGC

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_newsletter_result():
    """Test the get_email_generation_result function."""
    message_queue = asyncio.Queue()
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {
                "name": "evaluator_agent",
                "content": "Extract the latest news about pharmaceutical industry",
            },
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {
                "name": "email_writer_agent",
                "content": "The assistant drafted an email ...",
            },
        }
    )

    nwesletter, chat_history = get_newsletter_result(message_queue)

    assert nwesletter == "The assistant drafted an email ..."
    assert len(chat_history) == 2
    assert chat_history[0] == {
        "status": MESSAGE_SENT,
        "message": {
            "name": "evaluator_agent",
            "content": "Extract the latest news about pharmaceutical industry",
        },
    }
    assert chat_history[1] == {
        "status": MESSAGE_SENT,
        "message": {
            "name": "email_writer_agent",
            "content": "The assistant drafted an email ...",
        },
    }


@patch("dev.app.routes.autogen_newsletter_generator.autogen_newsletter_generator_router.get_newsletter")
def test_autogen_nwesletter_generator_endpoint(mocked_get_newsletter):
    # Define test data
    correct_input = {
        "language": "English",
        "newsUrl": "https://www.swissinfo.ch/eng/bloomberg/",
        "industry": "Pharmaceutical",
        "emailAddress": "newsletter.members@example.com",
    }
    incorrect_input = {"query": "Create a nwesletter about a pharmaceutical industry."}
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    # Mock get_text_translation to avoid calling autogen
    mocked_get_newsletter.return_value = "The assistant drafted an email ...", []

    # Make the requests and assert
    correct_response = client.post("/autogen_newsletter_generator/result", json=correct_input, headers=headers)
    incorrect_response = client.post("/autogen_newsletter_generator/result", json=incorrect_input, headers=headers)

    assert correct_response.status_code == 200
    assert incorrect_response.status_code == 422


class MockNwesletterGenerationnProxy:
    def __init__(self, receive_queue: asyncio.Queue):
        self.receive_queue = receive_queue

    async def a_initiate_chat(self, *args, **kwargs):
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {
                    "name": "evaluator_agent",
                    "content": "Extract the latest news about pharmaceutical industry",
                },
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {
                    "name": "email_writer_agent",
                    "content": "The assistant drafted an email ...",
                },
            }
        )


class MockNwesletterGenerationNGC:
    def __init__(
        self,
        receive_queue: asyncio.Queue,
        sent_queue: asyncio.Queue,
        industry: str,
        recipient_email_address: str,
    ):
        self.receive_queue = receive_queue
        self.sent_queue = sent_queue
        self.industry = industry

    def get_manager(self):
        return None

    def get_proxy(self) -> MockNwesletterGenerationnProxy:
        return MockNwesletterGenerationnProxy(self.receive_queue)


@pytest.mark.asyncio
@patch.object(NewsletterNGC, "__init__", MockNwesletterGenerationNGC.__init__)
@patch.object(NewsletterNGC, "get_manager", MockNwesletterGenerationNGC.get_manager)
@patch.object(NewsletterNGC, "get_proxy", MockNwesletterGenerationNGC.get_proxy)
async def test_get_newsletter():
    newsletter, chat_history = await get_newsletter(
        "English",
        "https://www.swissinfo.ch/eng/bloomberg/",
        "Pharmaceutical",
        "newsletter.members@example.com",
    )

    assert newsletter == "The assistant drafted an email ..."
    assert len(chat_history) == 2
