# ms_teams Integration

This integration provides functionality to interact with Microsoft Teams and Outlook Calendar. Users can create meetings, view their meetings and check for calendar availability of other participants.

## Usage

To use this integration, follow these steps:

1. Ensure you have the required dependencies installed. Update `requirements.txt` to include:
ffastapi
pydantic
jinja2
webexteamssdk
2. Set up the necessary environment variables (e.g., `DEFAULT_MAX_THREADS`).
3. Export your Graph API access token, found here: `https://developer.microsoft.com/en-us/graph/graph-explorer`
4. Include this module in your FastAPI application.

## API Endpoints


### POST /system/ms_teams/invoke

Invokes the ms_teams system API, which can perform different actions with the Graph API

```bash
curl --location --request POST 'http://localhost:8080/system/ms_teams/invoke' \
     --header "Integrations-API-Key: dev-only-token" \
     --header 'Content-Type: application/json' \
     --data-raw '{
         "action" : "list_meetings",
         "params" :
         {
             "end_date": "2024-08-09 15:32:02.977848"
         },
         "token": "'"${ACCESS_TOKEN}"'"
     }'
```


### POST /experience/ms_teams/invoke

Invokes the ms_teams experience API, which can perform different actions with natural language and the help of an LLM

```bash
curl --location --request POST 'http://localhost:8080/experience/ms_teams/invoke' \
     --header "Integrations-API-Key: dev-only-token" \
     --header 'Content-Type: application/json' \
     --data-raw '{
         "query": "Create a meeting for tomorrow, which should start at 1PM UTC+3 and last for 1 hour",
         "access_token": "'"${ACCESS_TOKEN}"'"
     }'
```


```bash
curl --location --request POST 'http://localhost:8080/experience/ms_teams/invoke' \
     --header "Integrations-API-Key: dev-only-token" \
     --header 'Content-Type: application/json' \
     --data-raw '{
         "query": "List the meeting i will have over the next 4 days",
         "access_token": "'"${ACCESS_TOKEN}"'"
     }'
```


```bash
curl --location --request POST 'http://localhost:8080/experience/ms_teams/invoke' \
     --header "Integrations-API-Key: dev-only-token" \
     --header 'Content-Type: application/json' \
     --data-raw '{
         "query": "Give me more details about the meeting with this id: AAMkAGZhZjBiZjc0LWQ4NTgtNDgxNS1iMGUxLTk2NzQ2NjJjOTk0MQBGAAAAAACVeJVtTIZLT519KT5shMGSBwAfiBQh1tz9SKVWES7HWesYAAAAAAENAAAfiBQh1tz9SKVWES7HWesYAAHKPKOMAAA=",
         "access_token": "'"${ACCESS_TOKEN}"'"
     }'
```

```bash
curl --location --request POST 'http://localhost:8080/experience/ms_teams/invoke' \
     --header "Integrations-API-Key: dev-only-token" \
     --header 'Content-Type: application/json' \
     --data-raw '{
         "query": "Find possible timeslot meetings tomorrow with Andrei Cigmaian (andrei.cigmaian@ibm.com)",
         "access_token": "'"${ACCESS_TOKEN}"'"
     }'
```
