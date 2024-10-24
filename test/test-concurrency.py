#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: A configurable and feature-rich test script for running concurrent HTTP requests.

Features:
- Load test configuration from a JSON file
- Set test duration and concurrency level
- Verbose output with detailed logging
- Colored console output for better readability
- Comprehensive test statistics and reporting
- Graceful handling of keyboard interrupts
- Configurable authentication (API key and cookie support)
- Improved error handling and logging
- Option to run each endpoint once and print the report
- Support for environment variables in payload
- Automatic detection of required environment variables
- Option to disable specific endpoints in the configuration
"""

import argparse
import datetime
import json
import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple

import requests
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama for colored output


def load_config(file_path: str) -> Dict[str, Any]:
    """
    Load JSON configuration from a file.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        Dict[str, Any]: The loaded configuration dictionary.
    """
    with open(file_path, "r") as file:
        return json.load(file)


def replace_env_vars(payload: Any) -> Any:
    """
    Recursively replace environment variables in the payload.

    Args:
        payload (Any): The payload to process.

    Returns:
        Any: The payload with environment variables replaced.
    """
    if isinstance(payload, dict):
        return {k: replace_env_vars(v) for k, v in payload.items()}
    elif isinstance(payload, list):
        return [replace_env_vars(item) for item in payload]
    elif isinstance(payload, str):
        return re.sub(r"\${(\w+)}", lambda m: os.getenv(m.group(1), m.group(0)), payload)
    else:
        return payload


def detect_required_env_vars(config: Dict[str, Any]) -> List[str]:
    """
    Detect required environment variables from the configuration.

    Args:
        config (Dict[str, Any]): The configuration dictionary.

    Returns:
        List[str]: A list of required environment variable names.
    """
    required_vars = set()

    def search_for_env_vars(item: Any):
        if isinstance(item, dict):
            for value in item.values():
                search_for_env_vars(value)
        elif isinstance(item, list):
            for value in item:
                search_for_env_vars(value)
        elif isinstance(item, str):
            matches = re.findall(r"\${(\w+)}", item)
            required_vars.update(matches)

    search_for_env_vars(config)
    return list(required_vars)


def send_request(
    url: str, method: str, headers: Dict[str, str], data: Optional[Dict[str, Any]]
) -> Tuple[Optional[int], str, float, float]:
    """
    Send an HTTP request and return the response along with request and response timestamps.

    Args:
        url (str): The URL to send the request to.
        method (str): The HTTP method to use (e.g., 'GET', 'POST').
        headers (Dict[str, str]): The headers to include in the request.
        data (Optional[Dict[str, Any]]): The JSON payload for the request, if any.

    Returns:
        Tuple[Optional[int], str, float, float]: The response status code, response text, request start time, and request end time.
    """
    start_time = time.time()
    try:
        response = requests.request(method, url, headers=headers, json=data)
        end_time = time.time()
        logging.debug(f"Received response: {response.text}")
        return response.status_code, response.text, start_time, end_time
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        end_time = time.time()
        return None, str(e), start_time, end_time


def handle_requests(
    config: Dict[str, Any],
    duration: int,
    verbose: bool,
    cookie: str,
    integrations_auth_token: str,
    run_once: bool,
) -> None:
    """
    Handle all configured requests based on the configuration and for a specified duration.

    Args:
        config (Dict[str, Any]): Configuration containing server, endpoints, and other settings.
        duration (int): Total duration to run the tests in seconds.
        verbose (bool): Flag to enable verbose logging output.
        cookie (str): Optional cookie string to include in the request headers.
        integrations_auth_token (str): API key for authentication.
        run_once (bool): Flag to run each endpoint once and exit.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    start_time = time.time()
    request_counts = {ep["path"]: 0 for ep in config["endpoints"] if not ep.get("disabled", False)}
    total_times = {ep["path"]: 0.0 for ep in config["endpoints"] if not ep.get("disabled", False)}
    success_counts = {ep["path"]: 0 for ep in config["endpoints"] if not ep.get("disabled", False)}
    failure_counts = {ep["path"]: 0 for ep in config["endpoints"] if not ep.get("disabled", False)}
    interrupt_count = 0
    last_interrupt_time = 0

    def print_stats():
        """Print statistics of all requests made."""
        end_time = time.time()
        total_time = end_time - start_time
        print(f"\n{Fore.CYAN}Test completed or interrupted. Duration: {total_time:.2f}s{Style.RESET_ALL}")
        print(
            f"{Fore.CYAN}{'Path':<60} {'Requests':<10} {'Req/min':<10} {'Avg Time':<10} {'Success':<10} {'Failure':<10}{Style.RESET_ALL}"
        )
        for path, count in request_counts.items():
            req_per_min = count * 60 / total_time
            avg_time = total_times[path] / count if count > 0 else 0
            success = success_counts[path]
            failure = failure_counts[path]
            color = Fore.GREEN if failure == 0 else Fore.RED
            print(
                f"{color}{path:<60} {count:<10} {req_per_min:<10.2f} {avg_time:<10.2f} {success:<10} {failure:<10}{Style.RESET_ALL}"
            )

    def request_loop(endpoint: Dict[str, Any]) -> None:
        """Continuous loop to send requests as per endpoint configuration."""
        if endpoint.get("disabled", False):
            logging.info(f"{Fore.YELLOW}Skipping disabled endpoint: {endpoint['path']}{Style.RESET_ALL}")
            return

        url = f"{config['server_url']}{endpoint['path']}"
        method = endpoint["method"]
        headers = {
            "Content-Type": endpoint["content_type"],
            "Integrations-API-Key": integrations_auth_token,
        }
        if cookie:
            headers["Cookie"] = cookie

        while True:
            logging.info(f"{Fore.BLUE}Starting test for {method} {endpoint['path']}{Style.RESET_ALL}")
            payload = replace_env_vars(endpoint.get("payload"))
            status, response, req_time, res_time = send_request(url, method, headers, payload)
            request_counts[endpoint["path"]] += 1

            if status == 200:
                success_counts[endpoint["path"]] += 1
                color = Fore.GREEN
            else:
                failure_counts[endpoint["path"]] += 1
                color = Fore.RED
                logging.error(f"{Fore.RED}Error response for {method} {endpoint['path']}: {response}{Style.RESET_ALL}")

            total_times[endpoint["path"]] += res_time - req_time

            log_message = f"{method} {color}{endpoint['path']}{Style.RESET_ALL} at {datetime.datetime.fromtimestamp(req_time)}: Status {color}{status}{Style.RESET_ALL} [Processed in {res_time - req_time:.2f}s]"
            if verbose:
                log_message += f"; Response: {response}"
            logging.info(log_message)

            if run_once:
                break

            time.sleep(endpoint["interval"])

    with ThreadPoolExecutor(max_workers=config["concurrency_level"]) as executor:
        futures = [executor.submit(request_loop, endpoint) for endpoint in config["endpoints"]]

        try:
            logging.info(f"Test started at {datetime.datetime.now()}. Duration: {duration} seconds.")
            logging.info(f"Concurrency level: {config['concurrency_level']}")
            logging.info(
                f"Endpoints: {', '.join(ep['path'] for ep in config['endpoints'] if not ep.get('disabled', False))}"
            )

            if run_once:
                logging.info("Running each endpoint once.")
                for future in futures:
                    future.result()
            else:
                done, not_done = as_completed(futures, timeout=duration), []
                for future in done:
                    future.result()
                for future in not_done:
                    future.cancel()
        except KeyboardInterrupt:
            interrupt_time = time.time()
            if interrupt_time - last_interrupt_time < 1:
                print_stats()
                exit(0)
            else:
                interrupt_count += 1
                last_interrupt_time = interrupt_time
                for future in futures:
                    future.cancel()
                executor.shutdown(wait=False)
                if interrupt_count == 1:
                    logging.info("Interrupt received. Press Ctrl+C again within 1 second to exit immediately.")
                    print_stats()
        finally:
            print_stats()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run configurable HTTP requests based on a JSON file.")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to the configuration JSON file",
    )
    parser.add_argument("--duration", type=int, default=120, help="Duration to run the test in seconds")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output for more detailed logging",
    )
    parser.add_argument("--cookie", help="Optional cookie string to include in the request headers")
    parser.add_argument(
        "--integrations-api-key",
        default="dev-only-token",
        help="API key for authentication",
    )
    parser.add_argument("--run-once", action="store_true", help="Run each endpoint once and exit")
    args = parser.parse_args()

    config = load_config(args.config)

    # Automatically detect required environment variables
    required_env_vars = detect_required_env_vars(config)
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    handle_requests(
        config,
        args.duration,
        args.verbose,
        args.cookie,
        args.integrations_api_key,
        args.run_once,
    )
