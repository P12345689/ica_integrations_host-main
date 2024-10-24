# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: IBM Watson Text-to-Speech integration router.

This module provides routes for listing available voices, getting information about specific voices,
and converting text to speech using various voices and formats.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import List, Optional

import aiofiles
import aiohttp
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
TTS_API_KEY = os.getenv("TTS_API_KEY")
TTS_BASE_URL = os.getenv("TTS_BASE_URL")
PUBLIC_DIR = "public/tts"

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Ensure the public directory exists
os.makedirs(PUBLIC_DIR, exist_ok=True)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/tts/templates"))


class AudioFormatEnum(str, Enum):
    ALAW = "audio/alaw"
    BASIC = "audio/basic"
    FLAC = "audio/flac"
    L16 = "audio/l16"
    MP3 = "audio/mp3"
    MPEG = "audio/mpeg"
    MULAW = "audio/mulaw"
    OGG = "audio/ogg"
    OGG_OPUS = "audio/ogg;codecs=opus"
    WAV = "audio/wav"
    WEBM = "audio/webm"
    WEBM_OPUS = "audio/webm;codecs=opus"
    WEBM_VORBIS = "audio/webm;codecs=vorbis"


class VoiceFeatures(BaseModel):
    """Model for voice features."""

    voice_transformation: bool
    custom_pronunciation: bool


class Voice(BaseModel):
    """Model for voice information."""

    name: str
    language: str
    gender: str
    url: str
    customizable: bool
    supported_features: VoiceFeatures
    description: str


class VoiceListResponse(BaseModel):
    """Model for the response of listing all voices."""

    voices: List[Voice]


class TTSInputModel(BaseModel):
    """Model to validate input data for text-to-speech conversion."""

    text: str = Field(..., description="The text to convert to speech")
    voice: str = Field(..., description="The voice to use for speech synthesis")
    format: AudioFormatEnum = Field(default=AudioFormatEnum.WAV, description="The audio format for the output file")
    rate: Optional[int] = Field(None, description="The sampling rate for the audio (where applicable)")
    endianness: Optional[str] = Field(None, description="The endianness for audio/l16 format")


class SpecificVoiceInputModel(BaseModel):
    """Model to validate input data for getting a specific voice."""

    voice: str = Field(..., description="The name of the voice to get information about")
    customization_id: Optional[str] = Field(None, description="The GUID of a custom model")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


async def list_voices() -> VoiceListResponse:
    """
    List all available voices.

    Returns:
        VoiceListResponse: The list of all available voices.

    Raises:
        HTTPException: If there's an error in the API call.
    """
    headers = {
        "Accept": "application/json",
    }

    auth = aiohttp.BasicAuth("apikey", TTS_API_KEY)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{TTS_BASE_URL}/v1/voices", headers=headers, auth=auth) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="Error in TTS API call")

                data = await response.json()
                return VoiceListResponse(**data)
    except Exception as e:
        log.error(f"Error in list_voices: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing voices")


async def get_specific_voice(voice: str, customization_id: Optional[str] = None) -> Voice:
    """
    Get information about a specific voice.

    Args:
        voice (str): The name of the voice to get information about.
        customization_id (Optional[str]): The GUID of a custom model.

    Returns:
        Voice: Information about the specified voice.

    Raises:
        HTTPException: If there's an error in the API call.
    """
    headers = {
        "Accept": "application/json",
    }

    auth = aiohttp.BasicAuth("apikey", TTS_API_KEY)

    params = {}
    if customization_id:
        params["customization_id"] = customization_id

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{TTS_BASE_URL}/v1/voices/{voice}",
                headers=headers,
                auth=auth,
                params=params,
            ) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="Error in TTS API call")

                data = await response.json()
                return Voice(**data)
    except Exception as e:
        log.error(f"Error in get_specific_voice: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting specific voice")


