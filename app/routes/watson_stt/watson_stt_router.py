# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: IBM Watson Speech-to-Text integration router with LLM experience.

This module provides routes for transcribing audio to text using various models and formats,
and includes an LLM-powered experience path.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import mimetypes
import os
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import List, Optional, Union

import aiohttp
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
STT_API_KEY = os.getenv("STT_API_KEY")
STT_BASE_URL = os.getenv("STT_BASE_URL")
PUBLIC_DIR = "public/stt"
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Ensure the public directory exists
os.makedirs(PUBLIC_DIR, exist_ok=True)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/watson_stt/templates"))


class AudioFormatEnum(str, Enum):
    FLAC = "audio/flac"
    MP3 = "audio/mp3"
    MPEG = "audio/mpeg"
    OGG = "audio/ogg"
    WAV = "audio/x-wav"
    WEBM = "audio/webm"


class STTInputModel(BaseModel):
    """Model to validate input data for speech-to-text conversion."""

    audio_url: Optional[str] = Field(None, description="URL to the audio file")
    model: str = Field(
        default="en-US_BroadbandModel",
        description="The model to use for speech recognition",
    )
    timestamps: bool = Field(default=False, description="Include timestamps for each word")
    max_alternatives: int = Field(default=1, description="Maximum number of alternative transcripts")

    @validator("audio_url")
    def validate_audio_url(cls, v):
        if v is None:
            return v
        try:
            # Use aiohttp to validate the URL
            aiohttp.client.URL(v)
        except Exception as e:
            raise ValueError(f"Invalid URL: {str(e)}")
        return v


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


