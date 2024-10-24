# Assistant Executor

> Author: Mihai Criveti

This module handles the routing for assistant_executor.

Executes an assistant with the provided prompt. Used as a tool by other integrations.

## Endpoints

- **POST /system/assistant_executor/retrievers/assistant/invoke**
  Invokes the assistant executor process. It expects a JSON payload with an `assistant_id` and a `prompt`.


## Testing the integration locally

```bash
curl --silent --location --request POST 'http://localhost:8080/system/assistant_executor/retrievers/assistant/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{ "assistant_id":"3903", "prompt": "app to open car trunk with face" }'
```
