# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: File upload integration router with UI and enhanced security.

This module provides routes for generating upload URLs, uploading files,
managing user files, and serving a simple UI for these operations.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import hashlib
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3 70B Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))
UPLOAD_DIR = Path("public/userfiles")
BASE_URL = os.getenv("SERVER_NAME", "http://localhost:8080")
UNIQUE_SALT = os.getenv("UNIQUE_SALT", "default_salt")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/file_upload/templates"))


class UserInputModel(BaseModel):
    """Model to validate input data for user identification."""

    team_id: str = Field(..., description="The team ID of the user")
    user_email: str = Field(..., description="The email of the user")


class UploadURLOutputModel(BaseModel):
    """Model to structure the upload URL response."""

    upload_url: str = Field(..., description="The URL for file upload")


class FileListOutputModel(BaseModel):
    """Model to structure the file list response."""

    files: List[str] = Field(..., description="List of user's files")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def generate_user_hash(team_id: str, user_email: str) -> str:
    """
    Generate a hash from team ID, user email, and a unique salt.

    Args:
        team_id (str): The team ID.
        user_email (str): The user's email.

    Returns:
        str: A hash string.

    >>> generate_user_hash("team123", "user@example.com")
    '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
    """
    combined = f"{team_id}:{user_email}:{UNIQUE_SALT}".encode("utf-8")
    return hashlib.sha256(combined).hexdigest()


