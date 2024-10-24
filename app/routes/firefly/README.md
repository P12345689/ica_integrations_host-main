# Adobe Firefly Integration

The integration for Adobe Firefly allows users to generate images based upon prompt inputs, specifying further options to tweak the output to what is desired.

## Backend Configuration

Integration with Adobe Firefly depends upon "Server-to-Server" API keys. These are created in the Adobe Developer Console, using the following [guide](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/). The following environment variables can be set, some are **required** for the integration to function.

| Key                     | Description  | Example Value | Default | Required  |
|:-----------------------:|:-------------|:--------------------:|:-------:|:---------:|
| ADOBE_FIREFLY_CLIENT_ID | The Client ID from the Adobe Technical account with access to the Firefly API. | | | **Yes** |
| ADOBE_FIREFLY_CLIENT_SECRET | The Client secret from the Adobe Technical account with access to the Firefly API. | | | **Yes** |
| ADOBE_FIREFLY_ENDPOINT | The specific Adobe host to perform queries against | firefly-beta.adobe.io | firefly-beta.adobe.io | No |

## Invoke Inputs

The following invoke inputs are supported currently:

### Image Generation

```bash
curl -X 'POST' \
  'http://localhost:8080/firefly/invoke' \
  -H 'Integrations-API-Key: dev-only-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "Horses in a field.",
    "image_type": "art",
    "width": 1024,
    "height": 1024
  }'
```

### Image Expand

```bash
curl -X 'POST' \
  'http://localhost:8080/firefly/invoke' \
  -H 'Integrations-API-Key: dev-only-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "action": "expand",
    "query": "Neon city streets",
    "width": 1792,
    "height": 1024,
    "reference_image": "https://example.com/image.jpg"
  }'
```

### Generative Fill

```bash
curl -X 'POST' \
  'http://localhost:8080/firefly/invoke' \
  -H 'Integrations-API-Key: dev-only-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "action": "fill",
    "query": "Remove text",
    "width": 1024,
    "height": 1024,
    "reference_image": "https://example.com/image.jpg",
    "mask_image": "https://example.com/mask.png"
  }'
```

## Testing Locally

You can perform a generation request against Firefly locally, by calling `http://localhost:8080/firefly/invoke` as a POST request, using the inputs described above. Successful output will return a URL which is valid for 1 hour, which can be downloaded from any saved:

```json
{
  "status": "success",
  "invocationId": "",
  "response": [
    {
      "message": "https://pre-signed-firefly-prod.s3.amazonaws.com/images/60dc3b2a-9172-4def-88e2-5e0a994090ac?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDA3TX66CSNORXF4%2F20240509%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240509T145903Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=ea174c1837b6002d5f857d72495a035a24fddde49be3e939e94122ebe6ea0a97",
      "type": "image"
    }
  ]
}
```
