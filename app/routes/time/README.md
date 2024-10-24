# Time Integration

This is the time integration, which provides services for telling the time and answering questions about time/timezones.

## Endpoints

- POST /experience/time/ask_time/invoke
  Invokes the Experience API to answer a question based on a time-related query.

- POST /system/time/retrievers/get_current_time/invoke
  Invokes the System API to give the current time. It accepts a JSON payload with a format string.

## Testing the integration locally

### Ask Time - Experience API

This is an example of an Experience Level API that will use the time service.
You can ask time-related questions using this endpoint.

```bash
curl --location --request POST \
    'http://localhost:8080/experience/time/ask_time/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "What is the time in London?"
    }'
```

### Get Current Time - System API

This is an example of a System Level API that will call the time service.
There is no GenAI involved in this call, so it will be very fast.

```bash
curl --location --request POST \
    'http://localhost:8080/system/time/retrievers/get_current_time/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "format": "%Y-%m-%d %H:%M:%S"
    }'
```
