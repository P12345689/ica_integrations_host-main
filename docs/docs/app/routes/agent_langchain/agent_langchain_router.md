# Agent Langchain Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Agents](./index.md#agents) / Agent Langchain Router

> Auto-generated documentation for [app.routes.agent_langchain.agent_langchain_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/agent_langchain_router.py) module.

#### Attributes

- `DEFAULT_MAX_THREADS` - Constants: int(os.getenv('DEFAULT_MAX_THREADS', 4))

- `TEMPLATES_DIRECTORY` - Load Jinja2 environment: 'app/routes/agent_langchain/templates'

- `ALL_TOOLS` - Get all available tools: get_tools(['google_search', 'retrieve_website_content', 'mermaid_create_diagram', 'docbuilder_tool_markdown_to_pptx_docx', 'summarize_text_tool', 'get_system_time', 'get_collections_tool', 'query_documents_tool', 'GPT-4 Vision', 'pii_masker_tool', 'get_prompts_tool', 'get_assistants_tool', 'wikipedia_search', 'create_chart'])


- [Agent Langchain Router](#agent-langchain-router)
  - [InputModel](#inputmodel)
  - [OutputModel](#outputmodel)
  - [_handle_error](#_handle_error)
  - [add_custom_routes](#add_custom_routes)
  - [get_agent_response](#get_agent_response)
  - [get_selected_tools](#get_selected_tools)
  - [stream_agent_response](#stream_agent_response)

## InputModel

[Show source in agent_langchain_router.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/agent_langchain_router.py#L61)

Model for incoming request data to specify query, optional context, tools to use, model configuration, and prompt template.

#### Signature

```python
class InputModel(BaseModel): ...
```



## OutputModel

[Show source in agent_langchain_router.py:70](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/agent_langchain_router.py#L70)

Output format for streamed and non-streamed data.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## _handle_error

[Show source in agent_langchain_router.py:76](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/agent_langchain_router.py#L76)

Custom Error Function

#### Signature

```python
def _handle_error(error: str) -> str: ...
```



## add_custom_routes

[Show source in agent_langchain_router.py:212](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/agent_langchain_router.py#L212)

Adds custom routes to the FastAPI application for agent invocation and result retrieval.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## get_agent_response

[Show source in agent_langchain_router.py:165](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/agent_langchain_router.py#L165)

Gets the final response from an agent based on a given query and context.

#### Signature

```python
async def get_agent_response(
    query: str,
    tools: List[Tool],
    model: Union[ChatOpenAI, ChatConsultingAssistants, WatsonxLLM],
    prompt_template: PromptTemplate,
    context_items: List[ContextItem],
) -> Dict[str, Any]: ...
```



## get_selected_tools

[Show source in agent_langchain_router.py:81](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/agent_langchain_router.py#L81)

Get a list of tools based on the provided tool names.

#### Signature

```python
def get_selected_tools(tool_names: List[str]) -> List[Tool]: ...
```



## stream_agent_response

[Show source in agent_langchain_router.py:87](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/agent_langchain/agent_langchain_router.py#L87)

#### Signature

```python
async def stream_agent_response(
    query: str,
    tools: List[Tool],
    model: Union[ChatOpenAI, ChatConsultingAssistants, WatsonxLLM],
    prompt_template: PromptTemplate,
    context_items: List[ContextItem],
) -> Generator[str, None, None]: ...
```
