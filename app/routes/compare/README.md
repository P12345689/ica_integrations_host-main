# Document Comparison Integration

> Author: Mihai Criveti

This integration provides a service for comparing two documents. It supports various comparison use cases based on the provided instruction.

## Features

- Flexible document comparison based on user-provided instructions
- Support for multiple LLM types (ChatConsultingAssistants, OpenAI, Ollama)
- Configurable output format (plain text or Markdown)
- Adjustable LLM parameters (context length and temperature)
- Ability to compare file contents

## Endpoint

- POST /experience/compare/compare_documents/invoke
  Invokes the Experience API to compare two documents based on the given instruction.

## Usage Examples

### Basic Document Comparison

```bash
curl --location --request POST \
    'http://localhost:8080/experience/compare/compare_documents/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "document1": "This is the content of the first document...",
        "document2": "This is the content of the second document...",
        "instruction": "Compare these documents and identify key differences",
        "output_format": "markdown"
    }'
```

### Comparing Two Versions of a CV

This example demonstrates how to compare two versions of a CV stored in separate files.

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/compare/compare_documents/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data "$(jq -n \
        --arg cv1 "$(cat cv_version1.txt)" \
        --arg cv2 "$(cat cv_version2.txt)" \
        '{
            document1: $cv1,
            document2: $cv2,
            instruction: "Compare these two versions of the CV. Identify any changes or updates made, such as new skills, experiences, or qualifications added. Highlight any information that was removed or modified.",
            output_format: "markdown"
        }')" | jq -r '.response[0].message'
```

### Comparing a CV to a Job Description

This example shows how to compare a CV to a job description, both stored in files.

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/compare/compare_documents/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data "$(jq -n \
        --arg cv "$(cat sample_cv.txt)" \
        --arg job "$(cat job_description.txt)" \
        '{
            document1: $cv,
            document2: $job,
            instruction: "Compare this CV to the job description and assess the candidates fit for the position. Highlight matching skills and experience, and identify any gaps. Provide a recommendation on whether to proceed with the candidate.",
            output_format: "markdown"
        }')" | jq -r '.response[0].message'
```

### Identify missing skills from a CV compared to a JD

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/compare/compare_documents/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data "$(jq -n \
        --arg cv "$(cat sample_cv.txt)" \
        --arg jd "$(cat job_description.txt)" \
        '{
            document1: $cv,
            document2: $jd,
            instruction: "Compare this CV to the job description. Identify matching skills and experiences. List skills and qualifications mentioned in the job description that are missing from the CV. Provide a bullet-point list of skills the candidate should add to their CV to better match the job requirements.",
            output_format: "markdown"
        }')" | jq -r '.response[0].message'
```

### Scoring a CV against a Job Description

This example demonstrates how to use the summarization endpoint to score a CV against a Job Description, providing matches by various areas and a total match score.

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/compare/compare_documents/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data "$(jq -n \
        --arg cv "$(cat sample_cv.txt)" \
        --arg jd "$(cat job_description.txt)" \
        '{
            document1: $cv,
            document2: $jd,
            instruction: "Compare this CV to the job description and provide a detailed assessment. Score the following areas out of 100: Skills Match, Experience Match, Education Match, and Overall Fit. Also calculate a Total Match Score out of 100. For each area, briefly explain the reasoning behind the score. Finally, provide a short recommendation on whether to proceed with the candidate. Format the output in Markdown.",
            output_format: "markdown"
        }')" | jq -r '.response[0].message'
```


### Comparing Legal Documents

```bash
curl --silent --location --request POST \
    'http://localhost:8080/experience/compare/compare_documents/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data "$(jq -n \
        --arg doc1 "$(cat legal_document1.txt)" \
        --arg doc2 "$(cat legal_document2.txt)" \
        '{
            document1: $doc1,
            document2: $doc2,
            instruction: "Compare these legal documents and identify any significant differences in terms, conditions, or clauses. Highlight any added, removed, or modified sections.",
            output_format: "markdown"
        }')" | jq -r '.response[0].message'
```

### Comparing Two Text Chunks

```bash
curl --location --request POST \
    'http://localhost:8080/experience/compare/compare_documents/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "document1": "First chunk of text...",
        "document2": "Second chunk of text...",
        "instruction": "Compare these two text chunks and provide a summary of the main differences in content and style",
        "output_format": "plain"
    }'
```

## Notes

- The `output_format` can be set to "markdown" or "plain" depending on your preference for the response format.
- The `jq` command is used in the file-based examples to properly escape the file contents for JSON. Make sure `jq` is installed on your system.

## File Preparation

For the file-based comparison examples, prepare your files as follows:

1. `cv_version1.txt` and `cv_version2.txt`: Two versions of a CV
2. `sample_cv.txt`: A sample CV
3. `job_description.txt`: A job description
4. `legal_document1.txt` and `legal_document2.txt`: Two legal documents to compare

Ensure these files are in the same directory as your curl command or provide the full path to the files.
