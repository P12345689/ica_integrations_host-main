# File Retriever Integration

> Author: Mihai Criveti

This integration provides services for retrieving files from URLs, converting them to text, and optionally analyzing the content using an LLM.

## Endpoints

- POST /system/file_retriever/retrievers/get_file_content/invoke
  Invokes the System API to retrieve a file from a URL and convert it to text.

- POST /file_retriever/invoke
  An alias for the system API endpoint.

- POST /experience/file_retriever/ask_file_content/invoke
  Invokes the Experience API to retrieve a file, convert it to text, and analyze it using an LLM.

## Supported File Types

The integration supports the following file types:
- PDF (.pdf)
- Microsoft Word (.docx)
- Microsoft PowerPoint (.pptx)
- Microsoft Excel (.xlsx)
- CSV (.csv)
- HTML (.html)
- Plain Text (.txt)
- Python (.py)

## Testing the integration locally

### Get File Content - System API

This endpoint retrieves a file from a URL and converts it to text.

```bash
curl --location --request POST \
    'http://localhost:8080/system/file_retriever/retrievers/get_file_content/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "url": "https://pdfobject.com/pdf/sample.pdf"
    }'
```

### Ask File Content - Experience API

This endpoint retrieves a file, converts it to text, and analyzes it using an LLM.

```bash
curl --location --request POST \
    'http://localhost:8080/experience/file_retriever/ask_file_content/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "url": "https://pdfobject.com/pdf/sample.pdf"
    }'
```

## Error Handling

If an unsupported file type is provided, the integration will return an error message indicating that the file type is not supported for conversion.