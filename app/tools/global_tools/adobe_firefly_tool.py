import json
import logging
import os

import requests
from langchain.agents import tool
from typing import Dict

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

FIREFLY_ENDPOINT = os.getenv("ADOBE_FIREFLY_ENDPOINT", "firefly-beta.adobe.io")
FIREFLY_AUTH_ENDPOINT = os.getenv(
    "ADOBE_FIREFLY_AUTH_ENDPOINT", "https://ims-na1.adobelogin.com/ims/token/v3"
)
FIREFLY_CLIENT_ID = os.getenv("ADOBE_FIREFLY_CLIENT_ID", "default_value_not_provided")
FIREFLY_CLIENT_SECRET = os.getenv(
    "ADOBE_FIREFLY_CLIENT_SECRET", "default_value_not_provided"
)

DEFAULT_IMAGE_TYPE = "photo"
DEFAULT_IMAGE_WIDTH = 1024
DEFAULT_IMAGE_HEIGHT = 1024
DEFAULT_VISUAL_INTENSITY = 6
DEFAULT_LOCALE = "en-US"


class FireflyAuthException(Exception):
    """
    Thrown whenever there are issues authenticating to the Firefly API.

    This exception is raised when there is a failure to authenticate with the Firefly API,
    either due to missing or invalid credentials, or any other authentication-related issues.

    Attributes:
        message (str): The error message associated with the authentication exception.

    Methods:
        __init__(self, message: str): Initializes a new instance of the FireflyAuthException class
            with the specified error message.

    Example:
        >>> try:
        ...     # Attempt to authenticate with Firefly API
        ...     token = get_adobe_firefly_token()
        ... except FireflyAuthException as e:
        ...     print(f"Authentication failed: {e}")
        ...
        Authentication failed: Invalid credentials
    """

    def __init__(self, message: str):
        """
        Initializes a new instance of the FireflyAuthException class with the specified error message.

        Args:
            message (str): The error message associated with the authentication exception.
        """
        self.message = message
        super().__init__(self.message)


def get_adobe_firefly_token() -> str:
    """
    Makes an OAuth call to get an API access token for Firefly.

    The Client ID and Secret are provided by the following environment variables:
    - ADOBE_FIREFLY_CLIENT_ID
    - ADOBE_FIREFLY_CLIENT_SECRET

    Returns:
        str: The access token.

    Raises:
        FireflyAuthException: If there is a failure to authenticate.

    Examples:
        >>> os.environ["ADOBE_FIREFLY_CLIENT_ID"] = "your_client_id"
        >>> os.environ["ADOBE_FIREFLY_CLIENT_SECRET"] = "your_client_secret"
        >>> token = get_adobe_firefly_token()
        >>> assert token.startswith("Bearer ")

    """
    try:
        data = {
            "client_secret": FIREFLY_CLIENT_SECRET,
            "client_id": FIREFLY_CLIENT_ID,
            "grant_type": "client_credentials",
            "scope": "openid, AdobeID, firefly_api, firefly_enterprise, ff_apis,read_organizations",
        }
        response = requests.post(url=FIREFLY_AUTH_ENDPOINT, data=data)
        if response.status_code != 200:
            raise FireflyAuthException(
                f"Failed to authenticate with Firefly, reason: {response.text}"
            )
        return response.json()["access_token"]
    except KeyError:
        raise FireflyAuthException(
            "Environment variables ADOBE_FIREFLY_CLIENT_ID or ADOBE_FIREFLY_CLIENT_SECRET are not defined."
        )


def adobe_firefly_headers(access_token: str) -> Dict[str, str]:
    """
    Creates headers needed for Firefly calls.

    Args:
        access_token (str): The access token for authentication.

    Returns:
        Dict[str, str]: The headers dictionary.

    Examples:
        >>> access_token = "your_access_token"
        >>> headers = adobe_firefly_headers(access_token)
        >>> assert headers["Authorization"] == f"Bearer {access_token}"

    """
    return {
        "Content-Type": "application/json",
        "X-Api-Key": FIREFLY_CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }


def adobe_image_upload(url: str, access_token: str) -> str:
    """
    Grabs an image from a URL, then uploads it for use in Firefly.

    Args:
        url (str): The URL of the image to upload.
        access_token (str): The access token for authentication.
        firefly_endpoint (str): The Firefly API endpoint.

    Returns:
        str: The ID of the uploaded image.

    Raises:
        requests.RequestException: If there is an error uploading the image.

    Examples:
        >>> url = "https://example.com/image.png"
        >>> access_token = "your_access_token"
        >>> firefly_endpoint = "firefly-beta.adobe.io"
        >>> image_id = adobe_image_upload(url, access_token)
        >>> assert isinstance(image_id, str)

    """
    input_response = requests.get(url)
    headers = adobe_firefly_headers(access_token)
    headers["Content-Type"] = input_response.headers['Content-Type']
    response = requests.post(
        url=f"https://{FIREFLY_ENDPOINT}/v2/storage/image",
        headers=headers,
        data=input_response.content,
    )
    return response.json()["images"][0]["id"]


