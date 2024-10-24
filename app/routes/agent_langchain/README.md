# Agents

> Author: Mihai Criveti

Streaming API for langchain agents with tool selection capability and dynamic model configuration.

## TODO:

1. Add support for configurable tags:
```json
"assistants_tags": ["1231231"],
"document_collection": ["1231231"],
"prompt_tags": ["1231231"]
```
2. Retrieve list of tools from Integrations Catalog, allowing full dynamic configuration.
3. Create a tool that is a REST API based tool.
4. Generic tool that finds the right tool by listing the catalog.

## Endpoints

- **POST /agent_langchain/invoke**
  Invokes an agent. It expects a JSON payload with a `query`, and optionally `context`, `use_context`, `tools`, and `llm_override`.

- **POST /agent_langchain/result**
  Gets the final result from an agent. It expects the same JSON payload as the `/invoke` endpoint.

## Input Parameters

- `query` (required): The question or task for the agent.
- `context` (optional): A stringified JSON array of context items. Each item should have `content` and `type` fields.
- `use_context` (optional): A boolean indicating whether to use the provided context. Defaults to `false`.
- `tools` (optional): A list of tool names to use for the query. This can be provided as:
  - An array of strings (e.g., `["tool_a", "tool_b"]`)
  - A comma-separated string (e.g., `"tool_a,tool_b"`)
  - A JSON string of an array (e.g., `"[\"tool_a\",\"tool_b\"]"`)
  If not provided or empty, all available tools will be used.
- `llm_override` (optional): A tuple of (model_host, model_name) to override the default model configuration.

## Specifying Tools

You can specify which tools the agent should use in several ways:

1. As a JSON array:
   ```json
   "tools": ["tool_a", "mermaid_create_diagram"]
   ```

2. As a comma-separated string:
   ```json
   "tools": "tool_a,tool_b"
   ```

3. As a JSON string of an array:
   ```json
   "tools": "[\"tool_a\",\"mermaid_create_diagram\"]"
   ```

The agent will parse these inputs and use only the specified tools. If no tools are specified or the list is empty, all available tools will be used.

## Model Configurations

The following model configurations are available:

1. OpenAI
2. Azure OpenAI
3. Watsonx
4. Consulting Assistants

You can select a model configuration either by setting the `MODEL_TYPE` environment variable or by using the `llm_override` parameter in your API request.

## Environment Configuration

### General Configuration

- `CLEAN_CONTEXT`: Set to "true" to enable cleaning triple backslash escapes in the context.
- `MODEL_TYPE`: Set to "OPENAI", "AZURE_OPENAI", "WATSONX", or "CONSULTING_ASSISTANTS" to select the default model type.
- `MODEL_NAME`: Set to the specific model name within the selected model type.

### OpenAI Configuration

When using OpenAI models, set the following environment variables:

```
export MODEL_TYPE="OPENAI"
export MODEL_NAME="gpt-4"  # or any other available OpenAI model
export OPENAI_API_KEY="your-openai-api-key"
```

### Azure OpenAI Configuration

For Azure OpenAI, use these environment variables:

```bash
export MODEL_TYPE="AZURE_OPENAI"
export MODEL_NAME="gpt-4"  # or your deployed model name
export AZURE_OPENAI_API_KEY="your-azure-openai-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment-name"
export AZURE_OPENAI_API_VERSION="2023-05-15"  # or the latest available version
```

### Watsonx Configuration

For Watsonx, set these environment variables:

```bash
export MODEL_TYPE="WATSONX"
export MODEL_NAME="mistralai/mistral-large"  # or your chosen Watsonx model
export WATSONX_URL="https://us-south.ml.cloud.ibm.com"  # or your specific endpoint
export WATSONX_PROJECT_ID="your-project-id"
export WATSONX_API_KEY="your-watsonx-api-key"
export WATSONX_DECODING_METHOD="sample"
export WATSONX_MAX_NEW_TOKENS=8000
export WATSONX_MIN_NEW_TOKENS=1
export WATSONX_TEMPERATURE=0.1
export WATSONX_TOP_K=50
export WATSONX_TOP_P=1.0
```

### Consulting Assistants Configuration

For Consulting Assistants, use:

```bash
export MODEL_TYPE="CONSULTING_ASSISTANTS"
export MODEL_NAME="Mixtral Large"  # or your specific model name
# Ensure that you have your .env configured with icacli settings.
```

## Using the agents

### Basic Query with Tool Selection

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "should i bring a brolly with me for my trip to london just now?",
            "tools": ["google_search", "get_system_time"]
    }'
```

or

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "should i bring a brolly with me for my trip to london just now?",
            "tools": "google_search,get_system_time"
    }'
```

### Query with Context, Tool Selection, and Model Override

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "What did I just say?",
            "context": "[{\"content\":\"What is OpenShift\",\"type\":\"PROMPT\"},{\"content\":\"OpenShift is a containerization and orchestration platform for deploying and managing applications using Kubernetes. It provides a simple and efficient way to manage containers and application services, enabling developers to focus on building their applications instead of managing the underlying infrastructure.\",\"type\":\"ANSWER\"}]",
            "use_context": true,
            "tools": ["query_documents_tool"],
            "llm_override": ["OPENAI", "gpt-4"]
    }'
