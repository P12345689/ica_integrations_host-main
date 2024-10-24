
```bash
curl --location --request POST 'http://localhost:8080/agent_llamaindex/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "who is chris hay of ibm?",
            "tools": ["google_search"]
    }'
```

```bash
curl --location --request POST 'http://localhost:8080/agent_llamaindex/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "who is chris hay of ibm?",
            "tools": ["google_search"],
            "llm_override": ["OLLAMA", "llama3.1"]
    }'
```

```bash
curl --location --request POST 'http://localhost:8080/agent_llamaindex/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "what is the current time?",
            "tools": ["get_system_time"]
    }'
```

```bash
curl --location --request POST 'http://localhost:8080/agent_llamaindex/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "who is chris hay of ibm?",
            "tools": ["google_search"],
            "llm_override": ["WATSONX", "mistralai/mistral-large"]
    }'
```

## testing the langchain version for comparison

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "who is chris hay of ibm?",
            "tools": ["google_search"],
            "llm_override": ["OLLAMA", "llama3.1"]
    }'
```


```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \ 
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "should i bring a brolly with me for my trip to london just now?",
            "tools": ["google_search", "get_system_time"],
            "llm_override": ["OLLAMA", "llama3.1"]
    }'
```