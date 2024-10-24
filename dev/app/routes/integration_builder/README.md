# integration_builder

> Author: Mihai Criveti

This module handles the routing for integration_builder.

Generates integrations

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/integration_builder/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "input": "test" }
}'
```
