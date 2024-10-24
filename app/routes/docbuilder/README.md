# Document Builder

> Author: Mihai Criveti

Document Builder is a service that generates pptx and docx documents from input markdown or topic text. It can create structured presentations and documents based on user input, leveraging AI to expand on topics when necessary.

## Requirements

- Pandoc document converter
  - For Linux/WSL: `sudo apt-get -y install pandoc`
  - For macOS: `brew install pandoc`

## Environment Variables

Set the following environment variables before running the service:

- `SERVER_NAME`: The hostname of the server (e.g., `export SERVER_NAME=http://localhost:8080`). This is used to generate URLs for the created documents.
- `DEBUG`: Set to `1` to enable debug logging (optional, e.g., `export DEBUG=1`).
- `DEFAULT_MAX_THREADS`: Maximum number of threads for concurrent processing (default is 4, e.g., `export DEFAULT_MAX_THREADS=8`).
- `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME`: The default AI model to use (e.g., `export ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME="Llama3.1 70b Instruct"`).

## Endpoints

- **POST /experience/docbuilder/generate_docs/invoke**
  Invokes the docbuilder process. It expects a JSON payload with the following structure:
  ```json
  {
    "input_text": "Topic or content for the document",
    "template_type": "IBM Consulting Green",
    "author_name": "John Doe",
    "author_email": "john.doe@example.com",
    "context": "Optional context or previous conversation",
    "llm_override": "Optional alternative LLM model name"
  }
  ```

## Templates

Available template types:
- "default"
- "IBM Consulting Green"
- "IBM Consulting Blue"
- "IBM Technology Blue"
- "IBM Technology Green"
- "Services Integration Hub"
- "Corporate Strategy"
- "OIC"

## Testing

Here are multiple examples of how to use the Document Builder API:

1. Basic usage with minimal input:

```bash
curl --location --request POST 'http://localhost:8080/experience/docbuilder/generate_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "input_text": "The impact of artificial intelligence on modern society"
    }'
```

2. Using a specific template and providing author information:

```bash
curl --location --request POST 'http://localhost:8080/experience/docbuilder/generate_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "input_text": "Sustainable energy solutions for the 21st century",
        "template_type": "IBM Technology Green",
        "author_name": "Jane Smith",
        "author_email": "jane.smith@example.com"
    }'
```

3. Providing context for a more tailored presentation:

```bash
curl --location --request POST 'http://localhost:8080/experience/docbuilder/generate_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "input_text": "The future of work in a post GenAI world",
        "template_type": "IBM Consulting Blue",
        "author_name": "Alex Johnson",
        "author_email": "alex.johnson@example.com",
        "context": "Previous discussion focused on remote work technologies and their impact on productivity."
    }'
```

4. Using pre-formatted markdown input:

```bash
curl --location --request POST 'http://localhost:8080/experience/docbuilder/generate_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "input_text": "% Cybersecurity Best Practices\n% Security Team\n% 2023-08-11\n\n# Introduction\n\n## Why Cybersecurity Matters\n\n- Protecting sensitive data\n- Maintaining customer trust\n- Complying with regulations\n\n::: notes\nEmphasize the increasing importance of cybersecurity in the digital age\n:::\n\n## Common Cyber Threats\n\n- Phishing attacks\n- Malware\n- Ransomware\n\n::: notes\nProvide recent examples of major cyber attacks\n:::\n\n# Best Practices\n\n## Strong Password Policies\n\n- Use complex, unique passwords\n- Implement multi-factor authentication\n- Regular password updates\n\n::: notes\nDemonstrate a strong password example\n:::\n\n## Regular Software Updates\n\n- Keep all systems and software up-to-date\n- Enable automatic updates when possible\n- Patch management for large organizations\n\n::: notes\nExplain how updates address security vulnerabilities\n:::\n",
        "template_type": "Corporate Strategy"
    }'
```

5. Using an alternative LLM model:

```bash
curl --location --request POST 'http://localhost:8080/experience/docbuilder/generate_docs/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "input_text": "The role of quantum computing in cryptography",
        "template_type": "IBM Technology Blue",
        "author_name": "Dr. Quantum",
        "author_email": "dr.quantum@example.com",
        "llm_override": "Llama3.1 70b Instruct"
    }'
```

## Response

The API will respond with a JSON object containing:
- `status`: The status of the request (e.g., "success")
- `invocationId`: A unique identifier for the request
- `response`: An array of response messages, including:
  - URLs for the generated .docx and .pptx files
  - The cleaned markdown content (if generated by AI)

## Error Handling

If an error occurs, the API will respond with an appropriate HTTP status code and an error message in the response body.

## Notes

- The service uses an AI model to expand on topics when the input is not in markdown format. The quality and content of the generated presentations may vary.
- Generated documents are temporarily stored and accessible via the provided URLs. Ensure proper security measures are in place in a production environment.
- The `llm_override` parameter allows users to specify an alternative LLM model for content generation. If not provided, the default model specified in the environment variables will be used.
- This service is currently in development and may require further testing and refinement.

## Recent Updates

- Added support for specifying an alternative LLM model using the `llm_override` parameter.
- Updated the markdown cleaning function to better handle various input formats, including those starting with triple backticks.
- Improved error handling and logging throughout the application.
- Updated the prompt template to generate more consistent and well-structured Pandoc-compatible markdown.
