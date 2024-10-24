# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Extended PII Masker integration router with decrypt support, key generation, and PII detection.

This module provides routes for masking, deleting, encrypting, decrypting, detecting, or faking Personally Identifiable Information (PII) in text, as well as generating encryption keys.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import base64
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

from cryptography.fernet import Fernet, InvalidToken
from faker import Faker
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))
DEFAULT_ENCRYPTION_KEY = os.getenv("PII_ENCRYPTION_KEY", Fernet.generate_key().decode())

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/pii_masker/templates"))

# Initialize Faker
fake = Faker()


class PrivacyObject(BaseModel):
    anonymized: str
    hasSensitiveInfo: bool
    hasPII: bool
    hasSPI: bool


class PrivacyOutputModel(BaseModel):
    status: str = Field(default="success")
    invocationId: str
    response: PrivacyObject


class MaskType(str, Enum):
    DELETE = "delete"
    MASK = "mask"
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    FAKE = "fake"
    DETECT = "detect"


class PIIType(str, Enum):
    CREDIT_CARD = "credit_card"
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"
    IP_ADDRESS = "ip_address"
    DATE_OF_BIRTH = "date_of_birth"
    ADDRESS = "address"
    PASSPORT = "passport"
    DRIVERS_LICENSE = "drivers_license"
    BANK_ACCOUNT = "bank_account"
    CUSTOM = "custom"


class PIIMaskInputModel(BaseModel):
    """Model to validate input data for PII masking."""

    text: str = Field(..., description="The text containing PII to be processed")
    mask_type: MaskType = Field(default=MaskType.MASK, description="The type of processing to apply")
    pii_types: List[PIIType] = Field(default=list(PIIType), description="Types of PII to process")
    custom_regex: Optional[Dict[str, str]] = Field(None, description="Custom regex patterns for PII detection")
    encryption_key: Optional[str] = Field(None, description="Custom encryption/decryption key")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_pii_patterns() -> Dict[PIIType, str]:
    """
    Get the regex patterns for PII detection.

    Returns:
        Dict[PIIType, str]: A dictionary of PII types and their corresponding regex patterns.
    """
    return {
        PIIType.CREDIT_CARD: r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        PIIType.NAME: r"\b[A-Z][a-z]+ (?:[A-Z][a-z]+ )?[A-Z][a-z]+\b",
        PIIType.EMAIL: r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        PIIType.PHONE: r"(?x)\b(?:(?:\+|00)?(?:\d{1,3}[-.\s]?)?)?\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        PIIType.SSN: r"\b\d{3}-\d{2}-\d{4}\b",
        PIIType.IP_ADDRESS: r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
        PIIType.DATE_OF_BIRTH: r"\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b",
        PIIType.ADDRESS: r"\b\d+\s+([A-Z][a-z]+ ?)+,?\s+([A-Z][a-z]+ ?)+,?\s+[A-Z]{2}\s+\d{5}(-\d{4})?\b",
        PIIType.PASSPORT: r"\b[A-Z]{1,2}[0-9]{6,9}\b",
        PIIType.DRIVERS_LICENSE: r"\b[A-Z]{1,2}[0-9]{6,8}\b",
        PIIType.BANK_ACCOUNT: r"\b[0-9]{8,17}\b",
    }


def generate_fernet_key() -> str:
    """Generate a valid Fernet key."""
    return Fernet.generate_key().decode()


def validate_fernet_key(key: str) -> bool:
    """Validate if the provided key is a valid Fernet key."""
    try:
        Fernet(key.encode())
        return True
    except ValueError:
        return False


def is_fernet_encrypted(s: str) -> bool:
    """Check if a string is likely to be Fernet-encrypted."""
    try:
        decoded = base64.urlsafe_b64decode(s)
        return len(decoded) > 32 and len(s) % 4 == 0 and s.startswith("gAAAAA")
    except:
        return False


def decrypt_fernet(text: str, encryption_key: str) -> str:
    """Attempt to decrypt a Fernet-encrypted string."""
    try:
        log.debug(f"Attempting to decrypt: {text} with key: {encryption_key}")
        fernet = Fernet(encryption_key.encode())
        decrypted = fernet.decrypt(text.encode()).decode()
        log.debug(f"Successfully decrypted to: {decrypted}")
        return decrypted
    except InvalidToken:
        log.error(f"Invalid token. Could not decrypt: {text}")
        return "Decryption Failed: Invalid Token"  # Explicitly indicating failure
    except Exception as e:
        log.error(f"Unexpected error during decryption: {str(e)}")
        return f"Decryption Failed: {str(e)}"  # Returning specific error message


