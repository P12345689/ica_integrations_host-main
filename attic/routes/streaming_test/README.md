# streaming_test

> Author: Mihai Criveti

This module handles the routing for streaming_test.

Streaming test

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/streaming_test/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "input": "test" }
}'
```
