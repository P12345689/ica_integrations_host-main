# GPT4 Vision

This is the GPT4Vision langchain agent that can be used with integrations in IBM Consulting Assistants.

## Environment Variables

The following environment variables are used in the GPT-4 Vision API integration:

- `GPT4VISION_MODEL_URL`: The URL of the GPT-4 Vision API endpoint. Defaults to "https://essentialsdalle3.openai.azure.com/openai/deployments/essentialsgpt4vision/chat/completions?api-version=2024-02-15-preview".
- `GPT4VISION_DEFAULT_MAX_TOKENS`: The maximum number of tokens to generate in the API response. Defaults to 500.
- `GPT4VISION_API_KEY`: The API key required to authenticate and access the GPT-4 Vision API. This variable is mandatory.
- `DEFAULT_MAX_THREADS`: The maximum number of threads to use for concurrent API requests. Defaults to 4.

Before running the application, make sure to set these environment variables in your shell or using a `.env` file. Here's an example:

```bash
export GPT4VISION_MODEL_URL="https://your-gpt4vision-api-url"
export GPT4VISION_DEFAULT_MAX_TOKENS=500
export GPT4VISION_API_KEY="your-api-key"
export DEFAULT_MAX_THREADS=4
```

## Testing the gpt4 vision model locally

In order to run the server you will need to run the following command to describe an image

### gpt4vision_imagetotext endpoint

```bash
curl --location --request POST 'http://localhost:8080/gpt4vision_imagetotext/invoke' \
--header 'Content-Type: application/json' \
--header "Integrations-API-Key: dev-only-token" \
--data-raw '{
    "query": "tell me everything you know about what is in this image",
    "image_url": "https://boots.scene7.com/is/image/Boots/10105075_1?id=ZoQkR1&wid=532&hei=578&fmt=jpg&dpr=off"
}'
```

### /experience/gpt4vision/askimage/invoke endpoint

```bash
curl --location --request POST 'http://localhost:8080/experience/gpt4vision/askimage/invoke' \
--header 'Content-Type: application/json' \
--header "Integrations-API-Key: dev-only-token" \
--data-raw '{
    "query": "tell me everything you know about what is in this image",
    "image_url": "https://boots.scene7.com/is/image/Boots/10105075_1?id=ZoQkR1&wid=532&hei=578&fmt=jpg&dpr=off"
}'
```

### /system/gpt4vision/transformers/imagetotext/invoke endpoint

```bash
curl --location --request POST 'http://localhost:8080/system/gpt4vision/transformers/image_to_text/invoke' \
--header 'Content-Type: application/json' \
--header "Integrations-API-Key: dev-only-token" \
--data-raw '{
    "query": "tell me everything you know about what is in this image",
    "image_url": "https://boots.scene7.com/is/image/Boots/10105075_1?id=ZoQkR1&wid=532&hei=578&fmt=jpg&dpr=off"
}'
```
