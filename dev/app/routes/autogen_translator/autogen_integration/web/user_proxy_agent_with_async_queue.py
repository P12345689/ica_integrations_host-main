# -*- coding: utf-8 -*-
"""Class definition of UserProxyAgentWithAsyncQueue."""

import asyncio
from typing import Any, Dict, List, Optional, Tuple, Union

from autogen import Agent, ConversableAgent, UserProxyAgent
from termcolor import colored

from dev.app.routes.autogen_translator.autogen_integration.const import \
    WAIT_FOR_USER
from dev.app.routes.autogen_translator.autogen_integration.web.with_async_queue import \
    WithAsyncQueue


class UserProxyAgentWithAsyncQueue(WithAsyncQueue, UserProxyAgent):
    """Class that inherits autogen's UserProxyAgent to provide async messaging functionality via asyncio queues."""

    client_receive_queue: asyncio.Queue
    client_sent_queue: asyncio.Queue

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize UserProxyAgentWithAsyncQueue."""
        super().__init__(*args, **kwargs)
        self._reply_func_list: List = []
        self.register_reply([Agent, None], ConversableAgent.generate_oai_reply)
        self.register_reply([Agent, None], ConversableAgent.generate_code_execution_reply)
        self.register_reply([Agent, None], ConversableAgent.generate_function_call_reply)
        self.register_reply(
            [Agent, None],
            UserProxyAgentWithAsyncQueue.a_check_termination_and_human_reply,
        )
        self.register_reply([Agent, None], WithAsyncQueue._a_populate_reply)

    async def a_check_termination_and_human_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[Any] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        """
        Check if the conversation should be terminated, and if human reply is provided.

        Args:
            messages (List[Dict]): Chat history
            sender (Agent): Sender of the current message
            config (Any): Configuration

        Returns:
            bool: Indicates the completion of the chat
            Union[str, Dict, None]: Chat history
        """
        if config is None:
            config = self
        if messages is None:
            messages = self._oai_messages[sender]
        message = messages[-1]
        reply = ""
        no_human_input_msg = ""
        sender_name = sender.name  # type: ignore
        if self.human_input_mode == "ALWAYS":
            reply = await self.a_get_human_input(
                f"Provide feedback to {sender_name}. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: "
            )
            no_human_input_msg = "NO HUMAN INPUT RECEIVED." if not reply else ""
            # if the human input is empty, and the message is a termination message, then we will terminate the conversation
            reply = reply if reply or not self._is_termination_msg(message) else "exit"
        else:
            if self._consecutive_auto_reply_counter[sender] >= self._max_consecutive_auto_reply_dict[sender]:
                if self.human_input_mode == "NEVER":
                    reply = "exit"
                else:
                    # self.human_input_mode == "TERMINATE":
                    terminate = self._is_termination_msg(message)
                    reply = await self.a_get_human_input(
                        f"Please give feedback to {sender_name}. Press enter or type 'exit' to stop the conversation: "
                        if terminate
                        else f"Please give feedback to {sender_name}. Press enter to skip and use auto-reply, or type 'exit' to stop the conversation: "
                    )
                    no_human_input_msg = "NO HUMAN INPUT RECEIVED." if not reply else ""
                    # if the human input is empty, and the message is a termination message, then we will terminate the conversation
                    reply = reply if reply or not terminate else "exit"
            elif self._is_termination_msg(message):
                if self.human_input_mode == "NEVER":
                    reply = "exit"
                else:
                    # self.human_input_mode == "TERMINATE":
                    reply = await self.a_get_human_input(
                        f"Please give feedback to {sender_name}. Press enter or type 'exit' to stop the conversation: "
                    )
                    no_human_input_msg = "NO HUMAN INPUT RECEIVED." if not reply else ""
                    # if the human input is empty, and the message is a termination message, then we will terminate the conversation
                    reply = reply or "exit"

        # print the no_human_input_msg
        if no_human_input_msg:
            print(colored(f"\n>>>>>>>> {no_human_input_msg}", "red"), flush=True)

        # stop the conversation
        if reply == "exit":
            # reset the consecutive_auto_reply_counter
            self._consecutive_auto_reply_counter[sender] = 0
            return True, None

        # send the human reply
        if reply or self._max_consecutive_auto_reply_dict[sender] == 0:
            # reset the consecutive_auto_reply_counter
            self._consecutive_auto_reply_counter[sender] = 0
            return True, reply

        # increment the consecutive_auto_reply_counter
        self._consecutive_auto_reply_counter[sender] += 1
        if self.human_input_mode != "NEVER":
            print(colored("\n>>>>>>>> USING AUTO REPLY...", "red"), flush=True)

        return False, None

    async def a_get_human_input(self, prompt: str) -> str:
        """
        Inherits autogen's method.

        Instead of waiting for console input it will read from the client_sent_queue and send the first element of the
        queue to autogen.

        Args:
            prompt (str): Message received

        Returns:
            str: Message to send back to autogen
        """
        await self.client_receive_queue.put({"status": WAIT_FOR_USER})
        reply = await self.client_sent_queue.get()
        if reply and reply == "DO_FINISH":
            return "exit"
        return reply
