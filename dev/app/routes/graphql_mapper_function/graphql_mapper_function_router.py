# -*- coding: utf-8 -*-
"""
Author: Oluwole Obamakin
Description: integration provides a rag solution for ingesting graphql schemas. Users can input a rest response and the matching mapper function is created

TODO: Remember to update the module-level docstring with specific details about your integration
and remove / address the TODOs in this template.
Remplace the example timestamp with a function of your choice.

This module provides routes for graphql_mapper_function, including a system route
for generating a timestamp, an experience route that wraps the system
functionality with LLM interaction, and a file generation route that creates
a timestamped file and returns its URL.

Integration Development Guidelines:
1. Use Pydantic v2 models to validate all inputs and outputs.
2. All functions should be defined as async.
3. Ensure that all code has full docstring coverage in Google docstring format.
4. Implement full unit test coverage (can also use doctest).
5. Use Jinja2 templates for LLM prompts and response formatting.
6. Implement proper error handling and logging.
7. Use environment variables for configuration where appropriate.
8. Follow PEP 8 style guidelines.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import logging
import os
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_consultingassistants import ChatConsultingAssistants
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from pydantic import BaseModel, Field

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to INFO in production

# Set default model and max threads from environment variables
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
# TODO: Update the template directory path if needed
template_env = Environment(loader=FileSystemLoader("app/routes/graphql_mapper_function/templates"))

# TODO: Update these models to match your integration's input requirements


class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""

    query: str = Field(..., description="The rest response as an input")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/graphql_mapper_function/generate_mapper_function/invoke")
    async def generate_mapper_function_route(request: Request) -> OutputModel:
        """
        Handle POST requests to generate a mapper function.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or timestamp generation fails.
        """

        print("here")

        log.info("Received request to generate mapper function")
        invocation_id = str(uuid4())

        # set the model
        model = ChatConsultingAssistants(model="Llama3.1 70b Instruct")
        # _______________________________________________ Chroma character splitting

        model_name = "BAAI/bge-small-en"
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        hf = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )

        # Load the document and split it into chunks
        # TODO Where will I load Context
        loader = TextLoader("app/routes/graphql_mapper_function/tools/graphql_context.txt")
        documents = loader.load()

        # # Split it into chunks
        text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)

        # # Create the embedding function
        vectorstore = Chroma.from_documents(documents=docs, collection_name="rag_chroma", embedding=hf)

        context = vectorstore.as_retriever()

        system_prompt = (
            "You are an expert JavaScript and TypeScript programmer. You are very good at generating efficient, production-ready code for users."
            "You will be working on writing the types and mapping function with error handling between a GraphQL Schema and example REST responses. This code is for the back-end of a website, so make sure you use relevant frameworks to ensure the code is production-ready. Generate TypeScript code for React and Node.js that fits the user requirements listed below."
            " - **Reflection**: Log your thoughts, steps, and decisions during the code generation process, appending messages to a reflection log."
            "- **Scratchpad**: Use a scratchpad to store intermediate results, examples, and other context that you refer to while generating the final output."
            "From these steps, output the type generation, mapping function with error handling, and a respective unit test in the style of the examples in the chat context."
            "With this output, provide an explanation of the assumptions that were made."
            "1. The user will input an example REST response that corresponds to the schema in the vector database. {input}"
            "2. Refer to the provided examples in our chat context as a guide for writing the TypeScript mapping function that maps between the schema and response. Ensure consistency in structure and adherence to coding conventions outlined in the examples. {context}"
            "3. Assume that no property is hard-coded."
            "4. Remember that the REST responses are examples, meaning there can be many responses for a single service."
            "5. Check the number of features in the schema and ensure that is reflected in the mapping function."
            "6. Parse the response as a JSON object and access properties directly."
            "7. Write the function as a named export."
            "8. Please use the given examples to generate types for the function to ensure type safety, using **type** instead of **interface**."
            "9. The ID must be a caching ID that is unique based on the object, and it should be **generated based on the items in the object that change**."
            "10. Keep the number of parameters in the functions consistent."
            "11. Please use the examples in the chat context to write in **error handling** and **logging** in the mapping function, while remembering to return NULL."
            "12. Include **optional chaining operators** to ensure robustness."
            "13. Output the mapping function and a unit test for it."
            "14. For the unit test, use **test** instead of **it**."
            "15. Provide an explanation of where assumptions were made for the type generation, mapping function with error handling, and the unit test, or where context was missing and so mapping could not be completed or was done as a pass-through."
            "Context: {context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        # set the parser
        output_parser = StrOutputParser()
        question_answer_chain = create_stuff_documents_chain(model, prompt) | output_parser
        chain = create_retrieval_chain(context, question_answer_chain)

        try:
            # get the data
            data = await request.json()
            log.debug(f"Received input data: {data}")
            # get the query
            query = data["input"]["query"]
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            # execute the search
            # Invoke the chain with the example input and context
            result = chain.invoke({"input": query, "context": context})
            formatted_result = result["answer"]
        except Exception:
            # handle any other unexpected errors
            logging.exception("Error invoking Grahql Mapper Function")
            formatted_result = "I'm sorry but i couldn't find a response, please try with a different query"

        # return response
        return OutputModel(
            invocationId=invocation_id,
            response=[ResponseMessageModel(message=formatted_result)],
        )


# TODO: Add any additional routes or helper functions as needed for your integration

# TODO: Consider adding any additional configuration variables specific to your integration

# TODO: Implement additional error handling specific to your integration if needed

# TODO: Create corresponding test files for unit and integration tests
