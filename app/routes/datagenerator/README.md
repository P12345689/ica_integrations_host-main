# Data Generator

> Author: Mihai Criveti

> Status: Disabled, need to add sdv dep to container first.

Synthetic Data Generator generates synthetic data based on sample input CSV files with optional data types JSON.

## Requirements

- sdv
- torch==2.2.0+cpu

You can test this manually with `pip install sdv`

## Endpoints

- **POST /datagenerator/invoke**
  Invokes the assistant reviewer process. It expects a JSON payload with a `num_rows`, `sample_csv` and `data_types`.

## Testing

### Specifying data types manually

```bash
curl --silent --request POST http://localhost:8080/datagenerator/invoke \
    --header "Content-Type: application/json" \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"num_rows": 20, "sample_csv":"name\nMihai", "data_types":"{ \"columns\": {\"name\":{\"sdtype\":\"first_name\",\"pii\": true}}}"}'
```

### Specify data types as a csv

```
curl --silent --request POST http://localhost:8080/datagenerator/invoke \
    --header "Content-Type: application/json" \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"num_rows": 20, "sample_csv":"name,mail\nMihai,mihai@example.com", "data_types":"first_name,email"}'
```


### Autodetect
```
curl --silent --request POST http://localhost:8080/datagenerator/invoke \
    --header "Content-Type: application/json" \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"num_rows": 20, "sample_csv":"name\nMihai"}'
```
