# Local document retriever

This integration provides functionality for retrieving local .docx or .pptx files with MIME Types.

## Endpoints

- **POST /system/docx/invoke**
    Downloads a local .docx as a File.

- **POST /system/pptx/invoke**
    Downloads a local .pptx as a File.

## Testing the integration locally

### Retrieve .pptx files

```bash
curl --location --request POST 'http://localhost:8080/system/pptx/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
        "filename": "30cb047a2fab4eb88192952f21d76827.pptx"
     }'
```

### Retrieve .docx files

```bash
curl --location --request POST 'http://localhost:8080/system/docx/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
        "filename": "f8c4435ba91c49008d63f1aa5c886fc0.docx"
     }'
```
