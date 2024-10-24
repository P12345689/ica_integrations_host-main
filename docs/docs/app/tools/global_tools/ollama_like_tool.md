# Ollama Like Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Ollama Like Tool

> Auto-generated documentation for [app.tools.global_tools.ollama_like_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ollama_like_tool.py) module.

- [Ollama Like Tool](#ollama-like-tool)
  - [generate_text](#generate_text)

## generate_text

[Show source in ollama_like_tool.py:17](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/ollama_like_tool.py#L17)

Tool for generating text using an Ollama-like interface.

#### Arguments

- `model` *str* - The model to use for generation.
- `prompt` *str* - The prompt for text generation.
- `system` *str, optional* - Optional system message.
- `template` *str, optional* - Optional template for formatting.
- `context` *str, optional* - Optional context for generation.
- `options` *dict, optional* - Optional generation options.

#### Returns

- `str` - The generated text.

#### Examples

```python
>>> result = generate_text("llama2", "Tell me a joke about programming.")
>>> assert isinstance(result, str)
>>> assert len(result) > 0
```

#### Signature

```python
@tool
def generate_text(
    model: str,
    prompt: str,
    system: Optional[str] = None,
    template: Optional[str] = None,
    context: Optional[str] = None,
    options: Optional[dict] = None,
) -> str: ...
```
