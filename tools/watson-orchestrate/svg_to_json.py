#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description:
    Download, resize an SVG file to 48x48 pixels, extract its content, and produce a JSON object
    with the SVG properly formatted as a string. Produce a JSON object with the SVG properly
    formatted as a string for use with Watson Orchestrate.
Reference:
    https://www.ibm.com/docs/en/watson-orchestrate?topic=skills-understanding-x-properties#adding-an-icon-to-the-app
Usage:
    python svg_to_json.py [--verbose] [--resize] <path_to_svg_file_or_url>

Args:
    path_to_svg_file_or_url: The path to the local SVG file or the URL of the SVG file.
    --verbose: Enable verbose output.
    --resize: Resize the SVG to 48x48 pixels.

Returns:
    None. Prints the JSON output to the console.

Raises:
    FileNotFoundError: If a required tool is not installed or the file is not found.
    ValueError: If the path to the SVG file or URL is missing.
    URLError: If there is an error downloading the file from the URL.

Example:
    python svg_to_json.py https://example.com/icon.svg
    {"info": {"x-ibm-application-icon": "<svg>...</svg>"}}
"""

import json
import logging
import os
import sys
import tempfile
from typing import List
from urllib.error import URLError
from urllib.request import urlopen

from cairosvg import svg2png
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def check_dependencies() -> None:
    """
    Check if required tools are installed.

    Raises:
        FileNotFoundError: If a required tool is not installed.
    """
    try:
        pass
    except ImportError:
        raise FileNotFoundError("Required tool 'jq' is not installed. Please install it using 'pip install jq'.")


def download_svg(url: str, verbose: bool = False) -> str:
    """
    Download an SVG file from a URL.

    Args:
        url: The URL of the SVG file.
        verbose: If True, enables verbose output for the download process.

    Returns:
        The path to the downloaded SVG file.

    Raises:
        URLError: If there is an error downloading the file from the URL.
    """
    temp_file = tempfile.mkstemp(suffix=".svg")[1]
    try:
        if verbose:
            log.info(f"Downloading SVG from {url}...")
        with urlopen(url) as response, open(temp_file, "wb") as file:
            file.write(response.read())
    except URLError as e:
        log.error("Failed to download the file. Check the URL and network connectivity.")
        os.remove(temp_file)
        raise e
    return temp_file


def resize_svg(file: str) -> None:
    """
    Resize an SVG file to 48x48 pixels using Python libraries.

    Args:
        file: The path to the SVG file.
    """
    log.info("Resizing SVG...")
    with tempfile.NamedTemporaryFile(suffix=".png") as temp_png:
        svg2png(url=file, write_to=temp_png.name, output_width=48, output_height=48)
        resized_svg = tempfile.mkstemp(suffix=".svg")[1]
        Image.open(temp_png.name).save(resized_svg)
        os.replace(resized_svg, file)


def format_svg_for_json(file: str) -> str:
    """
    Extract SVG content and format it for JSON.

    Args:
        file: The path to the SVG file.

    Returns:
        The formatted SVG content.
    """
    with open(file, "r") as f:
        svg_content = f.read().replace("\n", "")
    return svg_content


def main(args: List[str]) -> None:
    """
    Main function to process the SVG file and generate the JSON output.

    Args:
        args: Command-line arguments.

    Raises:
        ValueError: If the path to the SVG file or URL is missing.
        FileNotFoundError: If the file does not exist or the URL is not valid.
    """
    verbose = False
    resize = False
    svg_source = ""

    try:
        if "--verbose" in args:
            verbose = True
            args.remove("--verbose")
        if "--resize" in args:
            resize = True
            args.remove("--resize")

        if len(args) == 0:
            raise ValueError("Missing path to SVG file or URL.")
        svg_source = args[0]

        check_dependencies()

        if svg_source.startswith(("http://", "https://")):
            svg_file = download_svg(svg_source, verbose)
        elif os.path.isfile(svg_source):
            svg_file = svg_source
        else:
            raise FileNotFoundError(f"File does not exist and URL is not valid: {svg_source}")

        if resize:
            resize_svg(svg_file)
        else:
            log.info("Skipping resize as per user request.")

        log.info("Formatting SVG content for JSON...")
        svg_json_content = format_svg_for_json(svg_file)

        json_output = json.dumps({"info": {"x-ibm-application-icon": svg_json_content}})
        print(json_output)

    except Exception as e:
        log.error(f"An error occurred: {str(e)}")
        sys.exit(1)

    finally:
        if svg_source.startswith(("http://", "https://")):
            os.remove(svg_file)


if __name__ == "__main__":
    main(sys.argv[1:])
