# Plotly Chart Generation Integration

This integration provides functionality for creating various types of interactive charts using Plotly.

## Requirements

To use this integration, follow these steps:

1. Ensure you have the required dependencies installed. Update `requirements.txt` to include `plotly`.
2. Set up the (optional) environment variables: `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME`, `DEFAULT_MAX_THREADS` or `SERVER_NAME`.
3. Include this module in your FastAPI application.

## Endpoints

- **POST /system/plotly/generate_chart/invoke**
    Generates an interactive chart from provided data and returns it as an HTML file.

- **POST /experience/plotly/generate_chart/invoke**
    Generates an interactive chart based on a natural language description, using an LLM to interpret the request.

## Testing the integration locally

Available `chart_type` tags: `bar`, `pie`, `line`, `scatter`, `histogram`.

### Generating plot from provided data

```bash
curl --location --request POST 'http://localhost:8080/system/plotly/generate_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "chart_type": "bar",
         "data": {
             "x": ["A", "B", "C", "D"],
             "y": [1, 4, 2, 3]
         },
         "title": "Sample Bar Chart",
         "format": "HTML"
     }'
```

```bash
curl --location --request POST 'http://localhost:8080/system/plotly/generate_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "chart_type": "bar",
         "data": {
             "x": ["A", "B", "C", "D"],
             "y": [1, 4, 2, 3]
         },
         "title": "Sample Bar Chart",
         "format": "PNG"
     }'
```

### Generating histograms with provided data

Two inputs are accepted for generating a histogram:

1. Data in "x" is used as is, if "y" is empty.
```
"data": {
     "x": ["A", "A", "A", "B", "C", "C", "D"],
     "y": []
 },
```

2. Data in "x" is expanded based on frequencies in "y". Any duplicates in "x" are removed automatically.
```
"data": {
     "x": ["A", "B", "C", "D"],
     "y": [1, 4, 2, 3]
 },
```

### Histogram curl command examples

```bash
curl --location --request POST 'http://localhost:8080/system/plotly/generate_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "chart_type": "histogram",
         "data": {
             "x": ["A", "B", "C", "D"],
             "y": [1, 4, 2, 3]
         },
         "title": "Sample Histogram",
         "format": "HTML"
     }'
```

```bash
curl --location --request POST 'http://localhost:8080/system/plotly/generate_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "chart_type": "histogram",
         "data": {
             "x": ["A", "A", "A", "B", "B", "C", "D", "D"],
             "y": []
         },
         "title": "Sample Histogram",
         "format": "HTML"
     }'
```

### Generating plot using natural language

```bash
curl --location --request POST 'http://localhost:8080/experience/plotly/generate_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Create a pie chart showing the distribution of fruits: 30% apples, 25% bananas, 20% oranges, and 25% grapes",
         "format": "PNG"
     }'
```

```bash
curl --location --request POST 'http://localhost:8080/experience/plotly/generate_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Create a pie chart showing the distribution of fruits: 30% apples, 25% bananas, 20% oranges, and 25% grapes",
         "format": "HTML"
     }'
```

## Output

Both endpoints return a response containing the URL of the generated HTML/PNG file (containing the interactive Plotly chart) and the data used to generate the chart.


```json
{
    "status":"success",
    "invocationId":"b6862338-ee2f-4b3f-9449-95d1589f7679",
    "response": [{
        "message":"http://127.0.0.1:8080/public/plotly/chart_7a17d9ca-008d-479d-9ead-647ccdd2dea1.html, Chart data:\n\n```\n{\"chart_type\":\"bar\",\"data\":{\"x\":[\"A\",\"B\",\"C\",\"D\"],\"y\":[1,4,2,3]},\"title\":\"Sample Bar Chart\",\"format\":\"HTML\"}\n```",
        "type":"text"
    }]
}
```

## Dev Tools

This integration provides the following tools that can be used with LangChain or similar frameworks:

- `create_plotly_chart`: Generates a Plotly chart from provided data.
- `get_plotly_info`: Provides information about the Plotly integration.
- `plotly_chart_type_helper`: Offers information about different Plotly chart types and their data requirements.


These tools can be imported and used as follows:

```python
from langchain.agents import load_tools
from .tools.plotly_tool import create_plotly_chart, get_plotly_info, plotly_chart_type_helper

tools = load_tools(["create_plotly_chart", "get_plotly_info", "plotly_chart_type_helper"])
```

## Customization

1. Update the `generate_chart` function in `plotly_router.py` to support additional chart types or customize existing ones.
2. Update the Jinja2 templates in the `templates` directory to change the LLM prompts and response formatting.
