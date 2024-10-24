# Website Content Retriever Service

> Author: Mihai Criveti

This service retrieves the content of a website and converts it to plain text. It provides both an Experience API for general queries and a System API for direct content retrieval.

## Endpoints

- **POST /retriever_website/invoke**: Invokes the Experience API to retrieve website content based on a URL.
- **POST /system/retriever_website/transformers/url_to_text/invoke**: Invokes the System API to directly retrieve and convert website content to plain text.

## Testing the integration locally

### Website Content Retriever - Experience API

This is an example of an Experience Level API that will retrieve and process website content.

```bash
curl --location --request POST \
    'http://localhost:8080/retriever_website/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "url": "https://example.com"
    }'
```

### System API

This is an example of a System Level API that will directly retrieve and convert website content to plain text.

```bash
curl --location --request POST \
    'http://localhost:8080/system/retriever_website/transformers/url_to_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "url": "https://example.com"
    }'
```

## Response Format

Both APIs return a response in the following format:

```json
{
  "status": "success",
  "invocationId": "unique-uuid",
  "response": [
    {
      "message": "Retrieved text content...",
      "type": "text"
    }
  ]
}
```

## Error Handling

If there's an error processing the request, the API will return an appropriate HTTP status code along with an error message. For example:

```json
{
  "detail": "Failed to retrieve website content"
}
```

## Integration with LangChain

The `retriever_website_tool.py` file provides a Tool that can be easily integrated into your existing LangChain agent configuration:

```python
from app.routes.retriever_website.tools.retriever_website_tool import retriever_website_tool

tools = [
    # ... other tools ...
    retriever_website_tool,
    # ... other tools ...
]

# Use these tools in your agent setup
```

## Dependencies

This service requires the following Python packages:

- fastapi
- httpx
- beautifulsoup4
- langchain

You can install these dependencies using pip:

```bash
pip install fastapi httpx beautifulsoup4 langchain
```

## Running the Service

To run the service locally, use the following command:

```bash
uvicorn main:app --reload
```

Replace `main` with the name of your main FastAPI application file if it's different.

## Note

This service is designed to work with text-based website content. It may not accurately process websites with complex JavaScript-rendered content or those that require authentication.
```

This README provides an overview of the Website Content Retriever service, including how to use both the Experience and System APIs, the expected response format, error handling, integration with LangChain, dependencies, and how to run the service. You can adjust the content as needed to fit your specific implementation or add any additional information that might be relevant to your users.
