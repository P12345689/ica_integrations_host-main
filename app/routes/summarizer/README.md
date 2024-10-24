# Text Summarization Integration

> Author: Mihai Criveti

This integration provides services for summarizing long text using LangChain's various summarization methods.

## Features

- Multiple summarization methods: stuff, map_reduce, and refine
- Configurable summary type: bullets or paragraphs
- Adjustable summary length: short, medium, or long
- Output format options: plain text or Markdown
- Customizable style: business or casual
- Additional instructions for post-processing
- Configurable LLM parameters: context length and temperature
- Adjustable text chunking parameters for long documents

## Endpoints

- POST /experience/summarize/summarize_text/invoke
  Invokes the Experience API to summarize long text using various LangChain methods.

- POST /system/summarize/retrievers/get_text_stats/invoke
  Invokes the System API to provide statistics about the input text.

## Usage Examples

### Basic Text Summarization

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is a long text that needs to be summarized. It contains multiple sentences and paragraphs...",
        "summary_type": "bullets",
        "summary_length": "short",
        "output_format": "plain",
        "style": "business",
        "chain_type": "map_reduce"
    }'
```

### Summarize with Additional Instruction

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is a technical document describing a new software system...",
        "summary_type": "paragraphs",
        "summary_length": "medium",
        "output_format": "markdown",
        "style": "business",
        "chain_type": "refine",
        "additional_instruction": "Extract non-functional requirements from this document"
    }'
```

### Summarize File Content

To summarize the content of a file, you can use the `file.txt` syntax with `jq`

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data "$(jq -n --arg text "$(cat /path/to/your/file.txt)" \
                    '{
                        text: $text,
                        summary_type: "bullets",
                        summary_length: "long",
                        output_format: "markdown",
                        style: "casual",
                        chain_type: "stuff"
                    }')"
```

### Customizing LLM Parameters

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is a very long and detailed technical specification...",
        "summary_type": "paragraphs",
        "summary_length": "medium",
        "output_format": "plain",
        "style": "business",
        "chain_type": "map_reduce",
        "context_length": 8192,
        "temperature": 0.5,
        "chunk_size": 2000,
        "chunk_overlap": 300
    }'
```

### Extracting Specific Information

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is a comprehensive project proposal including budget, timeline, and resource allocation...",
        "summary_type": "bullets",
        "summary_length": "short",
        "output_format": "markdown",
        "style": "business",
        "chain_type": "refine",
        "additional_instruction": "Extract only the budget-related information from this proposal"
    }'
```

### Summarize a meeting transcript

```bash
curl --location --request POST 'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data "$(jq -n --arg text "$(cat transcript.srt)" \
                         --arg summary_type "bullets" \
                         --arg summary_length "short" \
                         --arg output_format "markdown" \
                         --arg style "business" \
                         --arg chain_type "map_reduce" \
                         --arg additional_instruction "Extract meeting minutes, a summary and actions from this meeting call transcript" \
                         '{
                             text: $text,
                             summary_type: $summary_type,
                             summary_length: $summary_length,
                             output_format: $output_format,
                             style: $style,
                             chain_type: $chain_type,
                             additional_instruction: $additional_instruction
                         }')"
```

### Summarizing in a Different Language

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is an English language document about climate change...",
        "summary_type": "paragraphs",
        "summary_length": "medium",
        "output_format": "plain",
        "style": "casual",
        "chain_type": "map_reduce",
        "additional_instruction": "Summarize this document in Spanish"
    }'
```

### Focusing on Specific Sections

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is a lengthy research paper with multiple sections including introduction, methodology, results, and conclusion...",
        "summary_type": "bullets",
        "summary_length": "short",
        "output_format": "markdown",
        "style": "business",
        "chain_type": "refine",
        "additional_instruction": "Focus on summarizing only the methodology and results sections"
    }'
```

### Comparing Different Summarization Methods

You can compare the results of different summarization methods by running multiple requests with different `chain_type` values:

1. Stuff method:
```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "Your long text here...",
        "chain_type": "stuff",
        "summary_type": "paragraphs",
        "summary_length": "medium"
    }'
```

2. Map-Reduce method:
```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "Your long text here...",
        "chain_type": "map_reduce",
        "summary_type": "paragraphs",
        "summary_length": "medium"
    }'
```

3. Refine method:
```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "Your long text here...",
        "chain_type": "refine",
        "summary_type": "paragraphs",
        "summary_length": "medium"
    }'
```

### Get Text Statistics

To get statistics about the input text without summarization:

```bash
curl --location --request POST \
    'http://localhost:8080/system/summarize/retrievers/get_text_stats/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "This is a sample text for getting statistics. It contains multiple sentences and various words."
    }'
```

## Advanced Usage

### Chunking Large Documents

For very large documents, you can adjust the `chunk_size` and `chunk_overlap` parameters to optimize processing:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "@/path/to/very_large_document.txt",
        "summary_type": "paragraphs",
        "summary_length": "long",
        "chain_type": "map_reduce",
        "chunk_size": 3000,
        "chunk_overlap": 500
    }'
```

### Adjusting LLM Behavior

You can fine-tune the LLM's behavior by adjusting the `context_length` and `temperature`:

```bash
curl --location --request POST \
    'http://localhost:8080/experience/summarize/summarize_text/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "text": "Your complex text here...",
        "summary_type": "bullets",
        "summary_length": "medium",
        "chain_type": "refine",
        "context_length": 8192,
        "temperature": 0.3
    }'
```

## Notes

- The `stuff` method is best for shorter texts that fit within the LLM's context window.
- The `map_reduce` method is efficient for very long documents but may lose some context between chunks.
- The `refine` method can provide more coherent summaries for long documents but may be slower than `map_reduce`.
- Adjust `chunk_size` and `chunk_overlap` based on the nature of your text. Larger chunks may preserve more context but require more processing time.
- Lower `temperature` values (e.g., 0.3) will make the output more deterministic, while higher values (e.g., 0.7) will introduce more randomness.
- The `additional_instruction` parameter can be used for various post-processing tasks such as translation, specific information extraction, or format conversion.
