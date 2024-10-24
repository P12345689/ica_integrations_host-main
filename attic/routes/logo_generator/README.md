# logo_generator

> Author: Mihai Criveti

This module handles the routing for logo_generator.

Generates a logo for marketing purpuse

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/logo_generator/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "input": "test" }
}'
```
