# IBM Watson Text-to-Speech Integration

> Author: Mihai Criveti

This integration provides services for listing available voices, getting information about specific voices, and converting text to speech using various voices and audio formats.

## Endpoints

- POST /system/tts/retrievers/list_voices/invoke
  Lists all available voices for text-to-speech conversion.

- POST /system/tts/retrievers/get_specific_voice/invoke
  Gets information about a specific voice.

- POST /system/tts/retrievers/generate_speech/invoke
  Generates speech from text and returns a URL for downloading the audio file.

- GET /public/{filename}
  Serves the generated audio file.

## Testing the integration locally

### List All Voices

This endpoint lists all available voices for text-to-speech conversion.

```bash
curl --location --request POST \
    'http://localhost:8080/system/tts/retrievers/list_voices/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{}'
```

Example response:

```json
{
  "status": "success",
  "invocationId": "1234567890abcdef",
  "response": [
    {
      "message": "Available voices for text-to-speech conversion:\n\n- en-US_AllisonV3Voice\n  Language: en-US\n  Gender: female\n  Description: Allison: American English female voice.\n\n- en-US_LisaV3Voice\n  Language: en-US\n  Gender: female\n  Description: Lisa: American English female voice.\n\n...\n\nTotal number of voices available: 32",
      "type": "text"
    }
  ]
}
```

### Get Specific Voice

This endpoint retrieves information about a specific voice.

```bash
curl --location --request POST \
    'http://localhost:8080/system/tts/retrievers/get_specific_voice/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "voice": "en-US_AllisonV3Voice",
        "customization_id": null
    }'
```

Example response:

```json
{
  "status": "success",
  "invocationId": "0987654321fedcba",
  "response": [
    {
      "message": "Information for voice: en-US_AllisonV3Voice\n\n- Language: en-US\n- Gender: female\n- Description: Allison: American English female voice.\n- Customizable: true\n- Supported Features:\n  - Voice Transformation: false\n  - Custom Pronunciation: true\n- URL: https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/abcdef/v1/voices/en-US_AllisonV3Voice",
      "type": "text"
    }
  ]
}
```

### Generate Speech

This endpoint generates speech from text using the specified voice and format.

```bash
curl --location --request POST \
    'http://localhost:8080/system/tts/retrievers/generate_speech/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "Hello, world! This is a test of the text-to-speech integration.",
        "voice": "en-US_AllisonV3Voice",
        "format": "audio/wav",
        "rate": 22050
    }'

curl --location --request POST \
    'http://localhost:8080/system/tts/retrievers/generate_speech/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "Hi, this is Mihai!",
        "voice": "en-US_MichaelV3Voice",
        "format": "audio/wav",
        "rate": 22050
    }'


```

Example response:

```json
{
  "status": "success",
  "invocationId": "abcdef1234567890",
  "response": [
    {
      "message": "Speech generated successfully. \n\nDownload URL: /public/12345678-90ab-cdef-1234-567890abcdef.wav\n\nYou can use this URL to download the generated audio file.",
      "type": "text"
    }
  ]
}
```

After receiving the download URL, you can use it to retrieve the generated audio file:

```bash
curl -O -J 'http://localhost:8080/public/12345678-90ab-cdef-1234-567890abcdef.wav'
```

This will download the audio file to your current directory.

## Supported Audio Formats

The integration supports the following audio formats for speech generation:

| Format | MIME Type | Default Sampling Rate | Required Parameters | Optional Parameters |
|--------|-----------|----------------------|---------------------|---------------------|
| ALAW | audio/alaw | None | `rate={integer}` | None |
| BASIC | audio/basic | 8000 Hz | None | None |
| FLAC | audio/flac | 22,050 Hz | None | `rate={integer}` |
| L16 | audio/l16 | None | `rate={integer}` | `endianness=big-endian` or `endianness=little-endian` |
| MP3 | audio/mp3 | 22,050 Hz | None | `rate={integer}` |
| MPEG | audio/mpeg | 22,050 Hz | None | `rate={integer}` |
| MULAW | audio/mulaw | None | `rate={integer}` | None |
| OGG | audio/ogg | 22,050 Hz | None | `rate={integer}` |
| OGG OPUS | audio/ogg;codecs=opus | 48,000 Hz | None | `rate={integer}` |
| WAV | audio/wav | 22,050 Hz | None | `rate={integer}` |
| WEBM | audio/webm | 48,000 Hz | None | None |
| WEBM OPUS | audio/webm;codecs=opus | 48,000 Hz | None | None |
| WEBM VORBIS | audio/webm;codecs=vorbis | 22,050 Hz | None | `rate={integer}` |

When using the generate_speech endpoint, specify the desired format using the `format` parameter. If applicable, you can also specify the `rate` and `endianness` parameters.

### Examples for different audio formats:

1. Generate speech in MP3 format:

```bash
curl --location --request POST \
    'http://localhost:8080/system/tts/retrievers/generate_speech/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "Hi, this is Mihai, and I'd like to present the IBM Watson Text to Speech integration.",
        "voice": "en-US_MichaelV3Voice",
        "format": "audio/mp3",
        "rate": 44100
    }'
```

2. Generate speech in OGG format:

```bash
curl --location --request POST \
    'http://localhost:8080/system/tts/retrievers/generate_speech/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is an OGG audio sample.",
        "voice": "en-US_AllisonV3Voice",
        "format": "audio/ogg"
    }'
```

3. Generate speech in FLAC format:

```bash
curl --location --request POST \
    'http://localhost:8080/system/tts/retrievers/generate_speech/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is a FLAC audio sample.",
        "voice": "en-US_AllisonV3Voice",
        "format": "audio/flac",
        "rate": 48000
    }'
```

4. Generate speech in L16 format with specific endianness:

```bash
curl --location --request POST \
    'http://localhost:8080/system/tts/retrievers/generate_speech/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is an L16 audio sample.",
        "voice": "en-US_AllisonV3Voice",
        "format": "audio/l16",
        "rate": 16000,
        "endianness": "big-endian"
    }'
```

## File Serving

Generated audio files are saved in the `public` directory and can be accessed using the URL provided in the response from the generate_speech endpoint. The files are served directly by the FastAPI application.

## Error Handling

The integration includes robust error handling. If an error occurs during processing, the API will return an appropriate HTTP status code along with an error message. Common error scenarios include:

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid or missing API key
- 404 Not Found: Requested resource (e.g., specific voice or audio file) not found
- 500 Internal Server Error: Unexpected server-side error

Always check the response status code and message when integrating with this API.

## Rate Limiting and Usage

Please be aware of any rate limiting or usage quotas imposed by the underlying text-to-speech service. Excessive requests may result in temporary blocks or additional charges.

## Environment Variables

Make sure to set the following environment variables before running the integration:

- `TTS_API_KEY`: Your Text-to-Speech API key
- `TTS_BASE_URL`: The base URL for the Text-to-Speech API
- `DEFAULT_MAX_THREADS`: (Optional) The maximum number of threads for concurrent processing (default is 4)

## Dependencies

Ensure you have the following Python packages installed:

- fastapi
- uvicorn (for running the FastAPI application)
- aiohttp
- aiofiles
- jinja2
- pydantic

You can install these dependencies using pip:

```bash
pip install fastapi uvicorn aiohttp aiofiles jinja2 pydantic
```
