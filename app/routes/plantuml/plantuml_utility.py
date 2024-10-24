# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Utility functions for PlantUML integration.

This module provides utility functions for encoding and decoding PlantUML text,
as well as generating UML diagrams using a PlantUML server.

Example usage:
    >>> encoded_text = encode_plantuml("@startuml\\nAlice -> Bob: Hello\\n@enduml")
    >>> decoded_text = decode_plantuml(encoded_text)
    >>> print(decoded_text)
    @startuml
    Alice -> Bob: Hello
    @enduml

    >>> filename = asyncio.run(generate_uml_image("@startuml\\nAlice -> Bob: Hello\\n@enduml"))
    >>> print(filename)
    uml_92f8d7a6-f0b5-4e2a-8d2d-1e9b9f4c6e3e.png
"""

import base64
import os
import string
import uuid
import zlib

import httpx
from fastapi import HTTPException

# Useful lambdas
plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + "-_"
base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
b64_to_plantuml = bytes.maketrans(base64_alphabet.encode("utf-8"), plantuml_alphabet.encode("utf-8"))
plantuml_to_b64 = bytes.maketrans(plantuml_alphabet.encode("utf-8"), base64_alphabet.encode("utf-8"))

# Server names
PLANTUML_IMAGE_TYPE = os.getenv("PLANTUML_IMAGE_TYPE", "png")  # Default is png, change to svg
PLANTUML_SERVER_URL = os.getenv("PLANTUML_SERVER_URL", f"https://www.plantuml.com/plantuml/{PLANTUML_IMAGE_TYPE}/")  # Default URL as fallback, or use http://127.0.0.1:9994/svg


def encode_plantuml(data: str) -> str:
    """
    Encodes PlantUML text using zlib compression and base64 encoding.

    Args:
        data (str): PlantUML text to encode.

    Returns:
        str: Encoded PlantUML text.

    Example:
        >>> encode_plantuml("@startuml\\nAlice -> Bob: Hello\\n@enduml")
        'SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd91m00'
    """
    zlibbed_str = zlib.compress(data.encode("utf-8"))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode("utf-8")


def decode_plantuml(data: str) -> str:
    """
    Decodes PlantUML text from base64 encoding and zlib compression.

    Args:
        data (str): Encoded PlantUML text.

    Returns:
        str: Decoded PlantUML text.

    Example:
        >>> decode_plantuml("SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd91m00")
        '@startuml\\nAlice -> Bob: Hello\\n@enduml'
    """
    data = base64.b64decode(data.translate(plantuml_to_b64).encode("utf-8"))
    dec = zlib.decompressobj()  # without checking the crc.
    header = b"x\x9c"
    return dec.decompress(header + data).decode("utf-8")


async def generate_uml_image(description: str) -> str:
    """
    Generates a UML diagram from the provided description using a PlantUML server.

    Args:
        description (str): The PlantUML description of the UML diagram.

    Returns:
        str: Filename of the generated image.

    Raises:
        HTTPException: If there is an error generating the UML diagram.

    Example:
        >>> import asyncio
        >>> filename = asyncio.run(generate_uml_image("@startuml\\nAlice -> Bob: Hello\\n@enduml"))
        >>> print(filename)
        uml_92f8d7a6-f0b5-4e2a-8d2d-1e9b9f4c6e3e.png
    """
    # Encode the UML text
    description = encode_plantuml(description)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PLANTUML_SERVER_URL}{description}")

    if response.status_code == 200:
        filename = f"uml_{uuid.uuid4()}.{PLANTUML_IMAGE_TYPE}"
        image_path = os.path.join("public", "images", filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        with open(image_path, "wb") as out:
            out.write(response.content)
        return filename
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to generate UML diagram.")
