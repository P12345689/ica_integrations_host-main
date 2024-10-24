# Test route with conversational context

> Author: Mihai Criveti

```bash
curl --location --request POST 'http://localhost:8080/system/test/debug/conversation' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "What is the context?",
            "context": "[{\"content\":\"This is a test context.\",\"type\":\"CONTEXT\"}]",
            "use_context": true
    }'
```

```bash
curl --silent --location --request POST 'http://localhost:8080/system/test/debug/conversation' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "What is the context?",
            "context": "[{\"content\":\"What is OpenShift\",\"type\":\"PROMPT\"},{\"content\":\"OpenShift is a containerization and orchestration platform for deploying and managing applications using Kubernetes. It provides a simple and efficient way to manage containers and application services, enabling developers to focus on building their applications instead of managing the underlying infrastructure.\",\"type\":\"ANSWER\"}]",
            "use_context": true
    }' | jq -r '.response[0].message'
```
