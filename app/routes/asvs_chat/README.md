# ASVS Chat Integration

This integration provides services for chatting with ASVS CSV data using pandas and an LLM.

## Endpoints

- POST /experience/asvs_chat/ask/invoke
  Invokes the Experience API to answer a question based on the provided ASVS CSV data.

- POST /system/asvs_chat/info/invoke
  Invokes the System API to provide information about the ASVS CSV data.

## Testing the integration locally

### Chat with ASVS CSV - Experience API

This endpoint allows you to ask questions about ASVS CSV data using natural language. Only a query is provided as the ASVS content is contained within the router.

```bash
curl --location --request POST \
    'http://localhost:8080/experience/asvs_chat/ask/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "query": "What is the average age?",
      "csv_content": "name,age,city\nJohn Doe,29,New York\nJane Smith,34,Los Angeles\nAlice Johnson,25,Houston\nBob Brown,40,Houston"
    }'
```

URL to a CSV or XLSX file:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/asvs_chat/ask/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "query": "What is the average age?",
      "file_url": "https://example.com/data.csv"
    }'
```

File upload:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/asvs_chat/ask/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "query": "What is the average age?",
      "file_path": "path/to/your/local/file.csv"
    }'
```

### Get ASVS Info - System API

This endpoint provides basic information about the CSV data.

Example with a file URL:

```bash
curl --location --request POST \
    'http://localhost:8080/system/asvs_chat/info/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "file_url": "https://example.com/data.csv"
    }'
```

To nicely format the information returned on the CSV, use:

```bash
curl --location --request POST \
    'http://localhost:8080/system/asvs_chat/info/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "file_url": "https://example.com/data.csv"
    }' | jq '.response[].message | fromjson | .'
```
