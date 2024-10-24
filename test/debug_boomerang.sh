#!/bin/bash
# Author: Mihai Criveti
# Description: test endpoints in dev

# Set the base URL
export BASE_URL="https://ocp2.cloud.boomerangplatform.net/dev/integrations/services/integrations-host/"  # DEV
export DEFAULT_ROUTE="plantuml/invoke"
export DEFAULT_JSON_FILE="routes/plantuml.json"

# Check if BMRG_COOKIE is set in the environment, if not, exit and show help
if [ -z "$BMRG_COOKIE" ]; then
    echo "Error: BMRG_COOKIE is not set."
    echo "Please set the BMRG_COOKIE environment variable and try again."
    exit 1
fi

# Validate arguments
if [ "$#" -gt 2 ]; then
    echo "Error: Too many arguments provided."
    echo "Usage: $0 [route] [json_file]"
    exit 1
elif [ "$#" -eq 0 ]; then
    # Set defaults if no arguments are provided
    ROUTE="${DEFAULT_ROUTE}"
    JSON_FILE="${DEFAULT_JSON_FILE}"
    echo "Using default route and JSON file."
elif [ "$#" -eq 1 ]; then
    echo "Error: Missing JSON file argument."
    echo "Usage: $0 [route] [json_file]"
    exit 1
else
    ROUTE="$1"
    JSON_FILE="$2"
fi

# Construct the full URL using the provided or default route
ROUTE_URL="${BASE_URL}/${ROUTE}"

# cURL command to send the JSON file to the server
curl -v \
  --location "${ROUTE_URL}" \
  --header "Cookie: bmrg_dev_auth_proxy=${BMRG_COOKIE}" \
  --header 'Content-Type: application/json' \
  --data @"${JSON_FILE}" \
  | jq

# Note: Ensure 'jq' is installed on your system for processing JSON data
