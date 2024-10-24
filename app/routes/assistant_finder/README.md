# Assistant Finder

> Author: Mihai Criveti

Assistant Finder is a FastAPI application that finds the most suitable assistants based on the input description.

It uses cosine similarity and a language model to rank and recommend the best assistants.

## Endpoints

- **POST /assistant_finder/invoke**
  Invokes the assistant recommendation process. It expects a JSON payload with a `description` and optional `tags` and `roles`.

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/assistant_finder/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
    "description": "I need help with data analysis",
    "tags": "SDLC Assistants",
    "roles": "Software Developer"
  }'
```
