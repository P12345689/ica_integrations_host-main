# -*- coding: utf-8 -*-
import base64
import logging
import os
import uuid
from io import BytesIO

import httpx
from fastapi import HTTPException
from PIL import Image

log = logging.getLogger(__name__)


async def call_nvidia_generation_api(model: str, query: str) -> str:
    """
    Makes a call to the given NVIDIA image generation API to generate an image.

    Args:
        model (str): The model to be used in generation.
        query (str): The query to be used in generation.

    Returns:
        str: The response from the API.

    Raises:
        httpx.RequestError: If there is an error making the API call.

    Examples:
        >>> input_data = InputModel(query="Generate an image of a penguin in a suit", image_url="", model="stable-diffusion-3-medium")
        >>> response = await call_nvidia_generation_api(input_data)
        >>> assert isinstance(response, str)
    """
    async with httpx.AsyncClient() as client:
        payload, headers, url = adjust_params(model, query)
        response = await client.post(url=url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        def get_response_data():
            if model == "stable-diffusion-3-medium":
                return response_data["image"]
            elif model == "sdxl-turbo" or model == "stable-diffusion-xl" or model == "sdxl-lightning":
                return response_data["artifacts"][0]["base64"]
            else:
                raise HTTPException(
                    status_code=422,
                    detail="Model not recognized (stable-diffusion-3-medium or sdxl-turbo",
                )

        if response.status_code == 200:
            filename = f"nvidia_{uuid.uuid4()}.jpg"
            image_path = os.path.join("public", "nvidia", filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_data = base64.b64decode(get_response_data())

            with open(image_path, "wb") as out:
                out.write(image_data)

            base_url = os.getenv("SERVER_NAME", "http://localhost:8080")
            image_url = f"{base_url}/public/nvidia/{filename}"
            return image_url
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to generate image.")


async def call_nvidia_llm_api(model: str, query: str) -> str:
    """
    Makes a call to the given NVIDIA LLM API to generate a response.

    Args:
        model (str): The model to be used in generation.
        query (str): The query to be used in generation.

    Returns:
        str: The response from the API.

    Raises:
        httpx.RequestError: If there is an error making the API call.

    Examples:
        >>> input_data = InputModel(query="What is the percentage change of the net income from Q4 FY23 to Q4 FY24?", image_url="", model="llama3-chatqa-1.5-70b")
        >>> response = await call_nvidia_llm_api(input_data)
        >>> assert isinstance(response, str)

    """
    async with httpx.AsyncClient() as client:
        payload = {
            "messages": [{"content": f"{query}", "role": "user"}],
            "model": f"nvidia/{model}",
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024,
            "seed": 42,
            "stream": False,
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_nvidia_bearer_token()}",
        }

        response = await client.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]


async def call_neva22b_api(image_url: str, query: str) -> str:
    """
    Makes a call to the NVIDIA Neva-22B API to recognize an image.

    Args:
        image_url (str): The url of the image to be recognized.
        query (str): The query to be used in generation.

    Returns:
        str: The response from the API.

    Raises:
        httpx.RequestError: If there is an error making the API call.

    Examples:
        >>> input_data = InputModel(query="What is in this image?", image_url="https://example.com/image.jpg", model="")
        >>> response = await call_neva22b_api(input_data)
        >>> assert isinstance(response, str)

    """
    log.info(f"Calling NVIDIA Neva-22B API with input data: {image_url} and {query}")
    async with httpx.AsyncClient() as client:
        log.info(f"Downloading image from URL: {image_url}")
        image_response = await client.get(image_url)
        log.info(f"Image downloaded. Status code: {image_response.status_code}")
        image = Image.open(BytesIO(image_response.content))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        log.info(f"Image converted to base64. Size: {len(image_base64)} bytes")

        log.info("Constructing payload for API request.")
        payload = {
            "messages": [
                {
                    "content": f'{query} <img src="data:image/png;base64,{image_base64}" />',
                    "name": None,
                    "role": "user",
                }
            ],
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024,
            "seed": 42,
            "stream": False,
        }
        log.info(f"Payload constructed: {payload}")

        log.info("Constructing headers for API request.")
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_nvidia_bearer_token()}",
        }
        log.info(f"Headers constructed: {headers}")

        log.info("Making API request to NVIDIA Neva-22B.")
        response = await client.post(
            "https://ai.api.nvidia.com/v1/vlm/nvidia/neva-22b",
            json=payload,
            headers=headers,
        )
        log.info(f"API response received. Status code: {response.status_code}")
        response.raise_for_status()
        response_data = response.json()
        log.info(f"API response data: {response_data}")
        return response_data["choices"][0]["message"]["content"]


