# Prompt Guard Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / `attic` / `routes` / [Prompt Guard](./index.md#prompt-guard) / Prompt Guard Router

> Auto-generated documentation for [attic.routes.prompt_guard.prompt_guard_router](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/prompt_guard/templates'))

- `MODEL_PATH` - Set the path to the local model: Path('app/routes/prompt_guard/Prompt-Guard')

- `tokenizer` - Load model and tokenizer from the local directory: AutoTokenizer.from_pretrained(MODEL_PATH)


- [Prompt Guard Router](#prompt-guard-router)
  - [OutputModel](#outputmodel)
  - [PromptGuardInputModel](#promptguardinputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [evaluate_text](#evaluate_text)
  - [find_malicious_bits](#find_malicious_bits)
  - [get_class_probabilities](#get_class_probabilities)
  - [get_indirect_injection_score](#get_indirect_injection_score)
  - [get_jailbreak_score](#get_jailbreak_score)
  - [split_text](#split_text)

## OutputModel

[Show source in prompt_guard_router.py:54](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L54)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## PromptGuardInputModel

[Show source in prompt_guard_router.py:42](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L42)

Model to validate input data for Prompt Guard queries.

#### Signature

```python
class PromptGuardInputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in prompt_guard_router.py:49](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L49)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in prompt_guard_router.py:183](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L183)

Add custom routes to the FastAPI application.

#### Arguments

- [App](../../../app/index.md#app) *FastAPI* - The FastAPI application to add routes to.

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## evaluate_text

[Show source in prompt_guard_router.py:154](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L154)

Evaluate the input text for jailbreak and optionally indirect injection probabilities.

#### Arguments

- `text` *str* - The input text to evaluate.
- `temperature` *float* - The temperature for the softmax function.
- `include_indirect_injection` *bool* - Whether to include indirect injection score in the evaluation.

#### Returns

- `dict` - A dictionary containing jailbreak and optionally indirect injection scores, and malicious bits.

#### Signature

```python
async def evaluate_text(
    text: str, temperature: float = 1.0, include_indirect_injection: bool = False
) -> dict: ...
```



## find_malicious_bits

[Show source in prompt_guard_router.py:125](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L125)

Identify potentially malicious bits in the input text.

#### Arguments

- `text` *str* - The input text to analyze.
- `temperature` *float* - The temperature for the softmax function.
- `threshold` *float* - The score threshold above which a chunk is considered malicious.
- `include_indirect_injection` *bool* - Whether to include indirect injection score in the evaluation.

#### Returns

- `List[dict]` - A list of dictionaries containing information about malicious chunks.

#### Signature

```python
def find_malicious_bits(
    text: str,
    temperature: float = 1.0,
    threshold: float = 0.5,
    include_indirect_injection: bool = False,
) -> List[dict]: ...
```



## get_class_probabilities

[Show source in prompt_guard_router.py:60](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L60)

Evaluate the model on the given text with temperature-adjusted softmax.

#### Arguments

- `text` *str* - The input text to classify.
- `temperature` *float* - The temperature for the softmax function.

#### Returns

- `torch.Tensor` - The probability of each class adjusted by the temperature.

#### Signature

```python
def get_class_probabilities(text: str, temperature: float = 1.0) -> torch.Tensor: ...
```



## get_indirect_injection_score

[Show source in prompt_guard_router.py:93](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L93)

Evaluate the probability that a given string contains any embedded instructions.

#### Arguments

- `text` *str* - The input text to evaluate.
- `temperature` *float* - The temperature for the softmax function.

#### Returns

- `float` - The probability of the text containing embedded instructions.

#### Signature

```python
def get_indirect_injection_score(text: str, temperature: float = 1.0) -> float: ...
```



## get_jailbreak_score

[Show source in prompt_guard_router.py:79](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L79)

Evaluate the probability that a given string contains malicious jailbreak or prompt injection.

#### Arguments

- `text` *str* - The input text to evaluate.
- `temperature` *float* - The temperature for the softmax function.

#### Returns

- `float` - The probability of the text containing malicious content.

#### Signature

```python
def get_jailbreak_score(text: str, temperature: float = 1.0) -> float: ...
```



## split_text

[Show source in prompt_guard_router.py:107](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/prompt_guard/prompt_guard_router.py#L107)

Split the input text into chunks of maximum token length.

#### Arguments

- `text` *str* - The input text to split.
- `max_tokens` *int* - The maximum number of tokens per chunk.

#### Returns

- `List[str]` - A list of text chunks.

#### Signature

```python
def split_text(text: str, max_tokens: int = 512) -> List[str]: ...
```
