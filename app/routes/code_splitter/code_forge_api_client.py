#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti, M S Rahul Saj
Description: Command-line client for the Code Splitter API.

This script provides a command-line interface for interacting with the Code Splitter API.
It allows users to split code into chunks, generate unit tests or business rules, and count tokens in files.

The API URL and API key can be provided as command-line arguments or set as environment variables.

Usage:
    python code_splitter_client.py --api-url <api_url> --api-key <api_key> --code <code_file> --language <language>
                                   [--max-chunk-size <max_chunk_size>] [--model <model>]
                                   [--request-type <request_type>] [--output <output_file>]

    python code_splitter_client.py --api-url <api_url> --api-key <api_key> --count-tokens <file1> <file2> ...

Arguments:
    --api-url (str): URL of the Code Splitter API.
    --api-key (str): API key for authentication.
    --code (str): Path to the code file to be processed.
    --language (str): Programming language of the code.
    --max-chunk-size (int, optional): Maximum size of each code chunk (default: 500).
    --model (str, optional): Name or ID of the model to use for generating unit tests or business rules.
    --request-type (str, optional): Type of request. Options are 'unit_test', 'business_rules', 'split', 'count_tokens' (default: 'unit_test').
    --output (str, optional): Path to the output file for saving the API response.
    --count-tokens (str, optional): Path(s) to the file(s) for counting tokens. Supports globbing.

Examples:
    python code_splitter_client.py --api-url http://localhost:8080 --api-key abc123 --code example.py --language python --max-chunk-size 1000 --model "Llama3.1 70b Instruct" --request-type unit_test --output response.json
    python code_splitter_client.py --api-url http://localhost:8080 --api-key abc123 --count-tokens file1.py file2.py


--------

Description: Command-line client for the GenAI Code Splitter API.

This script also provides a command-line interface for interacting with the GenAI Code Splitter API.
It allows users to split code into chunks, chunk and process and process only for Java to Business Rules, SpringBoot to Quarkus, Java X to Java Y Conversion.

The API URL and API key can be provided as command-line arguments or set as environment variables.

Usage:
    python code_splitter_client.py --api-url <api_url> --api-key <api_key> --code <code_file> --request-type <request_type> --usecase-id <usecase_id> [--response-mode <response_mode>]
                                   [--genai-platform <genai_platform>] [--transport-mode <transport_mode>] [--chunking-mode <chunking_mode>] [--response-format <response_format>] 

   
Arguments:
    --api-url (str): URL of the Code Splitter API.
    --api-key (str): API key for authentication.
    --code (str): Path to the code file to be processed.
    --request-type (str): Type of request. Options are 'custom_genai', 'unit_test', 'split'.
    --usecase-id (str): ID of the use case to trigger such as Java_to_Business_Rule, Java_X_to_Java_Y_Conversion, SpringBoot_to_Quarkus.
    --response-mode (str, optional): Type of the reponse that will be generated such as chunk or processed.
    --genai-platform (str, optional): Platform to use for LLM execution (ica, genai).
    --transport-mode (str, optional): Mode of transport.
    --chunking-mode (str, optional): Mode of chunking.
    --response-format (str, optional): Format of the response.

Examples:
    python code_splitter_client.py --api-url http://localhost:8080/code_splitter/invoke --api-key abc123 --code example.java --request-type custom_genai --usecase-id Java_to_Business_Rule
