# -*- coding: utf-8 -*-
"""
Pytest for autogen_translator route.

Description: Tests the autogen_translator route.

Authors: Max Belitsky, Alexandre Carlhammar
"""

import asyncio
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.server import app
from dev.app.routes.autogen_mail_generator.autogen_mail_generator_router import (
    get_email_generation, get_email_generation_result)
from dev.app.routes.autogen_translator.autogen_integration.const import \
    MESSAGE_SENT
from dev.app.routes.autogen_translator.autogen_integration.group_chats.mail_generation.ngc_mail_generation import \
    EmailNGC

client = TestClient(app)


summary: str = "The main point of the text is that someone has discovered one million dollars in the street."

email_draft_1: str = "\n".join(
    [
        "\n\n".join(
            [
                "Dear IBMer,",
                "We have had certain unusual developments around us. In an unexpected turn of events, **someone has surprisingly found a whopping one million dollars out in the street**.",
                "By all accounts, such occurrences do not occur in the usual pattern of our daily lives. Just imagine finding a million dollars. It's surreal.",
                "The situation raises some intriguing and important considerations about chance, fortune, and society. This can serve as an interesting area for contemplative discussions or debates that can engage our IBM community."
                "Isn't it incredible how the ordinary, the mundane can turn extraordinary in a split second? A regular stroll down the street turned into a life-changing moment.",
                "Let's keep our eyes open because who knows what fortune might be lying in plain sight, waiting to be discovered!",
                "Feel free to share your views about this unusual event, and let’s spark some interesting conversation around it.",
                "Best Wishes,",
            ]
        ),
        "IBM Consulting Assistant",
    ]
)

evaluator_draft_1: str = "\n\n".join(
    [
        "The email draft is overall well-written, professional, and accurate. I would however recommend adjusting a couple of areas. ",
        "1. In the beginning of the email, having the wording as 'we' gives the impression that the discovery of the money was an internal IBM event. Instead, maintain a more neutral tone by indicating that this occurrence happened publicly.",
        "2. The body of the email should be more formal. The tone is slightly too casual. Instead of using terms such as "
        "Just imagine finding a million dollars. It's surreal."
        ", establish a more professional tone.",
        "3. The ending of the email is encouraging discussions and views about the unusual event. However, it might not be clear who or where these views are to be shared. Thus it would be useful to include clear instructions or point of contact for further discussions.",
        "Furthermore, I would recommend adding a title to the start of the email. For instance, "
        "Unexpected Discoveries: One Million Dollars Found in the Street"
        ". This would immediately draw attention to the key point of the newsletter. ",
    ]
)

email_draft_2: str = "\n".join(
    [
        "\n\n".join(
            [
                "Dear IBMer,",
                "**Subject: Unexpected Discoveries: One Million Dollars Found in the Street**",
                "We are reaching out to share an intriguing bit of news that has caught our attention. In a rather extraordinary occurrence in the public sphere, **someone has stumbled upon a staggering sum of one million dollars simply lying unattended on a city street**.",
                "These kind of incidents often stir numerous discussions, considerations, and theorizations about fate, luck, and societal norms. We as a team at IBM are no strangers to engaging in complex discussions, and this seemingly straightforward event of a random street discovery provides ample grist for the intellectual mill.",
                "Life continues to surprise us on numerous occasions. Seeing an everyday event transform into an unusual situation raises many fascinating questions. What would one do when faced with such a sudden windfall? How would this impact their life? The questions are as endless as they are interesting.",
                "We invite you to share your thoughts on this unusual event. Please feel free to direct your responses to our IBM community forum, where we hope bring about a lively, thought-provoking discussion.",
                "We can't wait to hear your inputs and ideas!",
                "Best Wishes,",
            ]
        ),
        "IBM Consulting Assistant",
    ]
)

evaluator_draft_2: str = "\n\n".join(
    [
        "The corrections and recommendations have been well implemented in the revised draft. The email now comes across as more professional and maintains accuracy in detailing the information. It provides a clear call to action for IBMer's to participate in the discussion at the IBM community forum, and signing off the email is also appropriately done. The email is now complete and up to the mark.",
        "TASK IS DONE.",
    ]
)


