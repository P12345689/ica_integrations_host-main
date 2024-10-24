#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Simple chainlit example showing streaming events
"""

import chainlit as cl


@cl.step
def tool(message: str) -> str:
    return message


@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """

    # Call the tool
    tool(message=message.content)

    # Call the tool
    tool(message=message.content)

    # Send the final answer.
    await cl.Message(content="This is the final answer").send()
