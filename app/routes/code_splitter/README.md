# code_splitter

> Author: Mihai Criveti, M S Rahul Saj (GenAI Code Splitter)

This module handles the routing for code_splitter.

Split code into relevant chunks and call Agents to transform the code

## Requirements

To use this integration, follow these additional steps:

1. Ensure you have the required dependencies installed: `pip install -r app/routes/code_splitter/requirements.txt`

## Endpoints

- **POST /code_splitter/invoke**
  Invokes the code splitter process. It expects a JSON payload with substituted code, `language`, `max_chunk_size`, `request_type` and an optional `model`.

There are four possible inputs for `request_type`: `unit_test`, `split`, `count_tokens` or `business_rules`


## Generate unit tests

```bash
curl --silent --location --request POST \
  'http://localhost:8080/code_splitter/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data "$(jq -n --arg code "$(cat *.java)" '{
    code: $code,
    language: "java",
    max_chunk_size: 6000,
    model: "Llama3.1 70b Instruct",
    request_type: "unit_test"
  }')" | jq
```

## Split the code

```bash
curl --silent --location --request POST \
  'http://localhost:8080/code_splitter/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data "$(jq -n --arg code "$(cat *.java)" '{
    code: $code,
    language: "java",
    max_chunk_size: 6000,
    request_type: "split"
  }')" | jq
```

## Count tokens

```bash
curl --silent --location --request POST \
  'http://localhost:8080/code_splitter/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data "$(jq -n --arg code "$(cat *.java)" '{
    code: $code,
    language: "java",
    max_chunk_size: 6000,
    request_type: "count_tokens"
  }')" | jq
```

## Generate business rules

```bash
curl --silent --location --request POST \
  'http://localhost:8080/code_splitter/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data "$(jq -n --arg code "$(cat *.java)" '{
    code: $code,
    language: "java",
    max_chunk_size: 6000,
    model: "Llama3.1 70b Instruct",
    request_type: "business_rules"
  }')" | jq
```


# Using the CLI

```
./app/routes/code_splitter/ica_code_forge.py --verbose \
  test/test-concurrency.py -m 300 -l python -p -o out2
```


---
# GenAI code_splitter


This module is used to split Java Code based on its programming constructs and token size.

## Features
* Java Code Splitter.
* Java X to Java Y Conversion.
* Spring Boot to Quarkus Conversion.
* Business Rules Generation from Java code.

## Release Notes
1.0.0

Initial release of :
  * Use cases: 
    * Java to Business Rule.
    * Spring Boot to Quarkus.
    * Java X to Java Y.

  * Response mode supported: 
    * `chunk_only`:  return chunks of input code.
    * `process_only`: return only the generated result, in case of generated code, return merged/unchunked code.
    * `chunk_and_process`: return both chunk and result together.

  * Genai Platform: 
    * `ica`: uses assistants available on ICA to generate result.
    * `genai`: uses prompts deployed in GenAI Adapter.

  * Response Format:
    * text

  * Chunking Mode:
    * in memory


## Usage

```bash
curl --silent --location --request POST \
  'http://localhost:8080/code_splitter/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data "$(jq -n --arg code "$(cat *.java)" '{
    code: $code,
    request_type: "custom_genai",
    response_mode: "chunk_and_process",
    genai_platform: "ica",
    response_format: "text",
    "usecase_id": "Java_X_to_Java_Y_Conversion",
    "transport_mode": "https|https",
    "chunking_mode": "memory"
  }')" | jq
```