# Config

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Agents](./index.md#agents) / Config

> Auto-generated documentation for [app.routes.agent_langchain.config](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/config.py) module.

#### Attributes

- `ModelConfig` - Define a type for the model configurations: Dict[str, str]

- `DEFAULT_MODEL_CONFIGS`: `Dict[str, ModelConfig]` - Define default model configurations with explicit type annotation: {'OPENAI': {'MODEL_NAME': 'gpt-4o-mini'}, 'AZURE_OPENAI': {'MODEL_NAME': 'gpt-4', 'DEPLOYMENT_NAME': 'scribeflowgpt4o'}, 'WATSONX': {'MODEL_NAME': 'mistralai/mistral-large'}, 'CONSULTING_ASSISTANTS': {'MODEL_NAME': 'Consulting Assistants Model'}, 'OLLAMA': {'MODEL_NAME': 'llama3.1'}, 'NVIDIA_NIM': {'MODEL_NAME': 'llama3.1'}}

- `MODEL_TYPE` - Determine which model to use based on environment variable: os.getenv('MODEL_TYPE', 'AZURE_OPENAI')

- `AZURE_OPENAI_API_KEY` - Azure OpenAI specific configurations: os.getenv('AZURE_OPENAI_API_KEY', '')

- `WATSONX_URL` - WatsonX specific configurations: os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')

- `OLLAMA_URL` - OLLAMA: os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434/v1')

- `NVIDIA_NIM_URL` - NVIDIA NIM: os.getenv('NVIDIA_NIM_URL', 'https://integrate.api.nvidia.com/v1')

- `DEFAULT_MAX_THREADS` - General Tool Execution Configuration: int(os.getenv('DEFAULT_MAX_THREADS', 4))


- [Config](#config)
  - [get_model](#get_model)

## get_model

[Show source in config.py:91](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/config.py#L91)

Returns the appropriate model based on the configuration or override parameters.

This function selects the model type based on an environment variable or override parameters
and initializes it with relevant configurations. It logs the initialization details for debugging purposes.

#### Arguments

llm_override (Optional[Tuple[str, str]]): A tuple containing (model_host, model_name) to override default settings.

#### Raises

- `ValueError` - If the specified model type is invalid.

#### Returns

Union[ChatOpenAI, AzureChatOpenAI, ChatConsultingAssistants, WatsonxLLM]: An instance of the specified model.

#### Signature

```python
def get_model(
    llm_override: Optional[Tuple[str, str]] = None,
) -> Union[ChatOpenAI, AzureChatOpenAI, ChatConsultingAssistants, WatsonxLLM]: ...
```
