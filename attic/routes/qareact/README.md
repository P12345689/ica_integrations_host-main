# Google Search
This is a Google Search langchain agent that can be used with integrations in sidekick

## Using Google Search
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'http://localhost:8080/qareact/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "input": {
            "query": "should i bring a brolly with me for my trip to london just now?"
        }
    }'
```

## Using Google, Wikipedia and Powerpoint
In order to run the server you will need to run the following command

```
curl --location --request POST 'http://localhost:8080/qareact/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "query": "Give me a brief biography of Jerry Cuomo (use multiple sources)"
        }
    }'
```

## Using Website Up or Healthy
In order to run the server you will need to run the following command

```
curl --location --request POST 'http://localhost:8080/qareact/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "query": "is the ibm website up"
        }
    }'
```

or

```
curl --location --request POST 'http://localhost:8080/qareact/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "query": "is http://localhost:8080/health" healthy"
        }
    }'
```

## Using Mermaid and Powerpoint

```bash
curl --location --request POST 'http://localhost:8080/qareact/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "query": "generate an organization chart diagram for the microsoft executive team"
        }
    }'
```

## Testing the search remotely
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/googlesearch/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "query": "where is the superbowl being hosted in 2025?"
        }
    }'
```

or

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/googlesearch/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "query": "what age is Taylor Swift?"
        }
    }'
```

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/googlesearch/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "query": "what is the weather in London?"
        }
    }'
```