"""

import argparse
import glob
import json
import os

import requests

# Environment variables for API URL and API key
API_URL_ENV = "CODE_SPLITTER_API_URL"
API_KEY_ENV = "CODE_SPLITTER_API_KEY"


def send_request(api_url, api_key, code, language, max_chunk_size, model, request_type):
    headers = {"Content-Type": "application/json", "Integrations-API-Key": api_key}
    data = {
        "code": code,
        "language": language,
        "max_chunk_size": max_chunk_size,
        "model": model,
        "request_type": request_type,
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

def send_request_to_genai(api_url, api_key, code, request_type, response_mode, genai_platform, response_format, usecase_id, transport_mode, chunking_mode):
        headers = {"Content-Type": "application/json", "Integrations-API-Key": api_key}
        data = {
            "code": code,
            "request_type": request_type,
            "response_mode": response_mode,
            "genai_platform": genai_platform,
            "response_format": response_format,
            "usecase_id": usecase_id,
            "transport_mode": transport_mode,
            "chunking_mode": chunking_mode
        }
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()



def count_tokens(api_url, api_key, files):
    headers = {"Content-Type": "application/json", "Integrations-API-Key": api_key}
    results = {}
    for file in files:
        with open(file, "r") as f:
            code = f.read()
        data = {
            "code": code,
            "language": os.path.splitext(file)[1][1:],
            "request_type": "count_tokens",
        }
        response = requests.post(api_url, headers=headers, json=data)
        results[file] = response.json()
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Code Splitter API Command-Line Client"
    )
    parser.add_argument("--api-url", help="URL of the Code Splitter API")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--code", help="Path to the code file")
    parser.add_argument("--language", help="Programming language of the code")
    parser.add_argument(
        "--max-chunk-size",
        type=int,
        default=500,
        help="Maximum size of each code chunk (default: 500)",
    )
    parser.add_argument(
        "--model",
        help="Name or ID of the model to use for generating unit tests or business rules",
    )
    parser.add_argument(
        "--request-type",
        choices=["unit_test", "business_rules", "split", "count_tokens", "custom_genai"],
        help="Type of request (default: unit_test)",
    )
    parser.add_argument(
        "--output", help="Path to the output file for saving the API response"
    )
    parser.add_argument(
        "--count-tokens",
        nargs="+",
        help="Path(s) to the file(s) for counting tokens. Supports globbing.",
    )
    parser.add_argument(
        "--response-mode",
        choices=["chunk_only", "process_only", "chunk_and_process"],
        default="chunk_and_process",
        help="Output format should be either with chunk, llm_response, or both (default: chunk_and_process)",
    )
    parser.add_argument(
        "--genai-platform",
        choices=["ica", "genai"],
        default="ica",
        help="GenAI Platform to use for LLM response (default: ica)",
    )
    parser.add_argument(
        "--usecase-id",
        choices=["SpringBoot_to_Quarkus", "Java_X_to_Java_Y_Conversion", "Java_to_Business_Rule"],
        help="Use case ID to choose for GenAI Code Splitter",
    )
    parser.add_argument(
        "--transport-mode",
        choices=["https|https", "mq|mq"],
        default="https|https",
        help="Mode of transport for job creation",
    )
    parser.add_argument(
        "--chunking-mode",
        choices=["memory", "filesystem"],
        default="memory",
        help="Mode used for chunking",
    )
    parser.add_argument(
        "--response-format",
        choices=["text", "zip", "md"],
        default="text",
        help="Type of the response (default: text)",
    )
    

    args = parser.parse_args()

    api_url = args.api_url or os.getenv(API_URL_ENV)
    api_key = args.api_key or os.getenv(API_KEY_ENV)

    if not api_url:
        raise ValueError(
            f"API URL not provided. Set the {API_URL_ENV} environment variable or use the --api-url argument."
        )
    if not api_key:
        raise ValueError(
            f"API key not provided. Set the {API_KEY_ENV} environment variable or use the --api-key argument."
        )

    if args.count_tokens:
        files = []
        for path in args.count_tokens:
            if "*" in path:
                files.extend(glob.glob(path))
            else:
                files.append(path)
        results = count_tokens(api_url, api_key, files)
        print(json.dumps(results, indent=2))
        return

    if not args.code:
        raise ValueError(
            "Code file not provided. Use the --code argument to specify the code file."
        )
    
    with open(args.code, "r") as file:
        code = file.read()

    if request_type:= args.request_type:
        if request_type.startswith("custom_genai"):
            response = send_request_to_genai(
                api_url,
                api_key,
                code,
                args.request_type,
                args.response_mode,
                args.genai_platform,
                args.response_format,
                args.usecase_id,
                args.transport_mode,
                args.chunking_mode
            )
            print(json.dumps(response, indent=2))
            return

        

    if not args.language:
        raise ValueError(
            "Language not provided. Use the --language argument to specify the programming language."
        )



    response = send_request(
        api_url,
        api_key,
        code,
        args.language,
        args.max_chunk_size,
        args.model,
        args.request_type,
    )

    if args.output:
        with open(args.output, "w") as file:
            json.dump(response, file, indent=2)
        print(f"Response saved to {args.output}")
    else:
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
