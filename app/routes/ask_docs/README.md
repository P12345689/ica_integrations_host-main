# Ask Docs Integration

> Author: Mihai Criveti

This integration provides services for retrieving document collections and asking questions about documents within those collections.

## Requirements (optional)

> To nicely process the json output, some curl commands use `jq`.
> If you do not want to use `jq`, skip the requirements installation and run the curl commands **without** `jq`.

- `jq` command
  - Can be installed using the command: `pip install jq`
  - For alternative downloads, check the [official documentation](https://jqlang.github.io/jq/).

## Endpoints

- POST /system/docs/retrievers/get_collections/invoke
  Invokes the System API to retrieve and list document collections.

- POST /experience/docs/ask_docs/invoke
  Invokes the Experience API to ask questions about documents in selected collections.

## Testing the integration locally

### Get Collections - System API

This endpoint retrieves the list of document collections:

- Using `jq`

```bash
curl --silent --location --request POST \
    'http://localhost:8080/system/docs/retrievers/get_collections/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "refresh": false
    }' | jq -r '.response[0].message'
```

- Without `jq`

```bash
curl --silent --location --request POST \
    'http://localhost:8080/system/docs/retrievers/get_collections/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "refresh": false
    }'
```

### Ask Docs - Experience API

This endpoint allows you to ask questions about documents in selected collections. Below are various examples demonstrating different use cases:

1. Query a single collection about a specific topic:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["66142f5a2dd4fae8aa4d5781"],
        "document_names": ["Sidekick AI API Documentation - Early Adopters 4.5.pdf"],
        "query": "What is the API endpoint used to retrieve document collections?",
        "refresh": false
    }' | jq -r '.response[0].message'
```

- Same thing, but specifying document names
```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["66142f5a2dd4fae8aa4d5781"],
        "query": "What is the API endpoint used to retrieve document collections?",
        "refresh": false
    }' | jq -r '.response[0].message'
```

2. Query multiple collections about a common theme:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["65ce6759957657eab7eb71ad", "65da019b6af7b1a73353f4ae"],
        "query": "What are the common themes or challenges mentioned across these documents?",
        "refresh": false
    }'
```

3. Query specific documents within a collection:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["65bcfeaeb7ec24f940a2507d"],
        "document_names": ["Application Modernization Briefing Deck_final_feb2.pdf"],
        "query": "What are the key benefits of application modernization mentioned in the briefing deck?",
        "refresh": false
    }'
```

4. Compare information across different collections:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["65752a0a35a8396c39763267", "65e32ad1583e479fae8e3d65"],
        "query": "Compare and contrast the approaches to healthcare innovation and digital transformation mentioned in these documents.",
        "refresh": false
    }'
```

5. Ask for a summary of multiple documents:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["65c535c7b7ec24f940b9e992"],
        "query": "Provide a brief summary of the key points from all documents in this collection.",
        "refresh": false
    }'
```

6. Query about specific data or metrics:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["653240419de6f665bbaa7a0a"],
        "query": "What were the top-selling products for Ayira Cosmetics Company in 2022-2023?",
        "refresh": false
    }'
```

7. Ask about technical specifications:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["65f8eb5f2175795515ce3e14"],
        "query": "What are the key maintenance procedures for high-pressure breathing air compressors?",
        "refresh": false
    }'
```

8. Query about legal or contractual information:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["65e473f2217579551554409b"],
        "query": "What are the key confidentiality clauses in the NDA sample?",
        "refresh": false
    }'
```

9. Ask about customer feedback or reviews:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["65b8c5d4b7ec24f940903858"],
        "query": "What are the most common positive and negative points mentioned in the customer reviews?",
        "refresh": false
    }'
```

10. Query about product manuals:

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/docs/ask_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "collection_ids": ["66830ad6ab2c494364bcea10"],
        "query": "What are the common troubleshooting steps for Nespresso machines across different models?",
        "refresh": false
    }'
```
