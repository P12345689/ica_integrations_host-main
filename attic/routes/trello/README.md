# trello

> Author: Mihai Criveti

This module handles the routing for trello.

Trello integration

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/trello/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "input": "test" }
}'
```
