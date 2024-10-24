# Google Search

This is a Google Search langchain agent that can be used with integrations in IBM Consulting Assistants.

## Requirements:

> The following endpoints require a GOOGLE_API_KEY and a GOOGLE_CSE_ID in your environment variables

- A Custom Google Search API key
  - Can be created at [Google API Dashboard](https://console.cloud.google.com/apis/dashboard).
  - Run the following command: `export GOOGLE_API_KEY="your_api_key"`
- A Google Programmable Search Engine ID
  - Can be created at [Google Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/all).
  - Run the following command: `export GOOGLE_CSE_ID="your_search_engine_ID"`

## Endpoints

- **POST /googlesearch/invoke**
  Invokes the Google search process. It expects a JSON payload with a `query`.


## Testing the search locally
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'http://localhost:8080/googlesearch/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
            "query": "where is the superbowl being hosted in 2025?"
    }'
```

## Testing the search dev
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'http://localhost:8080/googlesearch/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
            "query": "where is the superbowl being hosted in 2025?"
    }'
```

## Testing the search production
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'http://localhost:8080/googlesearch/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
            "query": "where is the superbowl being hosted in 2025?"
    }'
```

or

```bash
curl --location --request POST 'http://localhost:8080/googlesearch/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
            "query": "what age is Taylor Swift?"
    }'
```

```bash
curl --location --request POST 'http://localhost:8080/googlesearch/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
            "query": "what is the weather in London?"
    }'
```
