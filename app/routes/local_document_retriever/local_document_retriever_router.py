# -*- coding: utf-8 -*-
"""
Author: Gytis Oziunas
Description: Public Downloads Router - Handles downloading of public documents with correct MIME types.
The main functionality includes:
- Serving docx and pptx files from the public/documents directory.
- Returning appropriate HTTP responses for file not found errors.
- Setting correct MIME types for the downloaded files.
Example usage:
    # Make a GET request to the /public/documents/docx/{filename} endpoint to download a docx file.
    # Make a GET request to the /public/documents/pptx/{filename} endpoint to download a pptx file.
"""

import json
import logging
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

log = logging.getLogger(__name__)


class InputModel(BaseModel):
    """Model to validate input data for file retrieval."""

    filename: str


def add_custom_routes(app: FastAPI):
    @app.post("/system/docx/invoke", response_class=FileResponse)
    async def download_docx(request: Request) -> FileResponse:
        """
        Handle POST requests to retrieve a .docx file from the given filename.
        Args:
            request (Request): The request object containing the filename.
        Returns:
            FileResponse: The file output response.
        Raises:
            HTTPException: If the input is invalid or file was not found.
        """
        try:
            data = await request.json()
            input_data = InputModel(**data)
        except json.JSONDecodeError:
            data = await request.form()
            input_data = InputModel(**data)

        file_path = os.path.join("public/documents/docx/", input_data.filename)

        if not os.path.isfile(file_path):
            log.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail=f"File '{input_data.filename}' not found")

        try:
            headers = {"Content-Disposition": f'attachment; filename="{input_data.filename}"'}

            return FileResponse(
                path=file_path,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                filename=input_data.filename,
                headers=headers,
            )

        except Exception as e:
            log.error(f"Error while preparing file response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error occurred while processing the file",
            )

    @app.post("/system/pptx/invoke", response_class=FileResponse)
    async def download_pptx(request: Request) -> FileResponse:
        """
        Handle POST requests to retrieve a .pptx file from the given filename.
        Args:
            request (Request): The request object containing the filename.
        Returns:
            FileResponse: The file output response.
        Raises:
            HTTPException: If the input is invalid or file was not found.
        """
        try:
            data = await request.json()
            input_data = InputModel(**data)
        except json.JSONDecodeError:
            data = await request.form()
            input_data = InputModel(**data)

        file_path = os.path.join("public/documents/pptx/", input_data.filename)

        if not os.path.isfile(file_path):
            log.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail=f"File '{input_data.filename}' not found")

        try:
            headers = {"Content-Disposition": f'attachment; filename="{input_data.filename}"'}

            return FileResponse(
                path=file_path,
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                filename=input_data.filename,
                headers=headers,
            )

        except Exception as e:
            log.error(f"Error while preparing file response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error occurred while processing the file",
            )
