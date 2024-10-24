# graphql_mapper_function Integration

This integration provides functionality for integration provides a rag solution for ingesting graphql schemas. Users can input a rest response and the matching mapper function is created.

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

1. Update the generate_timestamp function in graphql_mapper_function_router.py to implement your desired functionality.
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

### POST /system/graphql_mapper_function/generate_graphql_mapper_function_file/invoke

Generates a graphql_mapper_function, creates a file containing the graphql_mapper_function, zips the file, and returns both a formatted response and the URL to download the zip file.

```bash
curl --location --request \
  POST 'http://localhost:8080/system/graphql_mapper_function/generate_mapper_function/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
      "input": {
          "query": "{ }"
      }
  }'
```

```bash
curl --location --request POST 'http://localhost:8080/system/graphql_mapper_function/generate_mapper_function/invoke' \
--header 'Content-Type: application/json' \
--header 'Integrations-API-Key:  \
--data-raw '{
    "input": {
        "query": "{ \"contents\": { \"identifier\": \"c/passive-components/capacitors/aluminium-electrolytic-capacitors/miscellaneous-aluminium-electrolytic-capacitors\", \"tokenId\": \"1000000000000010354\", \"languageId\": 44, \"tokenType\": \"CategoryToken\" }, \"altContents\": [ { \"identifier\": \"c/passive-components/capacitors/aluminium-electrolytic-capacitors/miscellaneous-aluminium-electrolytic-capacitors\", \"tokenId\": \"1000000000000010354\", \"languageId\": 44, \"altLanguageId\": 44, \"tokenType\": \"CategoryToken\" } ] }"
    }
}'
```
