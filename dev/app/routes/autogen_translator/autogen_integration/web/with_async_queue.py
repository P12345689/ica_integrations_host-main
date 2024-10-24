# -*- coding: utf-8 -*-
"""Class definition of WithAsyncQueue."""

import asyncio
from typing import Any, Dict, List, Optional, Tuple, Union

from autogen import Agent

from dev.app.routes.autogen_translator.autogen_integration.const import \
    MESSAGE_SENT


class WithAsyncQueue:
    """Provide the functionality to store received messages on a queue."""

    client_receive_queue: asyncio.Queue
    client_sent_queue: asyncio.Queue

    async def _a_populate_reply(
        self,
        messages: List[Dict],
        sender: Agent,
        config: Optional[Any] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        """
        Will be called each time this agent receives a message.

        It will populate the client_receive_queue with the message and information about the sender

        Args:
            messages (List[Dict]): The chat history
            sender (Agent): The sender of the current message
            config (Any): Configuration

        Returns:
            bool: Indicates the completion of the chat
            Union[str, Dict, None]: Chat history
        """
        message = messages[-1]

        reply = {"status": MESSAGE_SENT, "sender": sender.name, "receiver": self.name, "message": message}  # type: ignore
        await self.client_receive_queue.put(reply)

        return False, None

    def set_queues(self, client_receive_queue: asyncio.Queue, client_sent_queue: asyncio.Queue) -> None:
        """
        Initialize the asyncio queues.

        Args:
            client_receive_queue (asyncio.Queue): Queue on which the agents' messages will be saved
            client_sent_queue (asyncio.Queue): Queue on which the user's messages will be read from
        """
        self.client_receive_queue = client_receive_queue
        self.client_sent_queue = client_sent_queue
