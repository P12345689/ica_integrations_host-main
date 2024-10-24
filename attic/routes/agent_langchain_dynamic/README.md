## Using the agents

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain_dynamic/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "what is the current time?"
    }'
```
