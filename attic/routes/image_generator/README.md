# image_generator

> Author: Mihai Criveti

This module handles the routing for image_generator.

Generate images using AI

## Testing the integration locally

```bash
curl --location --request POST 'http://localhost:8080/image_generator/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "input": "test" }
}'
```
