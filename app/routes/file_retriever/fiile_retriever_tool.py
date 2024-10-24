# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: File Retriever tool for use with langchain agents.

This module provides a tool for retrieving and converting files to text.

Example:
    >>> from langchain.agents import initialize_agent, Tool
    >>> from langchain.llms import OpenAI
    >>> llm = OpenAI(temperature=0)
    >>> tools = [Tool(name="FileRetriever", func=file_retriever, description="Useful for retrieving and converting files to text")]
    >>> agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    >>> agent.run("Retrieve and summarize the content of https://example.com/sample.pdf")
"""

import asyncio
from langchain.agents import tool
from file_retriever_router import fetch_file, convert_to_text

@tool
def file_retriever(url: str) -> str:
    """Retrieves a file from a URL and converts it to text.

    Args:
        url (str): The URL of the file to retrieve and convert.

    Returns:
        str: The text content of the file.

    Raises:
        Exception: If there's an error fetching or converting the file.
    """
    try:
        file_content = asyncio.run(fetch_file(url))
        file_extension = os.path.splitext(url)[1].lower()
        text_content = convert_to_text(file_content, file_extension)
        return text_content
    except Exception as e:
        return f"Error retrieving or converting file: {str(e)}"

if __name__ == "__main__":
    import doctest
    doctest.testmod()