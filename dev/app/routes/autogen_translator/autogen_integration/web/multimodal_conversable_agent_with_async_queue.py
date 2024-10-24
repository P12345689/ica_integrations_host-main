# -*- coding: utf-8 -*-
"""Class definition of MultimodalConversableAgentWithAsyncQueue."""

from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from autogen import Agent
from autogen.agentchat.chat import a_initiate_chats
from autogen.agentchat.contrib.multimodal_conversable_agent import \
    MultimodalConversableAgent

from dev.app.routes.autogen_translator.autogen_integration.web.with_async_queue import \
    WithAsyncQueue


class MultimodalConversableAgentWithAsyncQueue(WithAsyncQueue, MultimodalConversableAgent):
    """
    Class that inherits autogen's MultimodalConversableAgent to provide async messaging functionality via asyncio
    queues.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize MultimodalConversableAgentWithAsyncQueue."""
        super().__init__(*args, **kwargs)
        self.register_reply([Agent, None], WithAsyncQueue._a_populate_reply)

    @staticmethod
    async def _a_summary_from_nested_chats(
        chat_queue: List[Dict[str, Any]],
        recipient: Agent,
        messages: List[Dict],
        sender: Agent,
        config: Any,
    ) -> Tuple[bool, Union[str, None]]:
        """
        Inherits autogen's method such that nested chats are registered asynchronously.

        Args:
            chat_queue (List[Dict[str, Any]]): Chat history
            recipient (Agent):
            messages (Union[str, Callable]): Chat messages of current nested chat
            sender (Agent): Sender of the current message
            config (Any): Configuration

        Returns:
            bool: Indicates the completion of the chat
            str: Summary of the last chat if any chats were initiated
        """
        last_msg = messages[-1].get("content")
        chat_to_run = []
        for i, c in enumerate(chat_queue):
            current_c = c.copy()
            if current_c.get("sender") is None:
                current_c["sender"] = recipient
            message = current_c.get("message")
            # If message is not provided in chat_queue, we by default use the last message from the original chat history as the first message in this nested chat (for the first chat in the chat queue).
            # NOTE: This setting is prone to change.
            if message is None and i == 0:
                message = last_msg
            if callable(message):
                message = message(recipient, messages, sender, config)
            # We only run chat that has a valid message. NOTE: This is prone to change dependin on applications.
            if message:
                current_c["message"] = message
                chat_to_run.append(current_c)
        if not chat_to_run:
            return True, None

        for chat in chat_to_run:
            chat["chat_id"] = 0
        try:
            res = await a_initiate_chats(chat_to_run)
        except Exception as e:
            print(e)
        print("Completed async chat")
        return True, res[list(res.keys())[-1]].summary if len(res.keys()) > 0 else ""

    def register_nested_chats(
        self,
        chat_queue: List[Dict[str, Any]],
        trigger: Union[Type[Agent], str, Agent, Callable[[Agent], bool], List],
        reply_func_from_nested_chats: Union[str, Callable] = "summary_from_nested_chats",
        position: int = 2,
        **kwargs: Any,
    ) -> None:
        """
        Inherits autogen's method to provide functionality to register nested chats.

        Args:
            chat_queue (List[Dict[str, Any]]): Chat history
            trigger (Union[Type[Agent], str, Agent, Callable[[Agent], bool], List]): Other agent who will trigger a nested chats if sending message to this agent
            reply_func_from_nested_chats (Union[str, Callable]): Function used to get summary/reply of nested chat
            position (int): Ref to `register_reply` for details. Default to 2. It means we first check the termination and human reply, then check the registered nested chat reply.
        """

        async def wrapped_reply_func(
            recipient: Agent,
            messages: List[Dict],
            sender: Optional[Agent] = None,
            config: Optional[Any] = None,
        ) -> Tuple[bool, Union[str, None]]:
            return await self._a_summary_from_nested_chats(chat_queue, recipient, messages, sender, config)

        self.register_reply(
            trigger,
            wrapped_reply_func,
            position,
            kwargs.get("config"),
            kwargs.get("reset_config"),
            ignore_async_in_sync_chat=kwargs.get("ignore_async_in_sync_chat"),
        )