@pytest.mark.asyncio
async def test_get_email_generation_result():
    """Test the get_email_generation_result function."""
    message_queue = asyncio.Queue()
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "summary_agent", "content": summary},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "email_writer_agent", "content": email_draft_1},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "evaluator_agent", "content": evaluator_draft_1},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "email_writer_agent", "content": email_draft_2},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "evaluator_agent", "content": evaluator_draft_2},
        }
    )
    await message_queue.put(
        {
            "status": MESSAGE_SENT,
            "message": {"name": "email_evaluator_agent", "content": email_draft_2},
        }
    )

    email_generation, chat_history = get_email_generation_result(message_queue)

    assert email_generation == email_draft_2
    assert len(chat_history) == 6
    assert chat_history[0] == {
        "status": MESSAGE_SENT,
        "message": {"name": "summary_agent", "content": summary},
    }
    assert chat_history[1] == {
        "status": MESSAGE_SENT,
        "message": {"name": "email_writer_agent", "content": email_draft_1},
    }
    assert chat_history[2] == {
        "status": MESSAGE_SENT,
        "message": {"name": "evaluator_agent", "content": evaluator_draft_1},
    }
    assert chat_history[3] == {
        "status": MESSAGE_SENT,
        "message": {"name": "email_writer_agent", "content": email_draft_2},
    }
    assert chat_history[4] == {
        "status": MESSAGE_SENT,
        "message": {"name": "evaluator_agent", "content": evaluator_draft_2},
    }


@patch("dev.app.routes.autogen_mail_generator.autogen_mail_generator_router.get_email_generation")
def test_autogen_mail_generator_endpoint(mocked_get_email_generation):
    # Define test data
    correct_input = {
        "text": "Someone found 1 million dollars in the street.",
        "recipientEmailAddress": "newsletter.members@example.com",
    }
    incorrect_input = test_input = {
        "query": "Write an email about someone who found 1 million dollars in the street to newsletter.members@example.com"
    }
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    # Mock get_text_translation to avoid calling autogen
    mocked_get_email_generation.return_value = evaluator_draft_2, []

    # Make the requests and assert
    correct_response = client.post("/autogen_mail_generator/result", json=correct_input, headers=headers)
    incorrect_response = client.post("/autogen_mail_generator/result", json=incorrect_input, headers=headers)

    assert correct_response.status_code == 200
    assert incorrect_response.status_code == 422


class MockEmailGenerationnProxy:
    def __init__(self, receive_queue: asyncio.Queue):
        self.receive_queue = receive_queue

    async def a_initiate_chat(self, *args, **kwargs):
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {"name": "summary_agent", "content": summary},
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {"name": "email_writer_agent", "content": email_draft_1},
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {"name": "evaluator_agent", "content": evaluator_draft_1},
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {"name": "email_writer_agent", "content": email_draft_1},
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {"name": "evaluator_agent", "content": evaluator_draft_2},
            }
        )
        await self.receive_queue.put(
            {
                "status": MESSAGE_SENT,
                "message": {"name": "email_evaluator_agent", "content": email_draft_2},
            }
        )


class MockEmailGenerationNGC:
    def __init__(self, receive_queue: asyncio.Queue, sent_queue: asyncio.Queue):
        self.receive_queue = receive_queue
        self.sent_queue = sent_queue

    def get_manager(self):
        return None

    def get_proxy(self) -> MockEmailGenerationnProxy:
        return MockEmailGenerationnProxy(self.receive_queue)


@pytest.mark.asyncio
@patch.object(EmailNGC, "__init__", MockEmailGenerationNGC.__init__)
@patch.object(EmailNGC, "get_manager", MockEmailGenerationNGC.get_manager)
@patch.object(EmailNGC, "get_proxy", MockEmailGenerationNGC.get_proxy)
async def test_get_email_generation():
    mail_generated, chat_history = await get_email_generation(
        "Someone found 1 million dollars in the street.",
        "newsletter.members@example.com",
    )

    assert mail_generated == email_draft_2
    assert len(chat_history) == 6
