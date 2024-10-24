#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: A basic ollama CLI client (async) with streaming support.
"""

import asyncio
import json
import os
import sys
from argparse import ArgumentParser, Namespace

import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variable for the API URL with a default value
API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")


def parse_arguments() -> Namespace:
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: The namespace containing the command line arguments.

    Examples:
        >>> args = parse_arguments()
        Namespace(model='mistral', prompt='Describe AI in 5 words')
    """
    parser = ArgumentParser(description="Ollama Streaming API Client")
    parser.add_argument("--model", type=str, default="mistral", help="Model to use for generation")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to send to the model")
    return parser.parse_args()


async def send_request(model: str, prompt: str) -> None:
    """
    Sends an asynchronous request to the Ollama API and streams the response.

    Args:
        model (str): The model name.
        prompt (str): The prompt text to send.

    Examples:
        Run this function with asyncio to see the streamed responses:
        >>> asyncio.run(send_request('mistral', 'What is OpenShift, in 5 words'))
    """
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("POST", API_URL, json={"model": model, "prompt": prompt}) as response:
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        print(data["response"], end="")
                        if data.get("done", False):
                            break
        except json.JSONDecodeError:
            print("Received malformed JSON.", file=sys.stderr)
        except httpx.RequestError as e:
            print(f"An error occurred: {e}", file=sys.stderr)


async def main() -> None:
    """
    Main function to parse arguments and handle the streaming of responses.
    """
    args = parse_arguments()
    await send_request(args.model, args.prompt)


if __name__ == "__main__":
    asyncio.run(main())
