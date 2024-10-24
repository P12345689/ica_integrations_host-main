#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: A basic ollama CLI client with streaming support.
"""

import json
import os
import sys
from argparse import ArgumentParser, Namespace

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")


def parse_arguments() -> Namespace:
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: The namespace containing the command line arguments.

    Example:
        >>> args = parse_arguments()
        Namespace(model='mistral', prompt='What is OpenShift, in 5 words')
    """
    parser = ArgumentParser(description="Ollama Streaming API Client")
    parser.add_argument("--model", type=str, default="mistral", help="Model to use for generation")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to send to the model")
    return parser.parse_args()


def send_request(model: str, prompt: str):
    """
    Sends a request to the Ollama API and streams the response.

    Args:
        model (str): The model name.
        prompt (str): The prompt text to send.

    Yields:
        str: Responses from the API.

    Example:
        >>> for response in send_request('mistral', 'What is OpenShift, in 5 words'):
        ...     print(response)
        Container
        ization
        platform
        for
        cloud
        applications
        .
    """
    payload = {"model": model, "prompt": prompt}
    with requests.post(API_URL, json=payload, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                yield data["response"]
                if data.get("done", False):
                    break


def main():
    args = parse_arguments()
    try:
        for response in send_request(args.model, args.prompt):
            print(response, end="")
    except requests.RequestException as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
