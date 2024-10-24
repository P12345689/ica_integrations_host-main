# Batch Execution Integration

> Author: Mihai Criveti

This integration provides services for executing batches of prompts, potentially using different models or assistants, and returning the results in both XLSX and CSV formats.

## Configuration

The integration can be configured using the following environment variables:

- `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME`: Default model to use if not specified (default: "Llama3.1 70b Instruct")
- `DEFAULT_MAX_THREADS`: Maximum number of threads for concurrent execution (default: 4)
- `MAX_EXECUTIONS_PER_BATCH`: Maximum number of executions allowed in a single batch (default: 100)
- `MAX_PROMPT_LENGTH`: Maximum length of a single prompt in characters (default: 1000)
- `MAX_CONCURRENT_BATCHES`: Maximum number of batches that can be processed concurrently (default: 5)
- `EXECUTION_TIMEOUT`: Maximum time in seconds for a single prompt execution (default: 300)

To set these environment variables, you can use the following commands before running the application:

```bash
export ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME="Llama3.1 70b Instruct"
export DEFAULT_MAX_THREADS=4
export MAX_EXECUTIONS_PER_BATCH=100
export MAX_PROMPT_LENGTH=1000
export MAX_CONCURRENT_BATCHES=5
export EXECUTION_TIMEOUT=300
```

Or, you can create a `.env` file in the root directory of the project with the following content:

```
ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME=Llama3.1 70b Instruct
DEFAULT_MAX_THREADS=4
MAX_EXECUTIONS_PER_BATCH=100
MAX_PROMPT_LENGTH=1000
MAX_CONCURRENT_BATCHES=5
EXECUTION_TIMEOUT=300
```

## Endpoints

### 1. Process CSV (Synchronous)

- **POST** `/system/batch_execution/process_csv/invoke`

  Processes a CSV file containing prompts and models/assistants without executing them. Returns the path to an XLSX file with empty result columns.

#### Example:

```bash
curl --location --request POST 'http://localhost:8080/system/batch_execution/process_csv/invoke' \
--header 'Content-Type: application/json' \
--header 'Integrations-API-Key: dev-only-token' \
--data-raw '{
    "csv_content": "prompt,model\nWhat is the capital of France?,Granite 13B V2.1\nWhat is 2+2?,Llama3 8B Instruct"
}'
```

### 2. Execute Batch (Asynchronous)

- **POST** `/experience/batch_execution/execute_batch/invoke`

  Executes a batch of prompts asynchronously. Returns an invocation ID for checking status and retrieving results.

#### Example:

```bash
curl --location --request POST 'http://localhost:8080/experience/batch_execution/execute_batch/invoke' \
--header 'Content-Type: application/json' \
--header 'Integrations-API-Key: dev-only-token' \
--data-raw '{
    "executions": [
        {
            "prompt": "What is the capital of France?",
            "model": "Granite 13B V2.1"
        },
        {
            "prompt": "What is 2+2?",
            "model": "Llama3 8B Instruct"
        }
    ]
}'
```

### 3. Retrieve Execution Results

- **POST** `/system/batch_execution/results`

  Retrieves the status and results of a batch execution. If the execution is completed, it provides both a link to download the XLSX file and the CSV content.

#### Example:

```bash
curl --location --request POST 'http://localhost:8080/system/batch_execution/results/' \
--header 'Content-Type: application/json' --header 'Integrations-API-Key: dev-only-token' \
-d '{"invocation_id": "your-invocation-id"}'
```

#### Response:

```json
{
    "status": "completed",
    "invocationId": "your-invocation-id",
    "message": "Execution completed successfully.",
    "xlsx_url": "http://localhost:8080/public/batch_execution_results/batch_execution_uuid.xlsx",
    "csv_content": "prompt,model,result\nWhat is the capital of France?,Granite 13B V2.1,Paris\nWhat is 2+2?,Llama3 8B Instruct,4"
}
```

### 4. Download XLSX File

- **GET** `/public/batch_execution_results/{file_name}`

  Downloads the XLSX file generated from a completed batch execution.

#### Example:

```bash
curl --location --request GET 'http://localhost:8080/public/batch_execution_results/batch_execution_uuid.xlsx' \
--header 'Integrations-API-Key: dev-only-token' \
--output result.xlsx
```

## Using Variables in Prompts

You can use variables in your prompts to reference the output of previous executions. Use the format `${output.n}` where `n` is the index of the previous execution (1-based).

Example:

```json
{
    "executions": [
        {
            "prompt": "What is the capital of France?",
            "model": "Granite 13B V2.1"
        },
        {
            "prompt": "What is the population of ${output.1}?",
            "model": "Llama3 8B Instruct"
        }
    ]
}
```

In this example, the second prompt will use the output of the first execution.

## Error Handling

If an error occurs during execution, it will be reflected in the status and results. Always check the status when retrieving results.

## Note on Asynchronous Processing

Asynchronous batch executions are processed in the background. Use the results endpoint to check the status and retrieve results when processing is complete.

## File Storage

XLSX files are stored in the `public/batch_execution_results` directory and can be accessed via the provided URL in the results response.

## Safety Measures

- The integration limits the number of executions per batch to prevent overload.
- There's a maximum prompt length to prevent excessively large inputs.
- The number of concurrent batch executions is limited to manage system resources.
- Each prompt execution has a timeout to prevent hanging operations.
