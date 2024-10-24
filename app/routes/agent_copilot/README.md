# Agent Copilot Integration

This integration provides a streamlined interface for interacting with Azure OpenAI Assistants API.

## Available Endpoints

1. `/agent_copilot/{assistant_name}/invoke`: Invoke a conversation with a specific assistant
2. `/agent_copilot/assistants`: List available assistants

## Usage Examples

### List Available Assistants

```bash
curl --silent -X GET "http://localhost:8080/agent_copilot/assistants" \
     -H "Content-Type: application/json" \
     -H "Integrations-API-Key: dev-only-token" | jq
```

### Invoke AppMod Engineer Assistant

```bash
curl -X POST "http://localhost:8080/agent_copilot/appmod/invoke" \
     -H "Content-Type: application/json" \
     -H "Integrations-API-Key: dev-only-token" \
     -d '{
       "message": "Explain the process of application modernization."
     }'
```

### Invoke Migration Engineer Assistant

```bash
curl -X POST "http://localhost:8080/agent_copilot/migration/invoke" \
     -H "Content-Type: application/json" \
     -H "Integrations-API-Key: dev-only-token" \
     -d '{
       "message": "What are the key steps in a cloud migration project?"
     }'
```

## Environment Variables

Make sure to set the following environment variables:

```bash
export AGENT_COPILOT_ENDPOINT=https://va-gpt-4omni.openai.azure.com/
export AGENT_COPILOT_API_KEY=your_api_key_here
export AGENT_COPILOT_API_VERSION=2024-02-15-preview
```

Replace `your_api_key_here` with your actual Azure OpenAI API key.
