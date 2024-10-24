# Prompt Defender Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Prompt Defender](./index.md#prompt-defender) / Prompt Defender Router

> Auto-generated documentation for [app.routes.prompt_defender.prompt_defender_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py) module.

#### Attributes

- `MODEL_TYPE` - Constants: os.getenv('MODEL_TYPE', 'CONSULTING_ASSISTANTS')

- `WATSONX_MODEL_ID` - WatsonX Configuration: os.getenv('WATSONX_MODEL_ID', 'mistralai/mistral-large')

- `RULES_DIR` - File paths: 'app/routes/prompt_defender/rules'

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader(TEMPLATES_DIR))


- [Prompt Defender Router](#prompt-defender-router)
  - [DetectionMethod](#detectionmethod)
  - [OutputModel](#outputmodel)
  - [PromptDefenderConfig](#promptdefenderconfig)
  - [PromptDefenderInputModel](#promptdefenderinputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [get_model](#get_model)
  - [llm_analysis](#llm_analysis)
  - [load_config](#load_config)
  - [load_rules](#load_rules)
  - [regex_check](#regex_check)

## DetectionMethod

[Show source in prompt_defender_router.py:55](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L55)

#### Signature

```python
class DetectionMethod(BaseModel): ...
```



## OutputModel

[Show source in prompt_defender_router.py:78](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L78)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## PromptDefenderConfig

[Show source in prompt_defender_router.py:59](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L59)

Configuration model for Prompt Defender.

#### Signature

```python
class PromptDefenderConfig(BaseModel): ...
```



## PromptDefenderInputModel

[Show source in prompt_defender_router.py:67](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L67)

Model to validate input data for Prompt Defender.

#### Signature

```python
class PromptDefenderInputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in prompt_defender_router.py:73](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L73)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in prompt_defender_router.py:202](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L202)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## get_model

[Show source in prompt_defender_router.py:84](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L84)

Returns the appropriate model based on the MODEL_TYPE environment variable.

#### Signature

```python
def get_model() -> Union[ChatOpenAI, ChatConsultingAssistants, WatsonxLLM]: ...
```



## llm_analysis

[Show source in prompt_defender_router.py:169](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L169)

Perform LLM-based analysis to detect potential prompt injection.

#### Signature

```python
async def llm_analysis(prompt: str, threshold: float) -> bool: ...
```



## load_config

[Show source in prompt_defender_router.py:111](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L111)

Load configuration from file.

#### Signature

```python
def load_config() -> PromptDefenderConfig: ...
```

#### See also

- [PromptDefenderConfig](#promptdefenderconfig)



## load_rules

[Show source in prompt_defender_router.py:123](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L123)

Load regex patterns from specified rule set and language(s).

#### Signature

```python
def load_rules(rule_set: str, languages: Union[str, List[str]] = "all") -> List[str]: ...
```



## regex_check

[Show source in prompt_defender_router.py:148](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/prompt_defender/prompt_defender_router.py#L148)

Check if the prompt matches any of the given regex patterns.
This function is case-insensitive and ignores variations in whitespace.

#### Signature

```python
def regex_check(prompt: str, patterns: List[str]) -> bool: ...
```
