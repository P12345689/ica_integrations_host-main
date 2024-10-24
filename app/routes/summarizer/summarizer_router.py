# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Summarization Integration Router

This module provides routes for summarizing long text using LangChain's various summarization methods. Supports:

1. Different summary types (bullets or paragraphs)
2. Various summary lengths (short, medium, long)
3. Output formats (plain text or Markdown)
4. Different styles (business or casual)
5. Additional instructions (e.g., translation)
6. Choice of summarization method (stuff, map_reduce, or refine)
7. Configurable language models (ChatConsultingAssistants, OpenAI, Ollama)
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Literal
from uuid import uuid4

from fastapi import FastAPI, Request
from jinja2 import Environment, FileSystemLoader
from langchain.base_language import BaseLanguageModel
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_consultingassistants import ChatConsultingAssistants
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

# LLM Configuration
LLM_TYPE = os.getenv("LLM_TYPE", "consulting_assistants")  # Options: consulting_assistants, openai, ollama
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 8b Instruct")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Other configuration
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_CONTEXT_LENGTH = int(os.getenv("DEFAULT_CONTEXT_LENGTH", 8192))
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", 0.7))
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", 6000))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", 200))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/summarizer/templates"))


class SummarizeInputModel(BaseModel):
    """Model to validate input data for text summarization."""

    text: str = Field(..., description="The long text to be summarized")
    max_tokens: int = Field(default=1024, description="Maximum number of tokens per chunk")
    summary_type: Literal["bullets", "paragraphs"] = Field(default="bullets", description="Type of summary output")
    summary_length: Literal["short", "medium", "long"] = Field(default="medium", description="Length of the summary")
    output_format: Literal["plain", "markdown"] = Field(default="plain", description="Output format of the summary")
    style: Literal["business", "casual"] = Field(default="business", description="Style of the summary")
    additional_instruction: str = Field(default="", description="Additional instruction for the summarizer")
    chain_type: Literal["stuff", "map_reduce", "refine"] = Field(default="map_reduce", description="Type of summarization chain to use")
    context_length: int = Field(default=DEFAULT_CONTEXT_LENGTH, description="Context length for the LLM")
    temperature: float = Field(default=DEFAULT_TEMPERATURE, description="Temperature for the LLM")
    chunk_size: int = Field(default=DEFAULT_CHUNK_SIZE, description="Size of text chunks for splitting")
    chunk_overlap: int = Field(default=DEFAULT_CHUNK_OVERLAP, description="Overlap size between text chunks")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_llm(model_name: str, temperature: float) -> BaseLanguageModel:
    """
    Initialize and return the specified language model.
    """
    if LLM_TYPE == "consulting_assistants":
        return ChatConsultingAssistants(model=model_name)
    elif LLM_TYPE == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")
        return ChatOpenAI(model_name=model_name, temperature=temperature)
    elif LLM_TYPE == "ollama":
        return Ollama(model=model_name, base_url=OLLAMA_BASE_URL)
    else:
        raise ValueError(f"Unsupported LLM type: {LLM_TYPE}")


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/experience/summarize/summarize_text/invoke")
    async def summarize_text(request: Request) -> OutputModel:
        """
        Handle POST requests to summarize long text using various LangChain methods.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Example:
            >>> from fastapi.testclient import TestClient
            >>> client = TestClient(app)
            >>> headers = { "Content-Type": "application/json", "Integrations-API-Key": "dev-only-token" }
            >>> response = client.post("/experience/summarize/summarize_text/invoke",
            ...     json={"text": "This is a long text to summarize...", "max_tokens": 1024,
            ...           "summary_type": "bullets", "summary_length": "short",
            ...           "output_format": "markdown", "style": "casual",
            ...           "additional_instruction": "Translate to Spanish",
            ...           "chain_type": "map_reduce", "context_length": 4096,
            ...           "temperature": 0.7, "chunk_size": 1000, "chunk_overlap": 200}, headers=headers)
            >>> assert response.status_code == 200
            >>> assert "invocationId" in response.json()
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = SummarizeInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"Invalid input: {str(e)}")],
            )

        try:
            # Initialize LangChain components
            llm = get_llm(DEFAULT_MODEL, input_data.temperature)

            # Load prompt templates
            map_prompt_template = template_env.get_template("map_prompt.jinja").render(
                summary_type=input_data.summary_type,
                summary_length=input_data.summary_length,
                output_format=input_data.output_format,
                style=input_data.style,
            )
            combine_prompt_template = template_env.get_template("combine_prompt.jinja").render(
                summary_type=input_data.summary_type,
                summary_length=input_data.summary_length,
                output_format=input_data.output_format,
                style=input_data.style,
                additional_instruction=input_data.additional_instruction,
            )

            map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])
            combine_prompt = PromptTemplate(template=combine_prompt_template, input_variables=["text"])

            # Initialize text splitter
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=input_data.chunk_size, chunk_overlap=input_data.chunk_overlap)

            # Split the text into chunks
            docs = text_splitter.create_documents([input_data.text])

            # Initialize the summarization chain based on the chosen method
            if input_data.chain_type == "stuff":
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=combine_prompt)
            elif input_data.chain_type == "map_reduce":
                chain = load_summarize_chain(
                    llm,
                    chain_type="map_reduce",
                    map_prompt=map_prompt,
                    combine_prompt=combine_prompt,
                    return_intermediate_steps=True,
                )
            elif input_data.chain_type == "refine":
                chain = load_summarize_chain(
                    llm,
                    chain_type="refine",
                    question_prompt=map_prompt,
                    refine_prompt=combine_prompt,
                    return_intermediate_steps=True,
                )

            # Run the summarization in a separate thread
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                summarize_future = executor.submit(asyncio.run, asyncio.to_thread(chain, {"input_documents": docs}))
                summarize_result = summarize_future.result()

            # Extract the final summary
            final_summary = summarize_result.get("output_text", "")

            # Apply additional instruction if provided
            if input_data.additional_instruction:
                additional_prompt = template_env.get_template("additional_instruction.jinja").render(summary=final_summary, instruction=input_data.additional_instruction)
                with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                    additional_future = executor.submit(
                        asyncio.run,
                        asyncio.to_thread(lambda: llm.invoke([HumanMessage(content=additional_prompt)])),
                    )
                    result = additional_future.result()
                    final_summary = result if isinstance(result, str) else result.content

            # Render the response
            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(summary=final_summary)

            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response)],
            )

        except Exception as e:
            log.error(f"Error during summarization: {str(e)}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"An error occurred during summarization: {str(e)}")],
            )

    @app.post("/system/summarize/retrievers/get_text_stats/invoke")
    async def get_text_stats(request: Request) -> OutputModel:
        """
        Handle POST requests to get statistics about the input text.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response with text statistics.

        Example:
            >>> from fastapi.testclient import TestClient
            >>> client = TestClient(app)
            >>> headers = { "Content-Type": "application/json", "Integrations-API-Key": "dev-only-token" }
            >>> response = client.post("/system/summarize/retrievers/get_text_stats/invoke",
            ...     json={"text": "This is a sample text."}, headers=headers)
            >>> assert response.status_code == 200
            >>> assert "invocationId" in response.json()
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = SummarizeInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"Invalid input: {str(e)}")],
            )

        # Calculate text statistics
        text = input_data.text
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = text.count(".") + text.count("!") + text.count("?")

        stats = f"Word count: {word_count}\nCharacter count: {char_count}\nSentence count: {sentence_count}"

        return OutputModel(
            status="success",
            invocationId=invocation_id,
            response=[ResponseMessageModel(message=stats)],
        )
