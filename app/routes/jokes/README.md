# Joke Service

> Author: Chris Hay

This is an example of an experience api that will tell a joke.
It purely uses the prompt template and url to tell the joke


## Endpoints

- ## POST /experience/joke/retrievers/get_joke/invoke Invokes the Experience API to tell a joke about a topic.

- ## POST /joke/invoke Can also be invoked without the experience API to give the same result.

## Testing the joke locally

### Experience API
You can test the joke by running a curl command manually

```bash
curl --location --request \
    POST 'http://localhost:8080/experience/joke/retrievers/get_joke/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"topic": "cats"}'
```

or

### Joke API
You can test the joke by running a curl command manually

```bash
curl --location --request POST 'http://localhost:8080/joke/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"topic": "cats"}'
```
