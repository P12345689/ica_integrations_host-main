# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Monday.com integration router.

This module provides routes for interacting with the Monday.com API, asking natural language questions about Monday.com data,
and exporting Monday.com board data to XLSX format.
"""

import asyncio
import io
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, AsyncGenerator, Dict, List, Optional
from uuid import uuid4

import httpx
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Environment variables
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
MONDAY_API_TOKEN = os.getenv("MONDAY_API_TOKEN")
MONDAY_API_URL = "https://api.monday.com/v2"
DEFAULT_BOARD_ID = int(os.getenv("MONDAY_DEFAULT_BOARD_ID", "0"))
ITEMS_PER_CHUNK = 10  # Number of items to process in each LLM call

# Log initial settings
log.info(
    f"Loaded environment variables: DEFAULT_MODEL={DEFAULT_MODEL}, DEFAULT_MAX_THREADS={DEFAULT_MAX_THREADS}, DEFAULT_BOARD_ID={DEFAULT_BOARD_ID}"
)


# Load Jinja2 environment
def from_json_filter(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return {}  # or handle the error as needed


template_env = Environment(loader=FileSystemLoader("app/routes/monday/templates"))
template_env.filters["from_json"] = from_json_filter
log.info("Initialized Jinja2 environment")


class MondayInputModel(BaseModel):
    """Model to validate input data for Monday.com API calls."""

    query: str = Field(..., description="The GraphQL query or mutation")
    variables: Optional[Dict[str, Any]] = Field(default=None, description="Variables for the GraphQL query")


class ExperienceInputModel(BaseModel):
    """Model to validate input data for natural language queries."""

    query: str = Field(..., description="The natural language query about Monday.com data")
    board_id: Optional[int] = Field(None, description="The ID of the board to query (optional)")


class ExportInputModel(BaseModel):
    """Model to validate input data for exporting board data."""

    board_id: Optional[int] = Field(None, description="The ID of the board to export (optional)")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


log.info("Defined Pydantic models")


async def call_monday_api(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Call the Monday.com API with the given GraphQL query and variables.
    """
    log.debug(f"Calling Monday.com API with query: {query}, Variables: {variables}")

    headers = {
        "Authorization": MONDAY_API_TOKEN,
        "Content-Type": "application/json",
    }
    payload = {"query": query, "variables": variables}
    log.debug(f"HTTP Headers: {headers}")
    log.debug(f"HTTP Payload: {json.dumps(payload, indent=2)}")

    async with httpx.AsyncClient() as client:
        try:
            log.info(f"Sending POST request to {MONDAY_API_URL}")
            response = await client.post(MONDAY_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            log.info("Received successful response from Monday.com API")
            log.debug(f"Response Content: {response.text}")
            return response.json()
        except httpx.HTTPStatusError as e:
            log.error(f"HTTP error occurred: {e}")
            log.error(f"Response content: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            log.error(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


async def get_board_items_chunked(
    board_id: int, chunk_size: int = ITEMS_PER_CHUNK
) -> AsyncGenerator[List[Dict[str, Any]], None]:
    """
    Retrieve items from a Monday.com board in chunks.
    """
    log.info(f"Starting to retrieve items for board_id: {board_id}, Chunk size: {chunk_size}")

    cursor = None
    total_items = 0

    while True:
        query, variables = "", {}
        if cursor:
            log.debug(f"Fetching next chunk with cursor: {cursor}")
            query = """
            query ($cursor: String!, $limit: Int!) {
                next_items_page(cursor: $cursor, limit: $limit) {
                    cursor
                    items {
                        id
                        name
                        column_values {
                            id
                            column {
                                title
                            }
                            value
                            text
                        }
                    }
                }
            }
            """
            variables = {"cursor": cursor, "limit": chunk_size}
        else:
            log.debug("Fetching first chunk")
            query = """
            query ($board_id: [ID!], $limit: Int!) {
                boards(ids: $board_id) {
                    items_page(limit: $limit) {
                        cursor
                        items {
                            id
                            name
                            column_values {
                                id
                                column {
                                    title
                                }
                                value
                                text
                            }
                        }
                    }
                }
            }
            """
            variables = {"board_id": [str(board_id)], "limit": chunk_size}

        result = await call_monday_api(query, variables)

        if (
            "data" not in result
            or (cursor and "next_items_page" not in result["data"])
            or (not cursor and "boards" not in result["data"])
        ):
            log.error(f"Unexpected API response: {result}")
            raise HTTPException(status_code=500, detail="Unexpected API response")

        page_data = result["data"]["next_items_page"] if cursor else result["data"]["boards"][0]["items_page"]
        if not page_data:
            log.error(f"No items page data found in API response: {result}")
            raise HTTPException(status_code=500, detail="No items page data found in API response")

        items = page_data.get("items", [])
        total_items += len(items)
        log.info(f"Retrieved {len(items)} items in this chunk. Total items so far: {total_items}")
        log.debug(f"Items in this chunk: {json.dumps(items, indent=2)}")

        yield items

        cursor = page_data.get("cursor")
        if not cursor:
            log.info(f"No more items to fetch. Total items retrieved: {total_items}")
            break
        log.debug(f"Next cursor: {cursor}")


def add_custom_routes(app: FastAPI):
    @app.post("/system/monday/api/invoke")
    async def monday_api_call(request: Request) -> OutputModel:
        """
        Handle POST requests to make Monday.com API calls.
        """
        log.info("Received request to /system/monday/api/invoke")
        invocation_id = str(uuid4())
        log.debug(f"Generated invocation_id: {invocation_id}")

        try:
            data = await request.json()
            log.debug(f"Received data: {data}")
            input_data = MondayInputModel(**data)
            log.info("Successfully validated input data")

            result = await call_monday_api(input_data.query, input_data.variables)
            log.info("Successfully received response from Monday.com API")
            log.debug(f"API response: {result}")
            response_message = ResponseMessageModel(message=str(result))
            log.info("Prepared response message")
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except HTTPException as e:
            log.error(f"HTTP exception occurred: {e}")
            raise e
        except Exception as e:
            log.error(f"Error in monday_api_call: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @app.post("/experience/monday/ask/invoke")
    async def ask_monday(request: Request) -> OutputModel:
        """
        Handle POST requests to ask natural language questions about Monday.com data.
        """
        log.info("Received request to /experience/monday/ask/invoke")
        invocation_id = str(uuid4())
        log.debug(f"Generated invocation_id: {invocation_id}")

        try:
            data = await request.json()
            log.debug(f"Received data: {data}")
            input_data = ExperienceInputModel(**data)
            log.info("Successfully validated input data")

            board_id = input_data.board_id or DEFAULT_BOARD_ID
            log.info(f"Using board_id: {board_id}")

            client = ICAClient()
            log.info("Initialized ICAClient")
            prompt_template = template_env.get_template("monday_prompt.jinja")
            response_template = template_env.get_template("monday_response.jinja")
            log.info("Loaded Jinja templates")

            full_response = ""
            chunk_count = 0
            async for items_chunk in get_board_items_chunked(board_id):
                chunk_count += 1
                log.info(f"Processing chunk {chunk_count}")
                log.debug(f"Items in chunk {chunk_count}: {json.dumps(items_chunk, indent=2)}")

                rendered_prompt = prompt_template.render(
                    query=input_data.query,
                    board_items=json.dumps(items_chunk, indent=2),
                )
                log.debug(f"Rendered prompt for chunk {chunk_count}: {rendered_prompt}")

                async def call_prompt_flow():
                    log.info(f"Calling prompt_flow for chunk {chunk_count}")
                    return await asyncio.to_thread(
                        client.prompt_flow,
                        model_id_or_name=DEFAULT_MODEL,
                        prompt=rendered_prompt,
                    )

                with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                    log.info(f"Executing prompt_flow for chunk {chunk_count} in ThreadPoolExecutor")
                    formatted_result_future = executor.submit(asyncio.run, call_prompt_flow())
                    formatted_result = formatted_result_future.result()
                    log.info(f"Received result for chunk {chunk_count}")
                    log.debug(f"Result for chunk {chunk_count}: {formatted_result}")

                full_response += formatted_result + "\n"
                log.info(f"Appended result for chunk {chunk_count} to full_response")

            log.info("Rendering final response")
            rendered_response = response_template.render(result=full_response)
            log.debug(f"Rendered response: {rendered_response}")
            response_message = ResponseMessageModel(message=rendered_response)
            log.info("Prepared final response message")
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except HTTPException as e:
            log.error(f"HTTP exception occurred: {e}")
            raise e
        except Exception as e:
            log.error(f"Error in ask_monday: {e}")
            raise HTTPException(status_code=500, detail="Error processing the request")

    @app.post("/system/monday/export/xlsx/invoke")
    async def export_board_to_xlsx(request: Request) -> StreamingResponse:
        """
        Handle POST requests to export a Monday.com board to XLSX format.
        """
        log.info("Received request to /system/monday/export/xlsx/invoke")
        try:
            data = await request.json()
            log.debug(f"Received data: {data}")
            input_data = ExportInputModel(**data)
            log.info("Successfully validated input data")

            board_id = input_data.board_id or DEFAULT_BOARD_ID
            log.info(f"Using board_id: {board_id}")

            log.info("Initializing DataFrame")
            df = pd.DataFrame()

            log.info("Retrieving board items")
            async for items_chunk in get_board_items_chunked(board_id):
                log.debug(f"Processing chunk of {len(items_chunk)} items")
                chunk_df = pd.DataFrame(items_chunk)
                log.debug(f"Created DataFrame for chunk: {chunk_df.shape}")
                df = pd.concat([df, chunk_df], ignore_index=True)
                log.debug(f"Concatenated chunk DataFrame to main DataFrame: {df.shape}")

            log.info(f"Total items in DataFrame: {len(df)}")
            log.debug(f"DataFrame columns: {df.columns}")

            log.info("Converting DataFrame to XLSX")
            excel_bytes = io.BytesIO()
            df.to_excel(excel_bytes, index=False)
            excel_bytes.seek(0)
            log.info("DataFrame converted to XLSX")

            log.info("Preparing streaming response")
            headers = {"Content-Disposition": 'attachment; filename="monday_export.xlsx"'}
            return StreamingResponse(
                excel_bytes,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers=headers,
            )
        except Exception as e:
            log.error(f"Error in export_board_to_xlsx: {e}")
            raise HTTPException(status_code=500, detail="Error exporting board data")

    @app.post("/system/monday/board_items/invoke")
    async def get_all_board_items(request: Request) -> OutputModel:
        """
        Handle POST requests to retrieve all items from a Monday.com board.
        """
        log.info("Received request to /system/monday/board_items/invoke")
        invocation_id = str(uuid4())
        log.debug(f"Generated invocation_id: {invocation_id}")

        try:
            data = await request.json()
            log.debug(f"Received data: {data}")
            input_data = BoardItemsInputModel(**data)
            log.info("Successfully validated input data")

            board_id = input_data.board_id or DEFAULT_BOARD_ID
            log.info(f"Using board_id: {board_id}")

            log.info("Retrieving all board items")
            all_items = []
            async for items_chunk in get_board_items_chunked(board_id):
                log.debug(f"Retrieved {len(items_chunk)} items in chunk")
                all_items.extend(items_chunk)

            log.info(f"Total items retrieved: {len(all_items)}")
            log.debug(f"All items: {json.dumps(all_items, indent=2)}")

            response_message = ResponseMessageModel(message=json.dumps(all_items))
            log.info("Prepared response message")
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except HTTPException as e:
            log.error(f"HTTP exception occurred: {e}")
            raise e
        except Exception as e:
            log.error(f"Error in get_all_board_items: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving board items")