def get_nvidia_bearer_token() -> str:
    """
    Retrieves the Bearer token for authenticating with the NVIDIA Neva-22B API.

    The Bearer token is provided by the following environment variable:
    - NVIDIA_BEARER_TOKEN

    Returns:
        str: The Bearer token.

    Raises:
        KeyError: If the environment variable NVIDIA_BEARER_TOKEN is not defined.

    Examples:
        >>> os.environ["NVIDIA_BEARER_TOKEN"] = "your_bearer_token"
        >>> token = get_nvidia_bearer_token()
        >>> assert token == "your_bearer_token"

    """
    try:
        token = os.environ["NVIDIA_BEARER_TOKEN"]
        log.info(f"Retrieved NVIDIA_BEARER_TOKEN: {token[:5]}...{token[-5:]}")
        return token
    except KeyError:
        log.error("Environment variable NVIDIA_BEARER_TOKEN is not defined.")
        raise KeyError("Environment variable NVIDIA_BEARER_TOKEN is not defined.")


def adjust_params(model: str, query: str):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_nvidia_bearer_token()}",
    }
    if model == "stable-diffusion-3-medium":
        url = f"https://ai.api.nvidia.com/v1/genai/stabilityai/{model}"
        payload = {
            "aspect_ratio": "1:1",
            "cfg_scale": 5,
            "mode": "text-to-image",
            "model": "sd3",
            "negative_prompt": "string",
            "output_format": "jpeg",
            "prompt": f"{query}",
            "seed": 0,
            "steps": 50,
        }
    elif model == "sdxl-turbo":
        url = f"https://ai.api.nvidia.com/v1/genai/stabilityai/{model}"
        payload = {
            "height": 512,
            "width": 512,
            "text_prompts": [{"text": f"{query}", "weight": 1}],
            "cfg_scale": 0,
            "clip_guidance_preset": "NONE",
            "sampler": "K_EULER_ANCESTRAL",
            "samples": 1,
            "seed": 0,
            "steps": 4,
            "style_preset": "none",
        }
    elif model == "stable-diffusion-xl":
        url = f"https://ai.api.nvidia.com/v1/genai/stabilityai/{model}"
        payload = {
            "height": 1024,
            "width": 1024,
            "text_prompts": [{"text": f"{query}", "weight": 1}],
            "cfg_scale": 5,
            "clip_guidance_preset": "NONE",
            "sampler": "K_DPM_2_ANCESTRAL",
            "samples": 1,
            "seed": 0,
            "steps": 25,
            "style_preset": "none",
        }
    elif model == "sdxl-lightning":
        url = f"https://ai.api.nvidia.com/v1/genai/bytedance/{model}"
        payload = {
            "height": 1024,
            "width": 1024,
            "text_prompts": [{"text": f"{query}", "weight": 1}],
            "cfg_scale": 0,
            "clip_guidance_preset": "NONE",
            "sampler": "K_EULER_ANCESTRAL",
            "samples": 1,
            "seed": 0,
            "steps": 4,
            "style_preset": "none",
        }
    else:
        raise HTTPException(
            status_code=422,
            detail="Model not recognized (stable-diffusion-3-medium, sdxl-turbo, stable-diffusion-xl or sdxl-lightning",
        )

    return payload, headers, url
