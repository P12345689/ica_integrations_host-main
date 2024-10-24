# IBM Watson Discovery V2 Integration

> Author: Mihai Criveti

This integration provides services for querying IBM Watson Discovery V2 and asking questions based on Discovery results.

## Endpoints

- POST /system/discovery/retrievers/query/invoke
  Invokes the System API to query Watson Discovery.

- POST /experience/discovery/ask_discovery/invoke
  Invokes the Experience API to ask questions based on Discovery results using an LLM.

## Environment Variables

Make sure to set the following environment variables:

```bash
export WATSON_DISCOVERY_API_KEY="your_api_key"
export WATSON_DISCOVERY_URL="your_discovery_url"
export WATSON_DISCOVERY_PROJECT_ID="your_project_id"
```

## Testing the integration locally

### Query Discovery - System API

This endpoint allows you to query Watson Discovery directly.

```bash
curl --location --request POST \
    'http://localhost:8080/system/discovery/retrievers/query/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "What is artificial intelligence?",
        "collection_ids": ["your_collection_id"],
        "project_id": "your_project_id"
    }'
```

### Ask Discovery - Experience API

This endpoint allows you to ask questions based on Discovery results, processed by an LLM.

```bash
curl --location --request POST \
    'http://localhost:8080/experience/discovery/ask_discovery/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "Explain the concept of machine learning",
        "collection_ids": ["your_collection_id"],
        "project_id": "your_project_id"
    }'
```

## Additional Watson Discovery V2 API Examples

Here are some additional examples of using the Watson Discovery V2 API directly using `curl`:

### Get project
```bash
curl -u "apikey:${WATSON_DISCOVERY_API_KEY}" "${WATSON_DISCOVERY_URL}/v2/projects/${WATSON_DISCOVERY_PROJECT_ID}?version=2023-03-31"
```

### Get collections
```bash
curl -u "apikey:${WATSON_DISCOVERY_API_KEY}" "${WATSON_DISCOVERY_URL}/v2/projects/${WATSON_DISCOVERY_PROJECT_ID}/collections?version=2023-03-31"
```

### List collection
```bash
curl -u "apikey:${WATSON_DISCOVERY_API_KEY}" "${WATSON_DISCOVERY_URL}/v2/projects/${WATSON_DISCOVERY_PROJECT_ID}/collections/${WATSON_DISCOVERY_COLLECTION_ID}?status=available&version=2023-03-31"
```

### List documents in a collection
```bash
curl -u "apikey:${WATSON_DISCOVERY_API_KEY}" "${WATSON_DISCOVERY_URL}/v2/projects/${WATSON_DISCOVERY_PROJECT_ID}/collections/${WATSON_DISCOVERY_COLLECTION_ID}/documents?status=available&version=2023-03-31"
```

### Query a collection
```bash
curl -X POST -u "apikey:${WATSON_DISCOVERY_API_KEY}" \
    --header "Content-Type: application/json" \
    --data '{
        "collection_ids": [
            "your_collection_id_1",
            "your_collection_id_2"
        ],
        "query": "text:IBM"
    }' \
    "${WATSON_DISCOVERY_URL}/v2/projects/${WATSON_DISCOVERY_PROJECT_ID}/query?version=2023-03-31"
```

Replace `your_collection_id`, `your_project_id`, and other placeholders with your actual Watson Discovery values.
