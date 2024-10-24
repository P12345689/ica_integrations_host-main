# -*- coding: utf-8 -*-
import os
import subprocess

# import nest_asyncio
from uuid import uuid4

from langchain.agents import tool

# this is necessary for async wrapping
# nest_asyncio.apply()

# Construct URLs
server_name = os.getenv(
    "SERVER_NAME",
    "http://localhost:8080",
)


@tool
async def generate_pptx(markdown: str, template_name: str):
    """Generates a powerpoint (pptx) from the given markdown and returns a url to the powerpoint"""
    return await generate_pptx_async(markdown)


@tool
async def generate_docx(markdown: str):
    """Generates a word document (docx) from the given markdown and returns a url to the document"""
    return await generate_docx_async(markdown)


async def generate_pptx_async(markdown: str, template_name: str = "templates/ibm_consulting_green.pptx"):
    """Generates a powerpoint (pptx) from the given markdown and returns a url to the powerpoint"""
    # Unique identifier for the document
    doc_id = uuid4().hex

    # Temporary file paths
    markdown_file_path = f"temp/{doc_id}.md"

    # set the document filepath
    pptx_file_path = f"public/documents/pptx/{doc_id}.pptx"

    # Write the Markdown content to a temporary file
    with open(markdown_file_path, "w") as markdown_file:
        markdown_file.write(markdown)

    # Generate .pptx (assuming the input is suitable for slides)
    # TODO: check True
    subprocess.run(
        [
            "pandoc",
            "-s",
            markdown_file_path,
            "--reference-doc",
            template_name,
            "-o",
            pptx_file_path,
            "--slide-level=2",
        ],
        check=False,
    )

    # Clean up the temporary Markdown file
    os.remove(markdown_file_path)

    # return the powerpoint
    return f"{server_name}/public/documents/pptx/{doc_id}.pptx"


async def generate_docx_async(markdown: str):
    """Generates a word document (docx) from the given markdown and returns a url to the document"""
    # Unique identifier for the document
    doc_id = uuid4().hex

    # Temporary file paths
    markdown_file_path = f"temp/{doc_id}.md"

    # set the document filepath
    docx_file_path = f"public/documents/docx/{doc_id}.docx"

    # Write the Markdown content to a temporary file
    with open(markdown_file_path, "w") as markdown_file:
        markdown_file.write(markdown)

    # Generate .docx
    subprocess.run(["pandoc", markdown_file_path, "-o", docx_file_path])

    # Clean up the temporary Markdown file
    os.remove(markdown_file_path)

    # return the document
    return f"{server_name}/public/documents/docx/{doc_id}.docx"
