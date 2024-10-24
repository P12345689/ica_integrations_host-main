# Locally Loaded CSV Chat Integration

This integration provides services for chatting with CSV data that is stored within the router using pandas and an LLM.

## Endpoints

- POST /experience/local_load_csv_chat/ask/invoke
  Invokes the Experience API to answer a question based on the CSV datasets contained within the router.

- POST /system/local_load_csv_chat/info/invoke
  Invokes the System API to provide information about the CSV datasets contained within the router.

## Testing the integration locally

### Chat with local load CSV - Experience API

This endpoint allows you to ask questions about CSV data using natural language. Only a query is provided as the CSV content is contained within the router.

```bash
curl -sS --location --request POST \
    'http://localhost:8080/experience/local_load_csv_chat/ask/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
    --form 'query="What are the IDs of the level1 requirements in OWASP ASVS?"' \
	--form 'csvType="asvs"'
```

```bash
curl -sS --location --request POST \
    'http://localhost:8080/experience/local_load_csv_chat/ask/invoke' \
	--header 'Content-Type: multipart/form-data' \
	--header 'Integrations-API-Key: dev-only-token' \
	--form 'query="What are the client IPs and DB User name when login failed? output as a list"' \
	--form 'csvType="failed logins"'
```

```bash
curl -sS --location --request POST \
    'http://localhost:8080/experience/local_load_csv_chat/ask/invoke' \
	--header 'Content-Type: multipart/form-data' \
	--header 'Integrations-API-Key: dev-only-token' \
	--form 'query="Which clients have a session count of greater than 199?"' \
	--form 'csvType="trusted connection sql"'
```

### Get CSV Info - System API

This endpoint provides basic information about the CSV datasets contained within the router.

Example:

```bash
curl -sS --location --request POST \
    'http://localhost:8080/system/local_load_csv_chat/info/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
	--form 'csvType="asvs"'
```

To nicely format the information returned on the CSV, use:

```bash
curl -sS --location --request POST \
    'http://localhost:8080/system/local_load_csv_chat/info/invoke' \
    --header 'Content-Type: multipart/form-data' \
    --header 'Integrations-API-Key: dev-only-token' \
	--form 'csvType="asvs"' \
	| jq '.response[].message | fromjson | .'
```