async def generate_speech(
    text: str,
    voice: str,
    format: AudioFormatEnum,
    rate: Optional[int] = None,
    endianness: Optional[str] = None,
) -> str:
    """
    Generate speech from text using the specified voice and format.

    Args:
        text (str): The text to convert to speech.
        voice (str): The voice to use for speech synthesis.
        format (AudioFormatEnum): The audio format for the output file.
        rate (Optional[int]): The sampling rate for the audio (where applicable).
        endianness (Optional[str]): The endianness for audio/l16 format.

    Returns:
        str: The filename of the generated audio file.

    Raises:
        HTTPException: If there's an error in the API call or file saving process.
    """
    # Map the AudioFormatEnum to the correct MIME type
    mime_type = format.value  # This is already the correct MIME type string
    extension = mime_type.split("/")[-1].split(";")[0]
    filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(PUBLIC_DIR, filename)

    headers = {
        "Content-Type": "application/json",
        "Accept": mime_type,
    }

    auth = aiohttp.BasicAuth("apikey", TTS_API_KEY)

    params = {"voice": voice}
    if rate:
        params["rate"] = str(rate)
    if endianness and format == AudioFormatEnum.L16:
        params["endianness"] = endianness

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{TTS_BASE_URL}/v1/synthesize",
                json={"text": text},
                headers=headers,
                auth=auth,
                params=params,
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Error in TTS API call: {await response.text()}",
                    )

                async with aiofiles.open(file_path, mode="wb") as f:
                    await f.write(await response.read())

        return filename
    except Exception as e:
        log.error(f"Error in generate_speech: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating speech")


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/tts/retrievers/list_voices/invoke")
    async def list_voices_route(request: Request) -> OutputModel:
        """
        Handle POST requests to list all available voices.

        Args:
            request (Request): The request object.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error in processing.
        """
        invocation_id = str(uuid.uuid4())

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                voices_future = executor.submit(asyncio.run, list_voices())
                voices = voices_future.result()

            response_template = template_env.get_template("voice_list_response.jinja")
            rendered_response = response_template.render(voices=voices.voices)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error in list_voices_route: {str(e)}")
            raise HTTPException(status_code=500, detail="Error listing voices")

    @app.post("/system/tts/retrievers/get_specific_voice/invoke")
    async def get_specific_voice_route(request: Request) -> OutputModel:
        """
        Handle POST requests to get information about a specific voice.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or there's an error in processing.
        """
        invocation_id = str(uuid.uuid4())

        try:
            data = await request.json()
            input_data = SpecificVoiceInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                voice_future = executor.submit(
                    asyncio.run,
                    get_specific_voice(input_data.voice, input_data.customization_id),
                )
                voice = voice_future.result()

            response_template = template_env.get_template("specific_voice_response.jinja")
            rendered_response = response_template.render(voice=voice)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error in get_specific_voice_route: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting specific voice")

    @app.post("/system/tts/retrievers/generate_speech/invoke")
    async def generate_speech_route(request: Request) -> OutputModel:
        """
        Handle POST requests to generate speech from text.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or there's an error in speech generation.
        """
        invocation_id = str(uuid.uuid4())

        try:
            data = await request.json()
            input_data = TTSInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                filename_future = executor.submit(
                    asyncio.run,
                    generate_speech(
                        input_data.text,
                        input_data.voice,
                        input_data.format,
                        input_data.rate,
                        input_data.endianness,
                    ),
                )
                filename = filename_future.result()

            download_url = f"{SERVER_NAME}/{PUBLIC_DIR}/{filename}"

            response_template = template_env.get_template("tts_response.jinja")
            rendered_response = response_template.render(download_url=download_url)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error in generate_speech_route: {str(e)}")
            raise HTTPException(status_code=500, detail="Error generating speech")

    @app.get("/{PUBLIC_DIR}/{filename}")
    async def serve_file(filename: str) -> FileResponse:
        """
        Serve the generated audio file.

        Args:
            filename (str): The name of the file to serve.

        Returns:
            FileResponse: The audio file.

        Raises:
            HTTPException: If the file is not found.
        """
        file_path = os.path.join(PUBLIC_DIR, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file_path)