def add_custom_routes(app: FastAPI):
    """Adds custom routes to the FastAPI application for agent invocation and result retrieval."""

    # Serve static files (CSS, JS, etc.)
    app.mount("/static", StaticFiles(directory="app/routes/file_upload/static"), name="static")

    @app.get("/file_upload_ui")
    async def file_upload_ui(key: str = Query(...), team_id: str = Query(...), user_email: str = Query(...)):
        """Serve the file upload UI."""
        template = template_env.get_template("file_upload_ui.html")
        return HTMLResponse(template.render(key=key, team_id=team_id, user_email=user_email))

    @app.post("/system/file_upload/retrievers/get_upload_url/invoke")
    async def get_upload_url(request: Request) -> OutputModel:
        """
        Handle POST requests to generate an upload URL.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = UserInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        user_hash = generate_user_hash(input_data.team_id, input_data.user_email)
        upload_url = f"{BASE_URL}/file_upload_ui?key={user_hash}&team_id={input_data.team_id}&user_email={input_data.user_email}"

        output = UploadURLOutputModel(upload_url=upload_url)
        response_message = ResponseMessageModel(message=f"Upload URL generated: {output.upload_url}")
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/system/file_upload/upload")
    async def upload_file(
        file: UploadFile = File(...),
        key: str = Form(...),
        team_id: str = Form(...),
        user_email: str = Form(...),
    ):
        """
        Handle file uploads.

        Args:
            file (UploadFile): The file to be uploaded.
            key (str): The user's access key.
            team_id (str): The team ID of the user.
            user_email (str): The email of the user.

        Returns:
            dict: A message indicating the success of the upload and the full URL to the file.

        Raises:
            HTTPException: If the key is invalid or the upload fails.
        """
        if not key or not team_id or not user_email:
            raise HTTPException(
                status_code=400,
                detail="Access key, team ID, and user email are required",
            )

        if key != generate_user_hash(team_id, user_email):
            raise HTTPException(status_code=403, detail="Invalid access key")

        user_dir = UPLOAD_DIR / key
        user_dir.mkdir(parents=True, exist_ok=True)

        file_extension = Path(file.filename).suffix
        file_name = f"{uuid4()}{file_extension}"
        file_path = user_dir / file_name

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                await asyncio.get_event_loop().run_in_executor(executor, lambda: file_path.write_bytes(file.file.read()))
        except Exception as e:
            log.error(f"File upload failed: {str(e)}")
            raise HTTPException(status_code=500, detail="File upload failed")

        file_url = f"{BASE_URL}/system/file_upload/download/{file_name}?key={key}&team_id={team_id}&user_email={user_email}"
        return {
            "message": "File uploaded successfully",
            "file_name": file_name,
            "file_url": file_url,
        }

    @app.get("/system/file_upload/list")
    async def list_files(key: str, team_id: str, user_email: str):
        """
        List files for a user.

        Args:
            key (str): The user's access key.
            team_id (str): The team ID of the user.
            user_email (str): The email of the user.

        Returns:
            FileListOutputModel: A list of the user's files.

        Raises:
            HTTPException: If the key is invalid or the directory doesn't exist.
        """
        if not key or not team_id or not user_email:
            raise HTTPException(
                status_code=400,
                detail="Access key, team ID, and user email are required",
            )

        if key != generate_user_hash(team_id, user_email):
            raise HTTPException(status_code=403, detail="Invalid access key")

        user_dir = UPLOAD_DIR / key
        if not user_dir.exists():
            return FileListOutputModel(files=[])

        files = [f.name for f in user_dir.iterdir() if f.is_file()]
        return FileListOutputModel(files=files)

    @app.delete("/system/file_upload/delete/{file_name}")
    async def delete_file(file_name: str, key: str, team_id: str, user_email: str):
        """
        Delete a user's file.

        Args:
            file_name (str): The name of the file to delete.
            key (str): The user's access key.
            team_id (str): The team ID of the user.
            user_email (str): The email of the user.

        Returns:
            dict: A message indicating the success of the deletion.

        Raises:
            HTTPException: If the key is invalid, the file doesn't exist, or the deletion fails.
        """
        if not key or not team_id or not user_email:
            raise HTTPException(
                status_code=400,
                detail="Access key, team ID, and user email are required",
            )

        if key != generate_user_hash(team_id, user_email):
            raise HTTPException(status_code=403, detail="Invalid access key")

        file_path = UPLOAD_DIR / key / file_name
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        try:
            file_path.unlink()
        except Exception as e:
            log.error(f"File deletion failed: {str(e)}")
            raise HTTPException(status_code=500, detail="File deletion failed")

        return {"message": "File deleted successfully"}

    @app.get("/system/file_upload/download/{file_name}")
    async def download_file(file_name: str, key: str, team_id: str, user_email: str):
        """
        Download a user's file.

        Args:
            file_name (str): The name of the file to download.
            key (str): The user's access key.
            team_id (str): The team ID of the user.
            user_email (str): The email of the user.

        Returns:
            FileResponse: The file to be downloaded.

        Raises:
            HTTPException: If the key is invalid or the file doesn't exist.
        """
        if not key or not team_id or not user_email:
            raise HTTPException(
                status_code=400,
                detail="Access key, team ID, and user email are required",
            )

        if key != generate_user_hash(team_id, user_email):
            raise HTTPException(status_code=403, detail="Invalid access key")

        file_path = UPLOAD_DIR / key / file_name
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(file_path, filename=file_name)

    @app.post("/experience/file_upload/ask_about_files/invoke")
    async def ask_about_files(request: Request) -> OutputModel:
        """
        Handle POST requests to ask questions about user files.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = UserInputModel(**data)
            query = data.get("query")
            if not query:
                raise ValueError("Query is required")
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        user_hash = generate_user_hash(input_data.team_id, input_data.user_email)
        user_dir = UPLOAD_DIR / user_hash
        files = [f.name for f in user_dir.iterdir() if f.is_file()] if user_dir.exists() else []

        prompt_template = template_env.get_template("file_query_prompt.jinja")
        rendered_prompt = prompt_template.render(query=query, files=files)

        client = ICAClient()

        async def call_prompt_flow():
            return await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt,
            )

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                response_future = executor.submit(asyncio.run, call_prompt_flow())
                response = response_future.result()
        except Exception as e:
            log.error(f"LLM call failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to process query")

        response_template = template_env.get_template("file_query_response.jinja")
        rendered_response = response_template.render(result=response)

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])