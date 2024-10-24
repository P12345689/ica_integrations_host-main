# Chart Generation Integration

This integration provides functionality for creating various types of charts using matplotlib.


## Usage

To use this integration, follow these steps:

1. Ensure you have the required dependencies installed, including matplotlib.
2. Set up the necessary environment variables (e.g., `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME`, `DEFAULT_MAX_THREADS`).
3. Include this module in your FastAPI application.

## API Endpoints

### POST /system/chart/generate_chart/invoke

Generates a chart from provided data and returns it as a PNG file.

```bash
curl --location --request POST 'http://localhost:8080/system/chart/generate_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "chart_type": "bar",
         "data": {
             "x": ["A", "B", "C", "D"],
             "y": [1, 4, 2, 3]
         },
         "title": "Sample Bar Chart"
     }'
```

### POST /system/chart/generate_csv_chart/invoke

Generates a chart from provided csv data and returns it as a PNG file.

```bash
curl --location --request POST 'http://localhost:8080/system/chart/generate_csv_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "chart_type": "bar",
         "csv_data": "X,Y\nA,1\nB,4\nC,2",
         "sheet_name": "Employee Data",
         "title": "Sample Bar Chart CSV"
     }'
```

### POST /experience/chart/generate_chart/invoke

Generates a chart based on a natural language description, using an LLM to interpret the request.

```bash
curl --location --request POST 'http://localhost:8080/experience/chart/generate_chart/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Create a pie chart showing the distribution of fruits: 30% apples, 25% bananas, 20% oranges, and 25% grapes"
     }'
```

Both endpoints return a response containing the URL of the generated PNG file and the data used to generate the chart.

# Generates Histogram

bash
curl --location --request POST 'http://localhost:8080/system/chart/generate_chart/invoke' \
--header 'Content-Type: application/json' \
--header 'Integrations-API-Key: dev-only-token' \
--data-raw '{"chart_type": "histogram","data": {"values": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]},"title": "Sample Histogram","x_label": "Values","y_label": "Frequency"}'

# Generates Pie Chart

bash
curl --location --request POST 'http://localhost:8080/system/chart/generate_chart/invoke' \
--header 'Content-Type: application/json' \
--header 'Integrations-API-Key: dev-only-token' \
--data-raw '{"chart_type": "pie","data": {"values": [1, 4, 2, 3],"labels": ["A", "B", "C", "D"]},"title": "Sample Pie Chart"}'

# Generates Bar chart

bash
curl --location --request POST 'http://localhost:8080/system/chart/generate_chart/invoke' \
--header 'Content-Type: application/json' \
--header 'Integrations-API-Key: dev-only-token' \
--data-raw '{"chart_type": "bar","data": {"x": ["A", "B", "C", "D"],"y": [1, 4, 2, 3]},"title": "Sample Bar Chart", "x_label": "testx", "y_label": "testy"}'

# Generates Line chart

bash
curl --location --request POST 'http://localhost:8080/system/chart/generate_chart/invoke' \
--header 'Content-Type: application/json' \
--header 'Integrations-API-Key: dev-only-token' \
--data-raw '{"chart_type": "line","data": {"x": ["A", "B", "C", "D"],"y": [1, 4, 2, 3]},"title": "Sample Line Chart", "x_label": "testx", "y_label": "testy"}'

