# Monday.com Integration

This integration provides services for interacting with the Monday.com API and answering questions about Monday.com data using natural language processing.

## Endpoints

- POST /system/monday/api/invoke
  Invokes the System API to make direct calls to the Monday.com GraphQL API.

- POST /experience/monday/ask/invoke
  Invokes the Experience API to answer questions about Monday.com data using natural language.

## Environment Variables

- `MONDAY_API_TOKEN`: Your Monday.com API token (required)
- `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME`: The default model to use for NLP tasks (default: "Llama3.1 70b Instruct")
- `DEFAULT_MAX_THREADS`: Maximum number of threads for concurrent operations (default: 4)

## Testing the integration locally

### Make a Monday.com API Call - System API

This endpoint allows you to make direct GraphQL queries to the Monday.com API.

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{"query":"query { boards (ids: 5663387293) {name}}"}'
```

### Ask About Monday.com Data - Experience API

This endpoint allows you to ask natural language questions about your Monday.com data.

```bash
curl --location --request POST \
    'http://localhost:8080/experience/monday/ask/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "List all deals owned by Mihai"
    }'
```

Note: Make sure to set the `MONDAY_API_TOKEN` environment variable with your Monday.com API token before running these examples.


## Other examples

Here are several examples of using the Monday.com API to list items in your board with different filters and queries:

1. List all items in a specific board:

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items { id name } } }"
    }'
```

2. List items owned by a specific person (replace PERSON_ID with the actual ID):

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items(limit: 100) { id name column_values(ids: [\"person\"]) { text } } } }",
        "variables": {
            "person_id": "PERSON_ID"
        }
    }'
```

3. List items with a specific status (e.g., "Done"):

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items(limit: 100) { id name column_values(ids: [\"status\"]) { text } } } }"
    }'
```

4. List items created in the last 7 days:

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items(newest_first: true, limit: 100) { id name created_at } } }"
    }'
```

5. List items with high priority:

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items(limit: 100) { id name column_values(ids: [\"priority\"]) { text } } } }"
    }'
```

6. List items with specific tags:

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items(limit: 100) { id name column_values(ids: [\"tags\"]) { text } } } }"
    }'
```

7. List items sorted by a specific column (e.g., due date):

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items(limit: 100, order_by: { column_id: \"date\", direction: asc }) { id name column_values(ids: [\"date\"]) { text } } } }"
    }'
```

8. List items with multiple conditions (e.g., high priority and assigned to a specific person):

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items(limit: 100) { id name column_values(ids: [\"priority\", \"person\"]) { text } } } }"
    }'
```

9. List items and include specific custom fields:

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { items(limit: 100) { id name column_values(ids: [\"text\", \"numbers\", \"date\"]) { text } } } }"
    }'
```

10. List subitems of a specific item:

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { items(ids: ITEM_ID) { subitems { id name } } }"
    }'
```

Remember to replace `5663387293` with your actual board ID, and replace any column IDs (like "person", "status", "priority", etc.) with the actual column IDs from your Monday.com board. You may need to query the board's structure first to get these IDs if you're not sure what they are.

To get information about your board's structure, including column IDs, you can use this query:

```bash
curl --location --request POST \
    'http://localhost:8080/system/monday/api/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "query { boards(ids: 5663387293) { columns { id title type } } }"
    }'
```
