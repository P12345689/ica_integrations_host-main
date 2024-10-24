# -*- coding: utf-8 -*-
import json
import os

import aiohttp
import chainlit as cl

# Read the .env file
api_url = os.environ.get("AGENT_API_URL", "http://localhost:8080/agent_langchain/invoke")
api_key = os.environ.get("AGENT_API_KEY", "dev-only-token")


@cl.step
async def send_request(session, message):
    return await session.post(api_url, json={"query": message}, headers={"Integrations-API-Key": api_key})


@cl.step
async def process_response_line(line):
    if line.strip():
        return json.loads(line.decode("utf-8"))
    return None


@cl.step
async def display_event(event):
    event.get("invocation_id")
    event.get("event_id")
    is_final_event = event.get("is_final_event", False)
    response = event.get("response", [{}])[0].get("message", {})

    if is_final_event:
        content = response.get("content", "")
        await cl.Message(content=content).send()
    else:
        elements = []
        message_type = response.get("type")

        if message_type == "thought":
            elements.append(
                cl.Text(
                    content=f"💭 {response.get('title', 'Agent Thought')}: {response.get('content', '')}",
                    color="blue",
                )
            )
        elif message_type == "action":
            elements.append(
                cl.Text(
                    content=f"🎬 {response.get('title', 'Planned Action')}: {response.get('content', '')}",
                    color="green",
                )
            )
        elif message_type == "observation":
            elements.append(
                cl.Text(
                    content=f"👁️ {response.get('title', 'Observation')}: {response.get('content', '')}",
                    color="purple",
                )
            )
        elif message_type == "custom":
            elements.append(
                cl.Text(
                    content=f"🐻 {response.get('title', 'Custom')}: {response.get('content', '')}",
                    color="orange",
                )
            )

        if elements:
            await cl.Message(content="", elements=elements).send()


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    async with aiohttp.ClientSession() as session:
        response = await send_request(session, message.content)
        async for line in response.content:
            processed_event = await process_response_line(line)
            if processed_event:
                await display_event(processed_event)

    await msg.update()


if __name__ == "__main__":
    cl.run()
