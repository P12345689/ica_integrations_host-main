# Wikipedia Integration

> Author: Mihai Criveti

Wikipedia Integration is a FastAPI application which calls the Wikipedia public API to search for an input query.

It returns either the full page, or a summary of it.

## Endpoints

- POST /system/wikipedia/retrievers/search/invoke Invokes the Wikipedia search API for the input query. It expects a JSON payload with the search string and the expected result type (full/summary)
- POST /wikipedia/invoke alias for /system/wikipedia/retrievers/search/invoke for backward compatibility

## Testing the integration locally

### Return full Wikipedia page
The following will return the full Wikipedia page for Python programming

```bash
curl --silent --request POST \
     'http://localhost:8080/system/wikipedia/retrievers/search/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data '{
          "search_string": "Python programming",
          "results_type": "full"
          }'
```

### Return summary of a Wikipedia page
The following will return a summary for the Wikipedia page for Python programming

```bash
curl --silent --request POST \
     'http://localhost:8080/system/wikipedia/retrievers/search/invoke' \
     --header "Content-Type: application/json" \
     --header "Integrations-API-Key: dev-only-token" \
     --data '{
          "search_string": "Python programming",
          "results_type": "summary"
          }'
```
