#!/bin/bash

# Read the CV and job description files
CV_CONTENT=$(cat sample_cv.txt)
JOB_DESCRIPTION=$(cat job_description.txt)

# Escape the content for JSON
CV_CONTENT_ESCAPED=$(echo "$CV_CONTENT" | jq -sR .)
JOB_DESCRIPTION_ESCAPED=$(echo "$JOB_DESCRIPTION" | jq -sR .)

# Create the JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "document1": $CV_CONTENT_ESCAPED,
  "document2": $JOB_DESCRIPTION_ESCAPED,
  "instruction": "Compare this CV to the job description and assess the candidate's fit for the position. Highlight matching skills and experience, and identify any gaps. Provide a recommendation on whether to proceed with the candidate.",
  "output_format": "markdown"
}
EOF
)

# Send the request to the API
curl --location --request POST \
  'http://localhost:8080/experience/compare/compare_documents/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data "$JSON_PAYLOAD"
