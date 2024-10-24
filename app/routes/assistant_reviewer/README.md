# Assistant Reviewer

> Author: Mihai Criveti

This module handles the routing for assistant_reviewer.

Review assistant output and provide feedback

## Endpoints

- **POST /assistant_reviewer/invoke**
  Invokes the assistant reviewer process. It expects a JSON payload with an `assistant_id`, `assistant_input` and `assistant_output`.

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/assistant_reviewer/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{ "assistant_id": "3903", "assistant_input": "test input", "assistant_output": "test output" }'
```
