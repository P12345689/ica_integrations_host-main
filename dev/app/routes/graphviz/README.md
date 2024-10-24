# Graphviz Integration

This integration provides functionality for creating diagrams using Graphviz.

## Usage

To use this integration, follow these steps:

1. Ensure you have the required dependencies installed, including Graphviz.
2. Set up the necessary environment variables (e.g., `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME`, `DEFAULT_MAX_THREADS`).
3. Include this module in your FastAPI application.

## API Endpoints

### POST /system/graphviz/generate_png/invoke

Generates a PNG file from provided Graphviz syntax.

```bash
curl --location --request POST 'http://localhost:8080/system/graphviz/generate_png/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "syntax": "digraph G { A -> B; B -> C; C -> A; }"
     }'
```

### POST /experience/graphviz/generate_diagram/invoke

Generates a Graphviz diagram based on a text description, using an LLM to create the syntax.

```bash
curl --location --request POST 'http://localhost:8080/experience/graphviz/generate_diagram/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Create a simple flowchart with three steps: Start, Process, and End"
     }'
```

Both endpoints return a response containing the URL of the generated PNG file and the Graphviz syntax used to generate it.
