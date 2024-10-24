# NVIDIA Integration

> Author: Mihai Criveti

The integration for NVIDIA allows users to recognize images based on prompt inputs and image URLs, generate images based on a prompt and talk with LLMs.

## Requirements

> The following endpoints require an NVIDIA_BEARER_TOKEN in your environment variables

- An Nvidia API key
  - Can be created at [NVIDIA API portal](https://build.nvidia.com/explore/discover).
  - Run the following command: `export NVIDIA_BEARER_TOKEN="your_api_key"`

Model information: [NVIDIA API portal](https://docs.api.nvidia.com/nim/reference/nvidia-neva-22b-infer)

## Endpoints

- **POST /system/nvidia/neva22b/invoke**
  Invokes the image recognition process. It expects a JSON payload with a `query` and an `image_url`.
<br><br>
- **POST /system/nvidia/image/invoke**
  Invokes the image generation process. It expects a JSON payload with a `query` and an `model`.
<br><br>
- **POST /system/nvidia/llm/invoke**
  Invokes the LLM process. It expects a JSON payload with a `query` and an `model`.

## Testing

The following invoke inputs are supported currently:

### Image Recognition

```bash
curl --silent --request POST \
  'http://localhost:8080/system/nvidia/neva22b/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
    "query": "What is in this image?",
    "image_url": "https://bellard.org/bpg/2small.png"
  }'
```

Example output:
```json
{
  "status": "success",
  "invocationId": "96b6433f-a4d3-4656-9005-f46e5ddb0605",
  "response": [
    {
      "message": "NVIDIA Neva 22B\n---------------\n\nThe image has been identified as:\n\nThe image features a cartoon-style penguin standing on a black background. The penguin is drawn with a yellow beak and feet, and it appears to be looking up. The penguin's body is white and black, and it is positioned in the center of the image.",
      "type": "text"
    }
  ]
}
```

### Image generation

> Only the following models are currently supported:
> 1. stable-diffusion-3-medium
> 2. sdxl-turbo
> 3. stable-diffusion-xl
> 4. sdxl-lightning

```bash
curl --silent --request POST \
  'http://localhost:8080/system/nvidia/image/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
    "query": "Generate an image of a penguin in a suit",
    "model": "stable-diffusion-3-medium"
  }'
```

Example output:
```json
{
  "status": "success",
  "invocationId": "96b6433f-a4d3-4656-9005-f46e5ddb0605",
  "response": [
    {
      "message": "http://localhost:8080/public/nvidia/nvidia_8484d9c0-1b1a-412b-9685-9b3b6f462e99.jpeg",
      "type": "text"
    }
  ]
}
```

### Talk with models

```bash
curl --silent --request POST \
  'http://localhost:8080/system/nvidia/llm/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
    "query": "What is 1+1?",
    "model": "llama3-chatqa-1.5-70b"
  }'
```

## Testing Locally

You can perform an image recognition request against NVIDIA Neva-22B locally by calling `http://localhost:8080/neva22b/invoke` as a POST request, using the inputs described above. A successful output will return a text message with the recognition result:

```json
{
  "status": "success",
  "invocationId": "f62692d9-f6ce-47a5-b80e-2457083e914d",
  "response": [
    {
      "message": "The image contains a cat sitting on a couch.",
      "type": "text"
    }
  ]
}
```

#### Invalid bearer token output:
If the Bearer token is missing or invalid, an error message will be returned:

```json
{
  "status": "success",
  "invocationId": "abcdef12-3456-7890-abcd-ef1234567890",
  "response": [
    {
      "message": "I'm sorry but the NVIDIA Neva-22B integration is misconfigured. Please check the Bearer token.",
      "type": "text"
    }
  ]
}
```

#### Image recognition error:
If there is an error with the image recognition request, an error message will be returned:

```json
{
  "status": "success",
  "invocationId": "1234abcd-ef56-7890-abcd-1234ef567890",
  "response": [
    {
      "message": "I'm sorry but I couldn't recognize the image, please try with a different image.",
      "type": "text"
    }
  ]
}
```

Make sure to set the `NVIDIA_BEARER_TOKEN` environment variable with your Bearer token before running the integration.
