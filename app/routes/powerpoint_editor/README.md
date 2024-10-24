# PowerPoint Editor Integration

> Author: Mihai Criveti

This integration provides functionality for processing PowerPoint presentations based on meeting minutes or reviewer notes, using an LLM to generate content for predefined placeholders.

## Requirements

To use this integration, follow these steps:

1. Ensure you have the required dependencies installed. Update `requirements.txt` to include `python-pptx`, `pydantic`, `fastapi`, `pyyaml`, and necessary LangChain libraries.
2. Set up the (optional) environment variables: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_ENGINE`, `SERVER_NAME`.
3. Include this module in your FastAPI application.

## Endpoint

- **POST /system/powerpoint_editor/process/invoke**
    Processes a PowerPoint presentation based on provided notes and configuration, returning the URL of the processed file and details of the replacements made.

## Testing the integration locally

### Processing a PowerPoint with default settings

```bash
curl --silent --location --request POST 'http://localhost:8080/system/powerpoint_editor/process/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "notes": "Client ABC needs a new CRM system to improve customer engagement. Key requirements include integration with existing systems, mobile access, and advanced analytics capabilities. Timeline is 6 months with a budget of $500,000.",
         "author_name": "John Doe",
         "author_email": "john.doe@example.com"
     }' | jq -r '.response[0].message'
```

With a custom LLM:

```bash
curl --silent --location --request POST 'http://localhost:8080/system/powerpoint_editor/process/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "notes": "Project XYZ aims to develop a machine learning model for predictive maintenance in manufacturing. The model should reduce downtime by 30% and integrate with IoT sensors already in place.",
         "llm_override": ["AZURE_OPENAI", "scribeflowgpt4o"],
         "author_name": "Jane Smith",
         "author_email": "jane.smith@example.com"
     }' | jq -r '.response[0].message'
```


### Using a custom template and LLM override

```bash
curl --silent --location --request POST 'http://localhost:8080/system/powerpoint_editor/process/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "notes": "Project XYZ aims to develop a machine learning model for predictive maintenance in manufacturing. The model should reduce downtime by 30% and integrate with IoT sensors already in place.",
         "template_url": "https://example.com/custom_template.pptx",
         "llm_override": ["WATSONX", "meta-llama/llama-3-1-8b-instruct"],
         "author_name": "Jane Smith",
         "author_email": "jane.smith@example.com"
     }' | jq -r '.response[0].message'
```

### Providing custom configuration

```bash
curl --silent --location --request POST 'http://localhost:8080/system/powerpoint_editor/process/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "notes": "Startup ABC is looking to launch a new fintech app. They need assistance with regulatory compliance, user acquisition strategies, and securing Series A funding.",
         "config_data": "main_prompt: Generate concise content for a startup pitch deck.\nreplacements:\n  - placeholder: \"{executive_summary}\"\n    prompt: \"Summarize the startup'\''s vision and value proposition\"\n    instructions: \"Focus on the unique selling points and market opportunity\"\n    max_tokens: 50\n  - placeholder: \"{financial_projections}\"\n    prompt: \"Provide key financial metrics and projections\"\n    instructions: \"Include revenue forecast, burn rate, and break-even point\"\n    max_tokens: 30",
         "author_name": "Alex Johnson",
         "author_email": "alex.johnson@example.com"
     }' | jq -r '.response[0].message'
```

### Using a custom template file and LLM override

```bash
curl --silent --location --request POST 'http://localhost:8080/system/powerpoint_editor/process/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     -F 'template=@/path/to/your/custom_template.pptx' \
     -F 'data={
         "notes": "Project XYZ aims to develop a machine learning model for predictive maintenance in manufacturing. The model should reduce downtime by 30% and integrate with IoT sensors already in place.",
         "llm_override": ["AZURE_OPENAI", "scribeflowgpt4o"],
         "author_name": "Jane Smith",
         "author_email": "jane.smith@example.com",
         "date": "2024-09-15"
     }'
