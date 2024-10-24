# Pii Masker Tool

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Tools](../index.md#tools) / [Global Tools](./index.md#global-tools) / Pii Masker Tool

> Auto-generated documentation for [app.tools.global_tools.pii_masker_tool](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/pii_masker_tool.py) module.

- [Pii Masker Tool](#pii-masker-tool)
  - [pii_masker_tool](#pii_masker_tool)

## pii_masker_tool

[Show source in pii_masker_tool.py:17](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/tools/global_tools/pii_masker_tool.py#L17)

Tool for masking PII in the given text.

#### Arguments

- `text` *str* - The input text containing PII.
- `mask_type` *str* - The type of masking to apply ("delete", "mask", or "fake").
- `pii_types` *List[str]* - Types of PII to mask (e.g., ["credit_card", "name", "email"]).
- `custom_regex` *Optional[str]* - Custom regex pattern for PII detection.

#### Returns

- `str` - The text with masked PII.

#### Signature

```python
@tool
def pii_masker_tool(
    text: str,
    mask_type: str = "mask",
    pii_types: List[str] = ["credit_card"],
    custom_regex: Optional[Dict[str, str]] = None,
    encryption_key: Optional[str] = None,
) -> str: ...
```