async def download_file(url: str) -> tuple[str, str]:
    """
    Download a file from a URL and save it temporarily.

    Args:
        url (str): The URL of the file to download.

    Returns:
        tuple[str, str]: A tuple containing the path to the temporary file and its content type.

    Raises:
        HTTPException: If there's an error downloading the file.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Error downloading file: {await response.text()}",
                    )

                content_type = response.headers.get("Content-Type", "application/octet-stream")

                # Create a temporary file with the correct extension
                file_extension = mimetypes.guess_extension(content_type) or ".tmp"
                fd, temp_path = tempfile.mkstemp(suffix=file_extension)

                # Write the content to the temporary file
                with os.fdopen(fd, "wb") as temp_file:
                    temp_file.write(await response.read())

                return temp_path, content_type
    except aiohttp.ClientError as e:
        log.error(f"Error downloading file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error downloading file: {str(e)}")
    except Exception as e:
        log.error(f"Unexpected error downloading file: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error downloading file")


async def transcribe_audio(
    audio_file: Union[UploadFile, str],
    content_type: str,
    model: str,
    timestamps: bool,
    max_alternatives: int,
) -> dict:
    """
    Transcribe audio using the specified model and options.

    Args:
        audio_file (Union[UploadFile, str]): The audio file to transcribe or path to the file.
        content_type (str): The content type of the audio file.
        model (str): The model to use for speech recognition.
        timestamps (bool): Whether to include timestamps for each word.
        max_alternatives (int): Maximum number of alternative transcripts.

    Returns:
        dict: The transcription results.

    Raises:
        HTTPException: If there's an error in the API call.
    """
    # Convert audio/x-wav to audio/wav
    if content_type == "audio/x-wav":
        content_type = "audio/wav"

    headers = {
        "Content-Type": content_type,
    }

    auth = aiohttp.BasicAuth("apikey", STT_API_KEY)

    params = {
        "model": model,
        "timestamps": str(timestamps).lower(),
        "max_alternatives": str(max_alternatives),
    }

    try:
        async with aiohttp.ClientSession() as session:
            if isinstance(audio_file, UploadFile):
                data = audio_file.file
            else:
                data = open(audio_file, "rb")

            async with session.post(
                f"{STT_BASE_URL}/v1/recognize",
                data=data,
                headers=headers,
                auth=auth,
                params=params,
            ) as response:
                if response.status != 200:
                    error_detail = await response.text()
                    log.error(f"Error in STT API call: {error_detail}")
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Error in STT API call: {error_detail}",
                    )

                return await response.json()
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error(f"Error in transcribe_audio: {str(e)}")
        raise HTTPException(status_code=500, detail="Error transcribing audio")
    finally:
        if isinstance(audio_file, str):
            os.remove(audio_file)  # Delete the temporary file


async def generate_llm_response(transcript: str) -> str:
    """
    Generate a response using an LLM based on the transcript.

    Args:
        transcript (str): The transcribed text.

    Returns:
        str: The LLM-generated response.

    Raises:
        HTTPException: If there's an error in the LLM API call.
    """
    client = ICAClient()

    prompt = f"""You are an AI assistant analyzing a transcript of speech. Your task is to provide a summary
    and identify any key points or action items from the transcript. If there are any questions in the
    transcript, provide answers if possible.

    Transcript:
    {transcript}

    Please provide:
    1. A brief summary of the transcript (2-3 sentences)
    2. Key points or main ideas (bullet points)
    3. Any action items or next steps mentioned (if applicable)
    4. Answers to any questions in the transcript (if applicable)

    Your response:
    """

    try:
        response = await asyncio.to_thread(client.prompt_flow, model_id_or_name=DEFAULT_MODEL, prompt=prompt)
        return response
    except Exception as e:
        log.error(f"Error in LLM API call: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating LLM response")


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/stt/retrievers/transcribe_audio/invoke")
    async def transcribe_audio_route(
        request: Request,
        audio_file: Optional[UploadFile] = File(None),
        audio_url: Optional[str] = None,
        model: str = "en-US_BroadbandModel",
        timestamps: bool = False,
        max_alternatives: int = 1,
    ) -> OutputModel:
        """
        Handle POST requests to transcribe audio to text.

        Args:
            request (Request): The request object.
            audio_file (Optional[UploadFile]): The audio file to transcribe.
            audio_url (Optional[str]): URL to the audio file.
            model (str): The model to use for speech recognition.
            timestamps (bool): Whether to include timestamps for each word.
            max_alternatives (int): Maximum number of alternative transcripts.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error in processing.
        """
        invocation_id = str(uuid.uuid4())

        try:
            # If the request is JSON, parse it
            if request.headers.get("Content-Type") == "application/json":
                json_data = await request.json()
                input_data = STTInputModel(**json_data)
                audio_url = input_data.audio_url
            else:
                input_data = STTInputModel(
                    audio_url=audio_url,
                    model=model,
                    timestamps=timestamps,
                    max_alternatives=max_alternatives,
                )

            if audio_file:
                audio_data = audio_file
                content_type = audio_file.content_type
            elif audio_url:
                audio_data, content_type = await download_file(audio_url)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Either audio_file or audio_url must be provided",
                )

            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                transcription_future = executor.submit(
                    asyncio.run,
                    transcribe_audio(
                        audio_data,
                        content_type,
                        input_data.model,
                        input_data.timestamps,
                        input_data.max_alternatives,
                    ),
                )
                transcription = transcription_future.result()

            response_template = template_env.get_template("stt_response.jinja")
            rendered_response = response_template.render(transcription=transcription)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        except Exception as e:
            log.error(f"Error in transcribe_audio_route: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")

    @app.post("/experience/stt/ask_transcribe/invoke")
    async def ask_transcribe_route(
        request: Request,
        audio_file: Optional[UploadFile] = File(None),
        audio_url: Optional[str] = None,
        model: str = "en-US_BroadbandModel",
        timestamps: bool = False,
        max_alternatives: int = 1,
    ) -> OutputModel:
        """
        Handle POST requests to transcribe audio and provide a natural language response using an LLM.

        Args:
            request (Request): The request object.
            audio_file (Optional[UploadFile]): The audio file to transcribe.
            audio_url (Optional[str]): URL to the audio file.
            model (str): The model to use for speech recognition.
            timestamps (bool): Whether to include timestamps for each word.
            max_alternatives (int): Maximum number of alternative transcripts.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error in processing.
        """
        invocation_id = str(uuid.uuid4())

        try:
            # If the request is JSON, parse it
            if request.headers.get("Content-Type") == "application/json":
                json_data = await request.json()
                input_data = STTInputModel(**json_data)
                audio_url = input_data.audio_url
            else:
                input_data = STTInputModel(
                    audio_url=audio_url,
                    model=model,
                    timestamps=timestamps,
                    max_alternatives=max_alternatives,
                )

            if audio_file:
                audio_data = audio_file
                content_type = audio_file.content_type
            elif audio_url:
                audio_data, content_type = await download_file(audio_url)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Either audio_file or audio_url must be provided",
                )

            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                transcription_future = executor.submit(
                    asyncio.run,
                    transcribe_audio(
                        audio_data,
                        content_type,
                        input_data.model,
                        input_data.timestamps,
                        input_data.max_alternatives,
                    ),
                )
                transcription = transcription_future.result()

            # Extract the transcript text from the transcription result
            transcript_text = " ".join([result.get("alternatives", [{}])[0].get("transcript", "") for result in transcription.get("results", [])])

            # Generate LLM response
            llm_response = await generate_llm_response(transcript_text)

            response_template = template_env.get_template("stt_nl_response.jinja")
            rendered_response = response_template.render(transcription=transcription, llm_response=llm_response)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        except Exception as e:
            log.error(f"Error in ask_transcribe_route: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing transcription request: {str(e)}",
            )