```

## Using a Custom Prompt Template

You can provide a custom prompt template in your API request using the `prompt_template` parameter. Here's an example using the default prompt template:

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "What is the latest news on Paris",
            "tools": ["google_search"],
            "llm_override": ["OPENAI", "gpt-4o-mini"],
            "prompt_template": "You are an AI assistant. Use the following pieces of context to answer the human'\''s question:\\nContext: {context}\\n\\nAnswer the following questions as best you can.\\nAlso provide the VERBATIM citations for the sources refered in the end of the response.\\nStop if you arrive at the final answer.\\nDo not output an Action and a Final Answer at the same time.\\n\\nYou have access to the following tools:\\n\\n{tools}\\n\\nUse the following format. Do not leave out the colon:\\n\\nQuestion: the input question you must answer\\nThought: you should always think about what to do\\nAction: the action to take, should be one of [{tool_names}]\\nAction Input: the input to the action\\nObservation: the result of the action\\n... (this Thought/Action/Action Input/Observation can repeat N times)\\nThought: I now know the final answer\\nFinal Answer: the final answer to the original input question\\n\\nBegin!\\n\\nQuestion: {input}\\nThought: {agent_scratchpad}"
    }'
```

Or with context, using the streaming API, with a filter on the various assistants and document_collection tags:

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "What is the latest news on this topic?",
            "tools": "google_search,retrieve_website_content",
            "llm_override": ["WATSONX", "mistralai/mistral-large"],
            "context": "[{\"content\":\"What is OpenShift\",\"type\":\"PROMPT\"},{\"content\":\"OpenShift is a containerization and orchestration platform for deploying and managing applications using Kubernetes. It provides a simple and efficient way to manage containers and application services, enabling developers to focus on building their applications instead of managing the underlying infrastructure.\",\"type\":\"ANSWER\"}]",
            "use_context": true,
            "prompt_template": "You are an AI assistant. Use the following pieces of context to answer the human'\''s question:\\nContext: {context}\\n\\nAnswer the following questions as best you can.\\nAlso provide the VERBATIM citations for the sources refered in the end of the response.\\nStop if you arrive at the final answer.\\nDo not output an Action and a Final Answer at the same time.\\n\\nYou have access to the following tools:\\n\\n{tools}\\n\\nUse the following format. Do not leave out the colon:\\n\\nQuestion: the input question you must answer\\nThought: you should always think about what to do\\nAction: the action to take, should be one of [{tool_names}]\\nAction Input: the input to the action\\nObservation: the result of the action\\n... (this Thought/Action/Action Input/Observation can repeat N times)\\nThought: I now know the final answer\\nFinal Answer: the final answer to the original input question\\n\\nBegin!\\n\\nQuestion: {input}\\nThought: {agent_scratchpad}"
    }'
```

Note the following when using a custom prompt template:

- Escape newlines with `\\n` in the JSON string.
- Escape single quotes with `'\''` to ensure proper JSON formatting.
- Make sure to include all necessary placeholders: `{context}`, `{tools}`, `{tool_names}`, `{input}`, and `{agent_scratchpad}`.
- You can modify the instructions, format, or add additional context as needed in your custom template.

By providing a custom prompt template, you can tailor the agent's behavior and output format to your specific needs while still leveraging the underlying LangChain agent functionality.

### Using Google, Wikipedia and Powerpoint with Azure OpenAI

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "Give me a brief biography of Jerry Cuomo (use multiple sources)",
            "tools": ["google_search", "wikipedia_search", "docbuilder_tool_markdown_to_pptx_docx"],
            "llm_override": ["AZURE_OPENAI", "gpt-4"]
    }'
```

### Using Website Up or Healthy with Watsonx

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "is the ibm website up",
            "tools": ["retrieve_website_content"],
            "llm_override": ["WATSONX", "mistralai/mistral-large"]
    }'
```

### Using Mermaid and Powerpoint with Consulting Assistants

```bash
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
            "query": "generate an organization chart diagram for the microsoft executive team",
            "tools": ["mermaid_create_diagram", "docbuilder_tool_markdown_to_pptx_docx", "google_search"],
            "llm_override": ["CONSULTING_ASSISTANTS", "Consulting Assistants Model"]
    }'
```

## Note on Tool Selection

- If the `tools` array is not provided or is empty in the request, all available tools will be used.
- If specific tools are listed in the `tools` array, only those tools will be available for the agent to use during that particular request.
- Invalid tool names in the `tools` array will be ignored, and the agent will proceed with the valid tools.

## Note on Model Selection

- If `llm_override` is not provided, the default model configuration (set by environment variables) will be used.
- The `llm_override` parameter allows you to switch between different model hosts and specific models for each request.
- Ensure that the necessary environment variables are set for the selected model type, as outlined in the Environment Configuration section.

Remember to choose appropriate tools and models based on the task at hand to optimize the agent's performance and response time. Also, ensure that you have the necessary API keys and access rights for the model type you're using.

## Security Note

- Never expose these variables in public repositories or insecure environments.
- Consider using a secure secrets management system in production environments.
