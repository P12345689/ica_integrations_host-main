# Website Service

> Author: Mihai Criveti

This is an example of a System Level API that will call the website service.
There is no GenAI involved in this call, so it will be lightning fast.

## Endpoints

- ## POST /system/website/retrievers/check_website_up/invoke Invokes the Website Service to check if a website is up. It expects a JSON payload with the url.

### Check website it up
The following will check if a website is up:

```bash
    curl --location --request POST \
        'http://localhost:8080/system/website/retrievers/check_website_up/invoke' \
        --header 'Content-Type: application/json' \
        --header 'Integrations-API-Key: dev-only-token' \
        --data-raw '{
            "url": "https://www.ibm.com"
            }'
```


### Check website health endpoint
The following will check if a website health endpoint is healthy

```bash
    curl --location --request POST \
        'http://localhost:8080/system/website/retrievers/check_website_health/invoke' \
        --header 'Content-Type: application/json' \
        --header 'Integrations-API-Key: dev-only-token' \
        --data-raw '{
            "url": "http://localhost:8080/health"
            }'
```
