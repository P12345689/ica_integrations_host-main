# Duck Duck Go Search

This is a Duckduckgo Search langchain agent that can be used with integrations in sidekick.

## Endpoints

- **POST /duckduckgo/invoke**
  Invokes the Duckduckgo Search process. It expects a JSON payload with an `input` containing a `query`.

## Testing the search locally
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'http://localhost:8080/duckduckgo/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
        "input": {
            "query": "Where is the superbowl being hosted in 2025?"
        }
    }'
```

## Testing the search remotely
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/duckduckgo/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
        "input": {
            "query": "what age is Taylor Swift?"
        }
    }'
```

or

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/duckduckgo/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
        "input": {
            "query": "what age is Taylor Swift?"
        }
    }'
```

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/duckduckgo/invoke' \
    --header 'Content-Type: application/json' \
    --header "Integrations-API-Key:dev-only-token" \
    --data-raw '{
        "input": {
            "query": "what is the weather in London?"
        }
    }'
```
