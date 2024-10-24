# Instagram
This is a Google Search langchain agent that can be used with integrations in sidekick

## Testing the instagram piece locally
In order to run the server you will need to run the following command to generate instagram ideas

```bash
curl --location --request POST 'http://localhost:8080/instagram_post_ideas/invoke' \
--header 'Content-Type: application/json' \
--header "Integrations-API-Key: dev-only-token" \
--data-raw '{
"input": {
"topics": "new ice cream for vegans",
"pitch": "cold but not cold killers",
"guidelines": "fun, quirky",
"inspiration": "",
"audience": "genz",
"number": "5"
}
}'
```

or

```bash
curl --location --request POST 'http://localhost:8080/instagram_post_ideas/invoke' \
--header 'Content-Type: application/json' \
--header "Integrations-API-Key: dev-only-token" \
--data-raw '{
"input": {
"topics": "Rust vs Java",
"pitch": "borrowing is better than collecting the garbage",
"guidelines": "fun, quirky",
"inspiration": "",
"audience": "Rust developers",
"number": "5"
}
}'
```

## Testing the search remotely
In order to run the server you will need to run the following command

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/instagram_post_ideas/invoke' \
--header 'Content-Type: application/json' \
--header "Integrations-API-Key: dev-only-token" \
--data-raw '{
"input": {
"topics": "new ice cream for vegans",
"pitch": "cold but not cold killers",
"guidelines": "fun, quirky",
"inspiration": "",
"audience": "genz",
"number": "5"
}
}'
```

or

```bash
curl --location --request POST 'https://langserve.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/instagram_post_ideas/invoke' \
--header 'Content-Type: application/json' \
--header "Integrations-API-Key: dev-only-token" \
--data-raw '{
"input": {
"topics": "Rust vs Java",
"pitch": "borrowing is better than collecting the garbage",
"guidelines": "fun, quirky",
"inspiration": "",
"audience": "Rust developers",
"number": "5"
}
}'
```
