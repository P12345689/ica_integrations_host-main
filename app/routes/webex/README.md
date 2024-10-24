# WebEx Transcript Integration

This integration provides functionality for interacting with WebEx transcripts, including retrieving transcript lists, specific transcripts, and summarizing transcripts using an LLM. It can also be used to list the user's meetings and invite participants via chatting with the LLM

## Usage

To use this integration, follow these steps:

1. Ensure you have the required dependencies installed. Update `requirements.txt` to include:
ffastapi
pydantic
jinja2
webexteamssdk
2. Set up the necessary environment variables (e.g., `DEFAULT_MAX_THREADS`).
3. Include this module in your FastAPI application.

## API Endpoints

### POST /system/webex/invoke

Performs various WebEx operations based on the provided action.

#### Curl Examples

1. List Transcripts:

```bash
export WEBEX_TOKEN=...
curl --location --request POST 'http://localhost:8080/system/webex/invoke' \
  --header 'Content-Type: application/json' \
  --header "Integrations-API-Key: dev-only-token" \
  --data-raw '{
      "action": "list_transcripts",
      "params": {},
      "webex_token": "'"${WEBEX_TOKEN}"'"
  }'
```

2. Get Specific Transcript:

```bash
curl --location --request POST 'http://localhost:8080/system/webex/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "action": "get_transcript",
         "params": {"transcript_id": "12345"},
         "webex_token": "'"${WEBEX_TOKEN}"'"
     }'
```

### POST /experience/webex/invoke

This endpoint uses an LLM to interpret natural language queries about WebEx transcripts and perform the appropriate action.

```bash
curl --location --request POST 'http://localhost:8080/experience/webex/invoke' \
     --header "Integrations-API-Key: dev-only-token" \
     --header 'Content-Type: application/json' \
     --data-raw '{
         "query": "Summarize the transcript from my last meeting",
         "webex_token": "'"${WEBEX_TOKEN}"'"
     }'
```

```bash
curl --location --request POST 'http://localhost:8080/experience/webex/invoke' \
     --header "Integrations-API-Key: dev-only-token" \
     --header 'Content-Type: application/json' \
     --data-raw '{
         "query": "Invite Mark (mark.zhang@ibm.com) to the meeting 4553453fs5.",
         "webex_token": "'"${WEBEX_TOKEN}"'"
     }'
```


### POST /experience/webex/summarize_transcript

```bash
curl --location --request POST 'http://localhost:8080/experience/webex/summarize_transcript' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "transcript_id": "your_transcript_id_here",
         "query": "Summarize the key points discussed in this meeting",
         "webex_token": "'"${WEBEX_TOKEN}"'"
     }'
```

## Tools

This integration provides the following tools that can be used with LangChain or similar frameworks:

1. `webex_action`: Performs various WebEx operations.
2. `get_webex_info`: Provides information about the WebEx integration.
3. `webex_action_helper`: Offers information about different WebEx actions and their required parameters.
4. `summarize_transcript`: Summarizes a WebEx transcript using an LLM.

These tools can be imported and used as follows:

```python
from langchain.agents import load_tools
from .tools.webex_tool import webex_action, get_webex_info, webex_action_helper, summarize_transcript

tools = load_tools(["webex_action", "get_webex_info", "webex_action_helper", "summarize_transcript"])
```
