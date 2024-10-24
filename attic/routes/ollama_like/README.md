# Ollama-like Integration

This integration provides an Ollama-like interface for text generation using the prompt_flow based API.

## Endpoints

- POST /experience/ollama_like/generate/invoke
  Invokes the Experience API to generate text based on the provided prompt and options.

- POST /system/ollama_like/model_info/invoke
  Invokes the System API to get information about the available model.

## Testing the integration locally

### Generate Text - Experience API

This endpoint allows you to generate text using an Ollama-like interface.

```bash
curl --location --request POST \
    'http://localhost:8080/experience/ollama_like/generate/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "model": "Llama3 8B Instruct",
        "prompt": "Write a short story about a robot learning to paint.",
        "system": "You are a creative writing assistant.",
        "context": "The story should be heartwarming and suitable for all ages."
    }'
```

### Get Model Info - System API

This endpoint provides information about the available models.

```bash
curl --location --request POST \
    'http://localhost:8080/system/ollama_like/model_info/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token'
```

## Note

This integration mimics the Ollama API interface but uses the prompt_flow based API under the hood. It currently supports non-streaming text generation without image support.
