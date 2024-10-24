# XLSX Builder Integration

> Author: Mihai Criveti

This integration provides functionality for creating XLSX files from CSV data or natural language descriptions. It is designed to support a range of use cases, from simple data exports to complex multi-sheet spreadsheets.

## TODO

- Add `config.py`
- Add conversational history
- Support multiple models, each with its own prompt template
- Try multiple outputs in the prompt template (JSON, XML, YAML, MARKDOWN)
- Intermediate cleanup step
- Add `max_tokens` to `prompt_flow`
- Unit testing
- Move `OutputModel` and `ResponseMessageModel` to a global directory

## Usage

To use this integration:

1. **Set Up Environment Variables**: Ensure the following environment variables are set:
   - `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME` (Default: `"Llama3.1 70b Instruct"`)
   - `DEFAULT_MAX_THREADS` (Default: `4`)

2. **Include the Module**: Integrate the provided module into your FastAPI application.

## API Endpoints

### POST /system/xlsx_builder/generate_xlsx/invoke

Generates an XLSX file from provided CSV data.

**Request**

```bash
curl --location --request POST 'http://localhost:8080/system/xlsx_builder/generate_xlsx/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
      "csv_data": {
          "Employee Data": "Name,Age,City\nJohn,30,New York\nJane,25,Los Angeles\nBob,35,Chicago"
      }
  }'
```

**Request Parameters**

- `csv_data` (object): Dictionary of CSV data strings keyed by sheet name.
- `file_name` (str) Optional: Optional file_name for the excel to be generated

**Response**

The response contains the URL of the generated XLSX file.

```json
{
  "status": "success",
  "invocationId": "unique-id",
  "response": [
    {
      "message": "XLSX file generated successfully. You can download it from: http://localhost:8080/public/xlsx_builder/xlsx_unique-id.xlsx",
      "type": "text"
    }
  ]
}
```

### POST /experience/xlsx_builder/generate_xlsx/invoke

Generates an XLSX file based on a natural language query.

**Request**

```bash
curl --location --request POST 'http://localhost:8080/experience/xlsx_builder/generate_xlsx/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Create an XLSX file with a list of 5 popular books, including their titles, authors, and publication years."
     }'
```

**Request Parameters**

- `query` (string): A natural language description of the desired XLSX content.

## Examples

### Example 1: Simple Single-Sheet CSV Data

**Request**

```bash
curl --location --request POST 'http://localhost:8080/system/xlsx_builder/generate_xlsx/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
      "csv_data": {
          "Product Data": "Product,Price,Quantity\nLaptop,1000,50\nPhone,500,200"
      }
  }'
```

### Example 2: Multi-Sheet CSV Data

**Request**

```bash
curl --location --request POST 'http://localhost:8080/system/xlsx_builder/generate_xlsx/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
      "csv_data": {
        "Products": "Product,Price,Stock\nLaptop,1000,50\nPhone,500,200",
        "Sales": "Product,Sales\nLaptop,20000\nPhone,100000"
      }
  }'
```


### Example 3: Complex Multi-Sheet with Additional Metadata

**Request**

```bash
curl --location --request POST 'http://localhost:8080/system/xlsx_builder/generate_xlsx/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{
      "csv_data": {
        "Employee Details": "Name,Age,Position\nJohn Doe,30,Engineer\nJane Smith,25,Designer",
        "Department Overview": "Department,Head\nEngineering,John Doe\nDesign,Jane Smith"
      }
  }'
```

### Example 4: Natural Language Request for Simple Data

**Request**

```bash
curl --location --request POST 'http://localhost:8080/experience/xlsx_builder/generate_xlsx/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Create an XLSX file with a list of 5 popular books, including their titles, authors, and publication years."
     }'
```

### Example 5: Natural Language Request for Multi-Sheet Data

**Request**

```bash
curl --location --request POST 'http://localhost:8080/experience/xlsx_builder/generate_xlsx/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Generate an XLSX file with two sheets: one for a list of popular movies and another for their box office earnings."
     }'
```

### Example 6: Natural Language Request for Detailed Data

**Request**

```bash
curl --location --request POST 'http://localhost:8080/experience/xlsx_builder/generate_xlsx/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Create an XLSX file with a summary of quarterly financial reports for the past three years. Include income, expenses, and net profit for each quarter."
     }'
```


### Example 7: Complex Multi-Sheet Data with Nested Information

**Request**

```bash
curl --location --request POST 'http://localhost:8080/experience/xlsx_builder/generate_xlsx/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Generate an XLSX file with three sheets: one for employee details, one for department information, and one for project assignments. Include relevant data in each sheet."
     }'
```
