# Simplified Template Execution Integration

This integration allows you to execute pre-defined Jinja2 templates using various Language Models (LLMs). It supports both parallel and series execution of multiple templates, with the ability to maintain conversational context.

## Setup

1. Ensure you have the required dependencies installed:
   ```
   fastapi
   pydantic
   jinja2
   ```

2. Place the integration code in your FastAPI application directory.

3. Create a `templates` directory in the same directory as your FastAPI application.

4. Add your Jinja2 templates to the `templates` directory:
   - `user_story.j2`
   - `coder.j2`

## Usage

To use this integration, send a POST request to the `/system/templates/execute/invoke` endpoint with the following JSON structure:

```json
{
  "templates": [
    {
      "template_name": "template_name_without_extension",
      "variables": {
        "context": "Your context here"
      }
    }
  ],
  "execution_mode": "parallel_or_series",
  "llm_override": ["optional_model_host", "optional_model_name"]
}
```

### Example 1: Generating a User Story

```bash
curl --location --request POST 'http://localhost:8080/system/templates/execute/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "templates": [
             {
                 "template_name": "user_story",
                 "variables": {
                     "context": "We need a feature that allows users to reset their passwords if they forget them."
                 }
             }
         ],
         "llm_override": ["AZURE_OPENAI", "gpt-4"]
     }'
```

### Example 2: Generating Code

```bash
curl --location --request POST 'http://localhost:8080/system/templates/execute/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "templates": [
             {
                 "template_name": "coder",
                 "variables": {
                     "context": "Create a function that sends a password reset email to a user."
                 }
             }
         ],
         "execution_mode": "parallel",
         "llm_override": ["AZURE_OPENAI", "gpt-4"]
     }'
```

### Example 3: Combining Multiple Templates

You can also execute multiple templates in a single request:

```bash
curl --location --request POST 'http://localhost:8080/system/templates/execute/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "templates": [
             {
                 "template_name": "user_story",
                 "variables": {
                     "context": "We need a feature that allows users to reset their passwords if they forget them."
                 }
             },
             {
                 "template_name": "coder",
                 "variables": {
                     "context": "Create a function that sends a password reset email to a user."
                 }
             }
         ],
         "execution_mode": "series",
         "llm_override": ["AZURE_OPENAI", "gpt-4"]
     }'
```

This example will generate a user story followed by the corresponding code. In series mode, the output of the user story template will be added to the context for the code generation.

## Notes

- The `template_name` should be specified without the `.j2` extension.
- The `execution_mode` can be either "parallel" or "series". In series mode, the output of each template is added to the context for the next template.
- The `llm_override` is optional and can be used to specify a different LLM than the default.