# Prompt Integration

> Maintainer: Mihai Criveti

This integration provides services for retrieving and filtering prompts, as well as asking questions about prompts using an LLM.

## Endpoints

- POST /system/prompt/retrievers/get_prompts/invoke
  Invokes the System API to retrieve and filter prompts based on various criteria.

- POST /experience/prompt/ask_prompts/invoke
  Invokes the Experience API to answer questions about prompts using an LLM.

## Testing the integration locally

### Get Prompts - System API

This endpoint allows you to retrieve and filter prompts based on various criteria.

1. Retrieve prompts with a specific id:

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "prompt_id": "35485f84-df28-4b96-8358-bcc1161a386b"
    }'
```

2. Retrieve prompts with specific tags:


```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["Python", "Microservices"]
    }'
```

3. Retrieve prompts for a specific role:

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "roles": ["Software Developer"]
    }'
```

4. Search for prompts containing a specific term:

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "search_term": "best practices"
    }'
```

5. Retrieve prompts with specific visibility:

You can use: PRIVATE, TEAM, PUBLIC, *

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "visibility": "PRIVATE"
    }'
```

6. Retrieve prompts from a specific user:

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "user_email": "crmihai1@ie.ibm.com"
    }'
```

7. Combine multiple filters:

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["Python"],
        "roles": ["Software Developer"],
        "search_term": "best practices",
        "visibility": "TEAM"
    }'
```

8. Using glob patterns and regex:

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["crew.ai"],
        "search_term": "*",
        "visibility": "*"
    }'

curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["crew.ai"],
        "search_term": "^Python.*development$",
        "visibility": "TEAM"
    }'
```

### Ask About Prompts - Experience API

This endpoint allows you to ask questions about prompts using an LLM.

1. Ask about prompts related to a specific topic:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt/ask_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["Python", "Microservices"],
        "query": "What are the common themes in the Python and Microservices prompts?"
    }'
```

2. Ask about best practices for a specific role:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt/ask_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "roles": ["Software Developer"],
        "query": "Summarize the best practices for software development mentioned in these prompts."
    }'
```

3. Ask about prompts from a specific user:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt/ask_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "user_email": "crmihai1@ie.ibm.com",
        "query": "What are the main topics covered in the prompts created by this user?"
    }'
```

## Visibility Filter

The `visibility` parameter supports the following values:
- "PRIVATE": Retrieves only private prompts
- "TEAM": Retrieves only team prompts
- "PUBLIC": Retrieves only public prompts
- "*": Retrieves prompts with any visibility setting

Example:

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["crew.ai"],
        "search_term": "*",
        "visibility": "*"
    }'
```

This will retrieve all prompts with the "crew.ai" tag, regardless of their visibility setting.

## Tag Filtering

The `tags` parameter supports glob patterns for more flexible matching:
- Use `*` to match any number of characters
- Use `?` to match a single character
- Use `[abc]` to match one character in the brackets
- Use `[!abc]` to match any character not in the brackets

Examples:
- `"Python*"`: Matches tags starting with "Python"
- `"*AI*"`: Matches tags containing "AI" anywhere in the name
- `"Data?"`: Matches tags starting with "Data" followed by exactly one character

You can provide multiple tag patterns, and prompts matching any of the patterns will be returned.

Example API call:

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt/retrievers/get_prompts/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "tags": ["^tool:.*$"],
        "search_term": "*",
        "visibility": "*"
    }'
```

This will retrieve all prompts with tags matching the regular expression "^tool:.*$", which means any tag starting with "tool:".
