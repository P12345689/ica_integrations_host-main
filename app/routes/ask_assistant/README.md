# Ask Assistant Integration

> Maintainer: Mihai Criveti

This integration provides services for retrieving assistant information and answering questions about assistants.

## Endpoints

- POST /system/assistant/retrievers/get_assistants/invoke
  Invokes the System API to retrieve and filter assistants based on given criteria.

- POST /experience/assistant/ask_assistant/invoke
  Invokes the Experience API to answer questions about assistants using an LLM.

## Testing the integration locally

### Get Assistants - System API

This endpoint retrieves and filters assistants based on the provided criteria. Here are various examples:

1. Get all assistants with the "unified" tag:

```bash
curl --location --request POST \
    'http://localhost:8080/system/assistant/retrievers/get_assistants/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["unified"],
        "refresh": true
    }'
```

2. Get assistants with the "Developer" tag:

```bash
curl --location --request POST \
    'http://localhost:8080/system/assistant/retrievers/get_assistants/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["Developer"],
        "refresh": true
    }'
```

3. Get assistants with the "Software Developer" role:

```bash
curl --location --request POST \
    'http://localhost:8080/system/assistant/retrievers/get_assistants/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "roles": ["Software Developer"],
        "refresh": true
    }'
```

4. Search for assistants containing "Python" in their title or description:

```bash
curl --location --request POST \
    'http://localhost:8080/system/assistant/retrievers/get_assistants/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "search_term": "Python",
        "refresh": true
    }'
```

5. Get a specific assistant by ID:

```bash
curl --location --request POST \
    'http://localhost:8080/system/assistant/retrievers/get_assistants/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "assistant_id": "3909",
        "refresh": true
    }'
```

### Ask Assistant - Experience API

This endpoint allows you to ask questions about assistants using an LLM. Here are various examples:

6. Ask about assistants for generating Python code:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/assistant/ask_assistant/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "Which assistants can help me generate Python code?",
        "tags": ["Developer", "Code Generation"]
    }'
```

7. Inquire about assistants for creating user stories:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/assistant/ask_assistant/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "Is there an assistant that can help create user stories?",
        "tags": ["Business Analyst"]
    }'
```

8. Ask about assistants for generating test cases:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/assistant/ask_assistant/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "Which assistant can help me generate test cases for Python code?",
        "tags": ["Python", "Testing"]
    }'
```

9. Inquire about assistants for working with Mermaid.js:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/assistant/ask_assistant/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "Is there an assistant that can help with Mermaid.js syntax?",
        "tags": ["Mermaid.js"]
    }'
```

10. Ask about the capabilities of a specific assistant:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/assistant/ask_assistant/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "What are the capabilities of the assistant with ID 3903?",
        "assistant_id": "3903"
    }'
```