```

### Providing custom configuration and additional context

```bash
curl --silent --location --request POST 'http://localhost:8080/system/powerpoint_editor/process/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "notes": "Startup ABC is looking to launch a new fintech app. They need assistance with regulatory compliance, user acquisition strategies, and securing Series A funding.",
         "context": "The fintech market is currently experiencing rapid growth, with a 25% year-over-year increase in mobile banking users.",
         "config_data": "main_prompt: Generate concise content for a startup pitch deck.\nreplacements:\n  - placeholder: \"{executive_summary}\"\n    prompt: \"Summarize the startup'\''s vision and value proposition\"\n    instructions: \"Focus on the unique selling points and market opportunity\"\n    max_tokens: 50\n  - placeholder: \"{financial_projections}\"\n    prompt: \"Provide key financial metrics and projections\"\n    instructions: \"Include revenue forecast, burn rate, and break-even point\"\n    max_tokens: 30",
         "author_name": "Alex Johnson",
         "author_email": "alex.johnson@example.com",
         "date": "2024-10-01"
     }' | jq -r '.response[0].message'
```

### Using all available fields and a notes file

```bash
curl --silent --location --request POST 'http://localhost:8080/system/powerpoint_editor/process/invoke' \
     --header 'Content-Type: multipart/form-data' \
     --header 'Integrations-API-Key: dev-only-token' \
     -F 'notes=@/path/to/your/meeting_notes.txt' \
     -F 'template=@/path/to/your/custom_template.pptx' \
     -F 'data={
         "author_name": "Emily Brown",
         "author_email": "emily.brown@example.com",
         "date": "2024-11-20",
         "context": "This presentation is for a quarterly board meeting. The company has recently expanded into Asian markets and launched two new product lines.",
         "llm_override": ["CONSULTING_ASSISTANTS", "Mixtral Large"],
         "config_data": "main_prompt: Generate detailed content for a quarterly board meeting presentation.\nreplacements:\n  - placeholder: \"{financial_highlights}\"\n    prompt: \"Summarize key financial metrics for the quarter\"\n    instructions: \"Include revenue growth, profit margins, and comparison to previous quarters\"\n    max_tokens: 100\n  - placeholder: \"{market_expansion}\"\n    prompt: \"Outline the progress of Asian market expansion\"\n    instructions: \"Highlight key achievements, challenges, and next steps\"\n    max_tokens: 75\n  - placeholder: \"{new_products}\"\n    prompt: \"Describe the performance of the two new product lines\"\n    instructions: \"Include sales figures, customer feedback, and future projections\"\n    max_tokens: 75"
     }'
```

### Processing multiple input files

```bash
curl --silent --location --request POST 'http://localhost:8080/system/powerpoint_editor/process/invoke' \
     --header 'Content-Type: multipart/form-data' \
     --header 'Integrations-API-Key: dev-only-token' \
     -F 'notes=@/path/to/your/project_notes.txt' \
     -F 'additional_notes=@/path/to/your/market_research.pdf' \
     -F 'template=@/path/to/your/project_template.pptx' \
     -F 'data={
         "author_name": "Team Project X",
         "author_email": "projectx@example.com",
         "date": "2025-01-15",
         "context": "This presentation combines project notes with recent market research for a comprehensive project overview.",
         "llm_override": ["CONSULTING_ASSISTANTS", "Mixtral Large"]
     }'
```

## Output

The endpoint returns a response containing the URL of the processed PowerPoint file and details of the replacements made. Here's an example of the output:

```json
{
    "status":"success",
    "invocationId":"550e8400-e29b-41d4-a716-446655440000",
    "response": [{
        "message":"PowerPoint Processing Complete\n\nThe PowerPoint presentation has been successfully processed based on the provided notes and configuration.\n\nProcessed PowerPoint URL: http://localhost:8080/public/powerpoint/550e8400-e29b-41d4-a716-446655440000.pptx\n\nReplacements Made:\n- Placeholder: {tda_summary}\n  Content: Client needs new CRM. Integration, mobile, analytics. 6 months, $500k budget.\n\n- Placeholder: {client_environment}\n  Content: Legacy CRM limits engagement opportunities\n\n...\n\nSummary:\n- Total placeholders processed: 15\n- Processing completed on: 2024-09-02\n- Author: John Doe (john.doe@example.com)\n\nThe processed PowerPoint incorporates the generated content for each placeholder. Please review the presentation to ensure it meets your requirements.",
        "type":"text"
    }]
}
```

## Dev Tools

This integration can be used with LangChain or similar frameworks. The main functionality is encapsulated in the `process_powerpoint` function, which can be adapted for use as a custom tool.

## Customization

1. Update the `process_powerpoint` function in `powerpoint_editor_route.py` to modify the processing logic or add additional features.
2. Update the Jinja2 templates in the `templates` directory to change the LLM prompts and response formatting.
3. Modify the `config.yaml` file to adjust the default placeholders, prompts, and instructions used for content generation.