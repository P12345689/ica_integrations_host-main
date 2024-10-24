# Test

> Author: Mihai Criveti

This is a test integration that returns back any provided parameters

## Testing the integration locally


```bash
curl --location --request POST 'http://localhost:8080/summarize_sentences/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "input": "test" }
}'
```
