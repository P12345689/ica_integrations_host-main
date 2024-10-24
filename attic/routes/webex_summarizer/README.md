# WebEx Call Transcript Summarizer LLM

> Author: Mihai Criveti

Get an API token here: https://developer.webex.com/docs/api/v1/meeting-transcripts/list-meeting-transcripts

## Testing the integration locally


```bash
curl --request POST "http://127.0.0.1:8080/webex_summarizer/invoke" \
    --header "Content-Type: application/json" \
    --header 'Integrations-API-Key:dev-only-token' \
    --data '{
        "bearer_token": "your_token_here",
        "from_date": "2024-03-01",
        "to_date": "2024-03-31",
        "max_results": 10
    }'
```
