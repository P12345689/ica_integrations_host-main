# Summarizer Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Summarizer Tool

> Auto-generated documentation for [app.tools.global_tools.summarizer_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/summarizer_tool.py) module.

#### Attributes

- `global_summarize_text` - Create a global variable to store the summarize_text function: None


- [Summarizer Tool](#summarizer-tool)
  - [initialize_summarize_text](#initialize_summarize_text)
  - [summarize_text_tool](#summarize_text_tool)

## initialize_summarize_text

[Show source in summarizer_tool.py:36](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/summarizer_tool.py#L36)

Initialize the global summarize_text function.

#### Signature

```python
def initialize_summarize_text() -> None: ...
```



## summarize_text_tool

[Show source in summarizer_tool.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/summarizer_tool.py#L52)

Tool for summarizing text using configurable LangChain methods.

#### Arguments

- `text` *str* - The long text to be summarized.
- `style` *str, optional* - Style of the summary ("business" or "casual"). Defaults to "business".
- `output_format` *str, optional* - Output format of the summary ("plain" or "markdown"). Defaults to "plain".
- `summary_type` *str, optional* - Type of summary output ("bullets" or "paragraphs"). Defaults to "bullets".
- `summary_length` *str, optional* - Length of the summary ("short", "medium", or "long"). Defaults to "medium".
- `additional_instruction` *str, optional* - Additional instruction for the summarizer. Defaults to "".

#### Returns

- `str` - The summarized text.

#### Raises

- `ValueError` - If the input text is empty or invalid.

#### Examples

```python
>>> text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
>>> summary = summarize_text_tool(text, style="casual", summary_type="paragraphs", summary_length="short")
>>> print(summary)
A concise summary of the given text...
```

#### Signature

```python
@tool
def summarize_text_tool(
    text: str,
    style: Optional[str] = "business",
    output_format: Optional[str] = "plain",
    summary_type: Optional[str] = "bullets",
    summary_length: Optional[str] = "medium",
    additional_instruction: Optional[str] = "",
) -> str: ...
```
