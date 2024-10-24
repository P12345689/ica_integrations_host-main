# -*- coding: utf-8 -*-
import base64
import re
import os

from langchain.agents import tool

MERMAID_API_URL = os.getenv("MERMAID_API_URL", "https://mermaid.ink")

@tool
def syntax_to_image(mermaid_syntax: str) -> str:
    """
    Generates a mermaid diagram image from mermaid syntax and returns a URL.

    Args:
        mermaid_syntax (str): The mermaid syntax string, which may contain code blocks.

    Returns:
        str: A URL linking to the generated mermaid diagram image.
    """
    # Get text between markers if any
    print(mermaid_syntax)
    demarked_text = get_text_between_markers(mermaid_syntax)
    print(demarked_text)

    # Convert to bytes
    graphbytes = demarked_text.encode("utf8")

    # Convert to base64
    base64_bytes = base64.b64encode(graphbytes)

    # Decode as ascii
    base64_string = base64_bytes.decode("ascii")

    # Generate the URL
    url = f"{MERMAID_API_URL}/img/{base64_string}"

    # Return the URL
    return url


def get_text_between_markers(text: str) -> str:
    """
    Extracts and returns the text between triple backtick markers.

    Args:
        text (str): The input text potentially containing triple backtick markers.

    Returns:
        str: The text found between the triple backtick markers. If no markers are found,
             returns the trimmed input text.
    """
    markers = r"```(.*?)```"
    matches = re.findall(markers, text, flags=re.DOTALL)
    if matches:
        return matches[0].replace("mermaid", "").strip()
    else:
        return text.strip()
