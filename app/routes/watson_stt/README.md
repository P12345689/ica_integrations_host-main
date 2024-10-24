# Watson Speech-to-Text Integration

> Author: Mihai Criveti

This integration provides services for transcribing audio to text using IBM Watson Speech-to-Text.

## Table of Contents

- [Watson Speech-to-Text Integration](#watson-speech-to-text-integration)
  - [Table of Contents](#table-of-contents)
  - [Environment Setup](#environment-setup)
  - [Installation](#installation)
  - [Usage](#usage)
    - [System API](#system-api)
      - [Using a local file:](#using-a-local-file)
      - [Using a URL:](#using-a-url)
    - [Experience API](#experience-api)
      - [Using a local file:](#using-a-local-file-1)
      - [Using a URL:](#using-a-url-1)
  - [Endpoints](#endpoints)
  - [Supported Audio Formats](#supported-audio-formats)
  - [Error Handling](#error-handling)
  - [Customization](#customization)
  - [Security](#security)
  - [Limitations](#limitations)
  - [Contributing](#contributing)

## Environment Setup

Before using this integration, set up the following environment variables:

- `STT_API_KEY`: Your IBM Watson Speech-to-Text API key.
- `STT_BASE_URL`: The base URL for the IBM Watson Speech-to-Text service (e.g., "https://api.us-south.speech-to-text.watson.cloud.ibm.com").
- `SERVER_NAME`: The URL of your server (default: "http://127.0.0.1:8080").
- `DEFAULT_MAX_THREADS`: Maximum number of threads for concurrent processing (default: 4).

You can set these in a `.env` file in the root of your project:

```
STT_API_KEY=your_api_key_here
STT_BASE_URL=https://api.us-south.speech-to-text.watson.cloud.ibm.com
SERVER_NAME=http://127.0.0.1:8080
DEFAULT_MAX_THREADS=4
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/watson-stt-integration.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables as described above.

## Usage

### System API

The System API provides a straightforward transcription of audio to text.

#### Using a local file:

```bash
curl --location --request POST \
    'http://localhost:8080/system/stt/retrievers/transcribe_audio/invoke' \
    --header 'Integrations-API-Key: dev-only-token' \
    --form 'audio_file=@"/path/to/your/audio/file.flac"' \
    --form 'model="en-US_BroadbandModel"' \
    --form 'timestamps="true"' \
    --form 'max_alternatives="3"'
```

#### Using a URL:

```bash
curl --location --request POST \
    'http://localhost:8080/system/stt/retrievers/transcribe_audio/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "audio_url": "https://example.com/path/to/your/audio/file.flac",
        "model": "en-US_BroadbandModel",
        "timestamps": true,
        "max_alternatives": 3
    }'
```

### Experience API

The Experience API provides a more user-friendly, natural language response based on the transcription.

#### Using a local file:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/stt/ask_transcribe/invoke' \
    --header 'Integrations-API-Key: dev-only-token' \
    --form 'audio_file=@"/path/to/your/audio/file.flac"' \
    --form 'model="en-US_BroadbandModel"' \
    --form 'timestamps="true"' \
    --form 'max_alternatives="3"'
```

#### Using a URL:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/stt/ask_transcribe/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "audio_url": "https://example.com/path/to/your/audio/file.flac",
        "model": "en-US_BroadbandModel",
        "timestamps": true,
        "max_alternatives": 3
    }'
```

```bash
url --location --request POST \
    'http://localhost:8080/experience/stt/ask_transcribe/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "audio_url": "http://127.0.0.1:8080/system/file_upload/download/338e1276-5e3e-44d0-be29-860e915bac5a.flac?key=4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa&team_id=team123&user_email=user@example.com",
        "model": "en-US_BroadbandModel",
        "timestamps": false,
        "max_alternatives": 3
    }'
```

## Endpoints

1. POST /system/stt/retrievers/transcribe_audio/invoke
   - Invokes the System API to transcribe an audio file to text.

2. POST /experience/stt/ask_transcribe/invoke
   - Invokes the Experience API to transcribe an audio file and provide a natural language response.

## Supported Audio Formats

- FLAC (audio/flac)
- MP3 (audio/mp3)
- MPEG (audio/mpeg)
- OGG (audio/ogg)
- flac (audio/flac)
- WebM (audio/webm)

## Error Handling

The integration includes robust error handling. If an error occurs, you'll receive a JSON response with an appropriate HTTP status code and an error message. For example:

```json
{
    "detail": "Error transcribing audio: Invalid audio format"
}
```

## Customization

You can customize the response format by modifying the Jinja2 templates in the `app/routes/stt/templates` directory:

- `stt_response.jinja`: Template for the system API response
- `stt_nl_response.jinja`: Template for the experience API response

## Security

This integration uses an `Integrations-API-Key` header for authentication. Make sure to replace `dev-only-token` with a secure token in production environments.

## Limitations

- LLM support is not yet integrated with the experience API.
- There's currently no rate limiting implemented. Consider adding rate limiting for production use.

## Contributing

Contributions to improve the integration are welcome. Please submit a pull request or open an issue to discuss proposed changes.
