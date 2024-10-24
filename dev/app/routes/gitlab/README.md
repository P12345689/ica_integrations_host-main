# gitlab

> Author: Mihai Criveti

This module handles the routing for gitlab.

GitLab integration

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/gitlab/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "input": "test" }
}'
```