def process_pii(
    text: str,
    mask_type: MaskType,
    pii_types: List[PIIType],
    custom_regex: Optional[Dict[str, str]] = None,
    encryption_key: Optional[str] = None,
) -> str:
    """
    Process PII in the given text based on the specified mask type and PII types.

    Args:
        text (str): The input text containing PII.
        mask_type (MaskType): The type of processing to apply.
        pii_types (List[PIIType]): Types of PII to process.
        custom_regex (Optional[Dict[str, str]]): Custom regex patterns for PII detection.
        encryption_key (Optional[str]): Custom encryption/decryption key.

    Returns:
        str: The text with processed PII or a detection message.

    Raises:
        ValueError: If an invalid encryption key is provided.
    """
    log.debug(f"Processing PII with mask_type: {mask_type}, pii_types: {pii_types}")
    log.debug(f"Custom encryption key provided: {'Yes' if encryption_key else 'No'}")

    patterns = get_pii_patterns()

    if custom_regex:
        combined_regex = "|".join(custom_regex.values())
        patterns.update({PIIType.CUSTOM: combined_regex})
        log.debug(f"Added custom regex patterns: {custom_regex}")

    if encryption_key:
        if not validate_fernet_key(encryption_key):
            log.error("Invalid encryption key provided")
            raise ValueError("Invalid encryption key provided")
        log.debug("Using custom encryption key")
    else:
        log.debug("Using default encryption key")
        encryption_key = DEFAULT_ENCRYPTION_KEY

    if mask_type == MaskType.DETECT:
        log.debug("Performing PII detection")
        for pii_type in pii_types:
            pattern = patterns.get(pii_type)
            if pattern and re.search(pattern, text):
                log.info(f"PII detected: {pii_type}")
                return "PII_DATA FOUND IN INPUT"
        log.info("No PII detected")
        return text  # Return original text if no PII is detected

    if mask_type == MaskType.DECRYPT:
        log.debug("Performing decryption")
        # Use regex to find all potential Fernet-encrypted strings
        encrypted_pattern = r"gAAAAA[A-Za-z0-9_-]+={0,2}"
        matches = re.findall(encrypted_pattern, text)
        log.debug(f"Found {len(matches)} potential encrypted strings")

        def decrypt_match(match):
            decrypted = decrypt_fernet(match.group(), encryption_key)
            log.debug(f"Decryption result: '{match.group()}' -> '{decrypted}'")
            return decrypted

        decrypted_text = re.sub(encrypted_pattern, decrypt_match, text)
        log.debug(f"Decryption completed. Original length: {len(text)}, Decrypted length: {len(decrypted_text)}")
        return decrypted_text

    # For other mask types (ENCRYPT, MASK, DELETE, FAKE)
    fernet = Fernet(encryption_key.encode())

    log.debug(f"Processing PII types: {pii_types}")
    for pii_type in pii_types:
        pattern = patterns.get(pii_type)
        if not pattern:
            log.warning(f"No pattern found for PII type: {pii_type}")
            continue

        log.debug(f"Processing {pii_type} with pattern: {pattern}")
        if mask_type == MaskType.DELETE:
            text = re.sub(pattern, "", text)
            log.debug(f"Deleted {pii_type}")
        elif mask_type == MaskType.MASK:
            text = re.sub(pattern, f"<{pii_type.name}>", text)
            log.debug(f"Masked {pii_type}")
        elif mask_type == MaskType.ENCRYPT:
            text = re.sub(pattern, lambda m: fernet.encrypt(m.group().encode()).decode(), text)
            log.debug(f"Encrypted {pii_type}")
        elif mask_type == MaskType.FAKE:

            def replace_with_fake():
                if pii_type == PIIType.CREDIT_CARD:
                    return fake.credit_card_number()
                elif pii_type == PIIType.NAME:
                    return fake.name()
                elif pii_type == PIIType.EMAIL:
                    return fake.email()
                elif pii_type == PIIType.PHONE:
                    return fake.phone_number()
                elif pii_type == PIIType.SSN:
                    return fake.ssn()
                elif pii_type == PIIType.IP_ADDRESS:
                    return fake.ipv4()
                elif pii_type == PIIType.DATE_OF_BIRTH:
                    return fake.date_of_birth().strftime("%Y-%m-%d")
                elif pii_type == PIIType.ADDRESS:
                    return fake.address()
                elif pii_type == PIIType.PASSPORT:
                    return fake.passport_number()
                elif pii_type == PIIType.DRIVERS_LICENSE:
                    return fake.license_plate()
                elif pii_type == PIIType.BANK_ACCOUNT:
                    return fake.bban()
                else:
                    return fake.word()

            text = re.sub(pattern, replace_with_fake, text)
            log.debug(f"Faked {pii_type}")

    log.debug("PII processing completed")
    return text


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/pii_masker/retrievers/process_pii/invoke")
    async def process_pii_route(request: Request) -> OutputModel:
        """
        Handle POST requests to process PII in text.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = PIIMaskInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                processed_text = await asyncio.to_thread(
                    process_pii,
                    input_data.text,
                    input_data.mask_type,
                    input_data.pii_types,
                    input_data.custom_regex,
                    input_data.encryption_key,
                )
        except ValueError as e:
            log.error(f"Error processing PII: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            log.error(f"Error processing PII: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing PII")

        response_template = template_env.get_template("pii_masker_response.jinja")
        rendered_response = response_template.render(processed_text=processed_text)

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/pii_masker/ask_process_pii/invoke")
    async def ask_process_pii(request: Request) -> OutputModel:
        """
        Handle POST requests to ask about PII processing and perform the operation.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid, the LLM call fails, or processing fails.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = PIIMaskInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        prompt_template = template_env.get_template("pii_masker_prompt.jinja")
        rendered_prompt = prompt_template.render(
            text=input_data.text,
            mask_type=input_data.mask_type,
            pii_types=input_data.pii_types,
            custom_regex=input_data.custom_regex,
        )

        client = ICAClient()

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                llm_response = await asyncio.to_thread(
                    client.prompt_flow,
                    model_id_or_name=DEFAULT_MODEL,
                    prompt=rendered_prompt,
                )
        except Exception as e:
            log.error(f"Error calling LLM: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing request with LLM")

        try:
            processed_text = process_pii(
                input_data.text,
                input_data.mask_type,
                input_data.pii_types,
                input_data.custom_regex,
                input_data.encryption_key,
            )
        except ValueError as e:
            log.error(f"Error processing PII: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            log.error(f"Error processing PII: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing PII")

        response_template = template_env.get_template("pii_masker_response.jinja")
        rendered_response = response_template.render(llm_response=llm_response, processed_text=processed_text)

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.get("/system/pii_masker/generate_key/invoke")
    async def generate_key() -> OutputModel:
        """
        Generate a new Fernet encryption key.

        Returns:
            OutputModel: The structured output response containing the generated key.
        """
        invocation_id = str(uuid4())
        new_key = generate_fernet_key()
        response_message = ResponseMessageModel(message=f"Generated key: {new_key}")
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/system/pii_masker/sanitize_pii/invoke")
    async def sanitize_pii(request: Request) -> PrivacyOutputModel:
        """
        Handle POST requests to sanitize PII in text and return detailed privacy information.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            PrivacyOutputModel: The structured output response with privacy information.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = PIIMaskInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                anonymized_text = await asyncio.to_thread(
                    process_pii,
                    input_data.text,
                    MaskType.MASK,  # Always use MASK for anonymization
                    input_data.pii_types,
                    input_data.custom_regex,
                    input_data.encryption_key,
                )

            # Check for sensitive information
            has_sensitive_info = anonymized_text != input_data.text

            # Check for PII and SPI
            has_pii = any(
                pii_type
                in [
                    PIIType.NAME,
                    PIIType.EMAIL,
                    PIIType.PHONE,
                    PIIType.SSN,
                    PIIType.DATE_OF_BIRTH,
                    PIIType.ADDRESS,
                ]
                for pii_type in input_data.pii_types
            )
            has_spi = any(
                pii_type
                in [
                    PIIType.CREDIT_CARD,
                    PIIType.PASSPORT,
                    PIIType.DRIVERS_LICENSE,
                    PIIType.BANK_ACCOUNT,
                ]
                for pii_type in input_data.pii_types
            )

            privacy_object = PrivacyObject(
                anonymized=anonymized_text,
                hasSensitiveInfo=has_sensitive_info,
                hasPII=has_pii,
                hasSPI=has_spi,
            )

            return PrivacyOutputModel(invocationId=invocation_id, response=privacy_object)

        except Exception as e:
            log.error(f"Error processing PII: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing PII")
