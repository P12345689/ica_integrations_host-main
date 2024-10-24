# -*- coding: utf-8 -*-
"""
Pytest for autogen_translator route.

Description: Tests the autogen_translator route.

Authors: Max Belitsky
"""

import asyncio
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.server import app
from dev.app.routes.autogen_translator.autogen_integration.const import \
    MESSAGE_SENT
from dev.app.routes.autogen_translator.autogen_integration.group_chats.translation.ngc_translation import \
    TranslationNGC
from dev.app.routes.autogen_translator.autogen_translator_router import (
    get_text_translation, get_translation_result)

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_translation_result():
    """Test the get_translation_result function."""
    message_queue = asyncio.Queue()
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "translator", "content": "My favorite color is blue."},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {
                "name": "critic",
                "content": "This translation does not need any changes. It's already good.",
            },
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {
                "name": "translator_with_critic",
                "content": "My favorite color is blue.",
            },
        }
    )

    translation, chat_history = get_translation_result(message_queue)

    assert translation == "My favorite color is blue."
    assert len(chat_history) == 3
    assert chat_history[0] == {
        "status": MESSAGE_SENT,
        "message": {"name": "translator", "content": "My favorite color is blue."},
    }
    assert chat_history[1] == {
        "status": MESSAGE_SENT,
        "message": {
            "name": "critic",
            "content": "This translation does not need any changes. It's already good.",
        },
    }
    assert chat_history[2] == {
        "status": MESSAGE_SENT,
        "message": {
            "name": "translator_with_critic",
            "content": "My favorite color is blue.",
        },
    }


@patch("dev.app.routes.autogen_translator.autogen_translator_router.get_text_translation")
def test_autogen_translator_endpoint(mocked_get_text_translation):
    # Define test data
    correct_input = {
        "text": "Meine Lieblingsfarbe ist blau.",
        "languageFrom": "German",
        "languageTo": "English",
    }
    incorrect_input = test_input = {"query": "Translate Meine Lieblingsfarbe ist blau from German to English."}
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    # Mock get_text_translation to avoid calling autogen
    mocked_get_text_translation.return_value = "My favorite color is blue.", []

    # Make the requests and assert
    correct_response = client.post("/autogen_translator/result", json=correct_input, headers=headers)
    incorrect_response = client.post("/autogen_translator/result", json=incorrect_input, headers=headers)

    assert correct_response.status_code == 200
    assert incorrect_response.status_code == 422


class MockTranslationProxy:
    def __init__(self, receive_queue: asyncio.Queue):
        self.receive_queue = receive_queue

    async def a_initiate_chat(self, *args, **kwargs):
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {
                    "name": "translator",
                    "content": "My favorite color is blue.",
                },
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {
                    "name": "critic",
                    "content": "This translation does not need any changes. It's already good.",
                },
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {
                    "name": "translator_with_critic",
                    "content": "My favorite color is blue.",
                },
            }
        )


class MockTranslationNGC:
    def __init__(self, receive_queue: asyncio.Queue, sent_queue: asyncio.Queue):
        self.receive_queue = receive_queue
        self.sent_queue = sent_queue

    def get_manager(self):
        return None

    def get_proxy(self) -> MockTranslationProxy:
        return MockTranslationProxy(self.receive_queue)


@pytest.mark.asyncio
@patch.object(TranslationNGC, "__init__", MockTranslationNGC.__init__)
@patch.object(TranslationNGC, "get_manager", MockTranslationNGC.get_manager)
@patch.object(TranslationNGC, "get_proxy", MockTranslationNGC.get_proxy)
async def test_get_text_translation():
    text_translated, chat_history = await get_text_translation("Meine Lieblingsfarbe ist blau", "German", "English")

    assert text_translated == "My favorite color is blue."
    assert len(chat_history) == 3
