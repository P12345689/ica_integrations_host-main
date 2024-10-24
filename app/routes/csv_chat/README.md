# CSV Chat Integration

This integration provides services for chatting with CSV data using pandas and an LLM. It supports various input formats including direct CSV content, URLs to CSV or XLSX files, and file uploads.

## Endpoints

- POST /experience/csv_chat/ask/invoke
  Invokes the Experience API to answer a question based on the provided CSV data.

- POST /system/csv_chat/info/invoke
  Invokes the System API to provide information about the CSV data.

## Testing the integration locally

### Chat with CSV - Experience API

This endpoint allows you to ask questions about CSV data using natural language. You can provide the data in three ways:

1. Direct CSV content:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/csv_chat/ask/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "query": "What is the average age?",
      "csv_content": "name,age,city\nJohn Doe,29,New York\nJane Smith,34,Los Angeles\nAlice Johnson,25,Houston\nBob Brown,40,Houston"
    }'
```

2. URL to a CSV or XLSX file:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/csv_chat/ask/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "query": "What is the average age?",
      "file_url": "https://example.com/data.csv"
    }'
```

3. File upload

```bash
curl --location --request POST \
    'http://localhost:8080/experience/csv_chat/ask/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "query": "What is the average age?",
      "file_path": "path/to/your/local/file.csv"
    }'
```

### Get CSV Info - System API

This endpoint provides basic information about the CSV data. You can use the same three methods to provide the data as in the Chat with CSV endpoint.

Example with direct CSV content:

```bash
curl --location --request POST \
    'http://localhost:8080/system/csv_chat/info/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "csv_content": "name,age,city\nJohn Doe,29,New York\nJane Smith,34,Los Angeles\nAlice Johnson,25,Houston\nBob Brown,40,Houston"
    }'
```

To nicely format the information returned on the CSV, use:

```bash
curl --location --request POST \
    'http://localhost:8080/system/csv_chat/info/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "csv_content": "name,age,city\nJohn Doe,29,New York\nJane Smith,34,Los Angeles\nAlice Johnson,25,Houston\nBob Brown,40,Houston"
    }' | jq '.response[].message | fromjson | .'
```
