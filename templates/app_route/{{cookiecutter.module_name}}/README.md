# {{ cookiecutter.module_name }} Integration

This integration provides functionality for {{ cookiecutter.description }}.

## Integration Development Guidelines

When developing or modifying this integration, please adhere to the following guidelines:

1. Use Pydantic v2 models to validate all inputs and outputs.
2. Define all functions as async where appropriate.
3. Provide full docstring coverage in Google docstring format for all functions and classes.
4. Implement comprehensive unit tests, including doctests where applicable.
5. Use Jinja2 templates for LLM prompts and response formatting.
6. Implement proper error handling and logging throughout the integration.
7. Use environment variables for configuration where appropriate.
8. Follow PEP 8 style guidelines and maintain consistent code formatting.
9. Keep the README updated with any changes to usage or functionality.

### Customization

1. Update the generate_timestamp function in {{ cookiecutter.module_name }}_router.py to implement your desired functionality.
2. Modify the Pydantic models (TimestampInputModel, ExperienceInputModel) to match your input requirements.
3. Update the Jinja2 templates in the templates directory to change the LLM prompts and response formatting.
4. Add any additional routes or helper functions as needed for your integration.
5. Remember to update this README with any changes to the API endpoints or usage instructions.

## Usage

To use this integration, follow these steps:

1. Ensure you have the required dependencies installed. Update `pyproject.toml` accordingly.
2. Set up the necessary environment variables (e.g., `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME`, `DEFAULT_MAX_THREADS`).
3. Include this module in your FastAPI application.

## API Endpoints

### POST /system/{{ cookiecutter.module_name }}/generate_timestamp/invoke

Generates a timestamp using the system's date command.

```bash
curl -X POST "http://localhost:8080/system/{{ cookiecutter.module_name }}/generate_timestamp/invoke" \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"format": "%Y-%m-%d %H:%M:%S"}'
```

```json
{
  "status": "success",
  "invocationId": "f3589037-8ade-4049-b9ad-2f2eecda83bc",
  "response": [
    {
      "message": "Generated timestamp: 2024-06-23 19:25:00",
      "type": "text"
    }
  ]
}
```

### POST /experience/{{ cookiecutter.module_name }}/timestamp_experience/invoke

Invokes the {{ cookiecutter.module_name }} timestamp experience, which combines timestamp generation with LLM interaction.

```bash
curl --silent --location --request POST 'http://localhost:8080/experience/{{ cookiecutter.module_name }}/timestamp_experience/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{"query": "What'\''s the current time?"}' | jq
```

```json
{
  "status": "success",
  "invocationId": "a3264395-b542-4127-ad47-772685b1da8a",
  "response": [
    {
      "message": "Here's the response to your query about time or timestamps:\n\nHello there! As of our conversation, the current time is 19:24:25 on June 23rd, 2024. I hope that answers your question! By the way, did you know that June 23rd is also celebrated as International Widow's Day? It's a day to raise awareness about the struggles faced by widows around the world and to promote their rights and dignity. Anyway, I hope you're having a great day so far!\n\nFor reference, the timestamp generated was: 2024-06-23 19:24:25\n\nIs there anything else you'd like to know about time or timestamps?",
      "type": "text"
    }
  ]
}
```

### POST /system/{{ cookiecutter.module_name }}/generate_{{ cookiecutter.module_name }}_file/invoke

Generates a {{ cookiecutter.module_name }}, creates a file containing the {{ cookiecutter.module_name }}, zips the file, and returns both a formatted response and the URL to download the zip file.

```bash
curl --location --request POST 'http://localhost:8080/system/{{ cookiecutter.module_name }}/generate_{{ cookiecutter.module_name }}_file/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{"format": "%Y-%m-%d %H:%M:%S"}'
```

```json
{
  "status": "success",
  "invocationId": "unique-uuid",
  "response": [
      {
          "message": "A {{ cookiecutter.module_name }} file has been generated for you.\n\nGenerated {{ cookiecutter.module_name }}: 2023-06-24 15:30:45\n\nYou can download the ZIP file containing this {{ cookiecutter.module_name }} from the following URL:\nhttp://127.0.0.1:8080/public/{{ cookiecutter.module_name }}/{{ cookiecutter.module_name }}_<uuid>.zip\n\nIs there anything else you would like to know about {{ cookiecutter.module_name }} or file generation?",
          "type": "text"
      },
      {
          "message": "http://127.0.0.1:8080/public/{{ cookiecutter.module_name }}/{{ cookiecutter.module_name }}_<uuid>.zip",
          "type": "text"
      }
  ]
}
```
