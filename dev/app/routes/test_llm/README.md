# Test LLM

> Author: Mihai Criveti

This is a test integration that tests the llm extension

It's also useful as a template

## Testing the integration locally


```bash
curl --location --request POST 'http://localhost:8080/test_llm/invoke' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "model": "Llama2 70B Chat", "prompt": "What is 1+1" }'
```