@tool
def adobe_firefly_image_generation(input_str: str) -> str:
    """
    Makes an image generation call, uploading reference images as needed.

    Args:
        input_json (str): A JSON string containing following possible keys
            'query' - description of the image
            'image_type' - the type of generated image (art or picture)
            'width' - the width of the generated image
            'height' - the height of the generated image
            'visual_intensity' - the visual intensity of the image
            'locale' - the locale for description
            'avoid' - (Optional) string containing negative prompt
            'reference_image' - (Optional) the URL of a reference image

    Returns:
        str: The presigned URL of the generated image.

    Raises:
        requests.RequestException: If there is an error generating the image.
        ValueError: if there is an error parsing the JSON input
    """
    try:
        input_data = json.loads(input_str)
    except json.JSONDecodeError as e:
        input_data = {
            "query": input_str
        }
        log.info(f"Error parsing JSON {str(e)} using input: {input_str} as string")
       

    access_token = get_adobe_firefly_token()
    headers = adobe_firefly_headers(access_token)
    try:
        data = {
            "prompt": input_data.get("query"),
            "contentClass": input_data.get("image_type", DEFAULT_IMAGE_TYPE),
            "n": 1,
            "size": {
                "width": input_data.get("width", DEFAULT_IMAGE_WIDTH),
                "height": input_data.get("height", DEFAULT_IMAGE_HEIGHT),
            },
            "visualIntensity": input_data.get("visual_intensity", DEFAULT_VISUAL_INTENSITY),
            "locale": input_data.get("locale", DEFAULT_LOCALE),
        }
        if "avoid" in input_data and bool(input_data["avoid"]):
            data["negativePrompt"] = input_data["avoid"]
        if "reference_image" in input_data and bool(input_data["reference_image"]):
            data["styles"] = {
                "referenceImage": {
                    "id": adobe_image_upload(input_data["reference_image"], access_token)
                }
            }
        response = requests.post(
            url=f"https://{FIREFLY_ENDPOINT}/v2/images/generate", headers=headers, json=data
        )
        log.info(f"Received response {response.json()}")
    except Exception as e:
        log.exception("An error occurred")
    response_json = response.json()
    if "error_code" in response_json:
        return response_json["message"]
    else:
        return response_json["outputs"][0]["image"]["presignedUrl"]


@tool
def adobe_firefly_image_expand(input_str: str) -> str:
    """
    Makes a generative fill call, uploading the image to work on, and the mask area.

    Args:
        input_json (str): A JSON string containing following possible keys
            'query' - description of the image
            'width' - the width of the generated image
            'height' - the height of the generated image
            'reference_image' - the URL of a reference image

    Returns:
        str: The presigned URL of the generated image.

    Raises:
        requests.RequestException: If there is an error generating the image.
        ValueError: if there is an error parsing the JSON input
    """
    try:
        input_data = json.loads(input_str)
    except json.JSONDecodeError as e:
        log.error(f"Error parsing JSON {str(e)}")
        raise ValueError("Invalid JSON input. Please provide a valid JSON string.")

    access_token = get_adobe_firefly_token()
    headers = adobe_firefly_headers(access_token)

    data = {
        "prompt": input_data.get("query"),
        "n": 1,
        "size": {
            "width": input_data.get("width", DEFAULT_IMAGE_WIDTH),
            "height": input_data.get("height", DEFAULT_IMAGE_HEIGHT),
        },
        "image": {
            "id": adobe_image_upload(input_data.get("reference_image"), access_token)
        },
    }
    response = requests.post(
        url=f"https://{FIREFLY_ENDPOINT}/v1/images/expand", headers=headers, json=data
    )
    return response.json()["images"][0]["image"]["presignedUrl"]


@tool
def adobe_firefly_generative_fill(input_str: str) -> str:
    """
    Makes an image expand call, uploading the image to expand.

    Args:
        input_json (str): A JSON string containing following possible keys
            'query' - description of the image
            'width' - the width of the generated image
            'height' - the height of the generated image
            'reference_image' - the URL of a reference image
            'mask_image' - the URL of the mask image

    Returns:
        str: The presigned URL of the generated image.

    Raises:
        requests.RequestException: If there is an error generating the image.
        ValueError: if there is an error parsing the JSON input
    """
    try:
        input_data = json.loads(input_str)
    except json.JSONDecodeError as e:
        log.error(f"Error parsing JSON {str(e)}")
        raise ValueError("Invalid JSON input. Please provide a valid JSON string.")

    access_token = get_adobe_firefly_token()
    headers = adobe_firefly_headers(access_token)

    data = {
        "prompt": input_data.get("query"),
        "n": 1,
        "size": {
            "width": input_data.get("width", DEFAULT_IMAGE_WIDTH),
            "height": input_data.get("height", DEFAULT_IMAGE_HEIGHT),
        },
        "image": {
            "id": adobe_image_upload(input_data.get("reference_image"), access_token)
        },
        "mask": {
            "id": adobe_image_upload(input_data.get("mask_image"), access_token)
        },
    }
    response = requests.post(
        url=f"https://{FIREFLY_ENDPOINT}/v1/images/fill", headers=headers, json=data
    )
    return response.json()["images"][0]["image"]["presignedUrl"]

# Example usage
if __name__ == "__main__":
    response = adobe_firefly_image_generation("London Bridge")
    print(response)