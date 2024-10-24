# scribeflow

> Author: Mihai Criveti

This module handles the routing for scribeflow.

Integrate with Scribeflow

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/scribeflow/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "input": "test" }
}'
```
