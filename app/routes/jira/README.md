# Jira Integration

> Author: Mihai Criveti

This is the Jira integration, which provides services for creating Jira issues, searching for issues, retrieving issue information, exporting issues as CSV, and answering questions about Jira.

## TODO

Currently, only the following fields are supported on creation: assignee, description, project, issuetype, summary. To add support for all fields on creation / edit (attachment, comment, duedate, issuelinks, priority, reporter, resolution, security, status, statuscategorychangedate, timetracking, versions, votes, watchers, worklog).

## Environment Variables

Before using this integration, you need to set up the following environment variables:

- `JIRA_URL`: The URL of your Jira instance (e.g., "https://jsw.ibm.com")
- `JIRA_USERNAME`: Your Jira username (usually your email address)
- `JIRA_API_TOKEN`: Your Jira API token (NOT your password)

You can set these environment variables in a `.env` file in the root directory of the project, or export them in your shell before running the application.

Example `.env` file:

```
JIRA_URL=https://jsw.ibm.com
JIRA_USERNAME=your.email@example.com
JIRA_API_TOKEN=your_api_token_here
```

## Endpoints

- POST /system/jira/retrievers/create_issue/invoke
  Invokes the System API to create a new Jira issue.

- POST /system/jira/retrievers/search_issues/invoke
  Invokes the System API to search for Jira issues using various criteria.

- POST /system/jira/retrievers/export_issues_csv/invoke
  Invokes the System API to export Jira issues as a CSV file.

- POST /system/jira/retrievers/get_issue/invoke
  Invokes the System API to retrieve information about a specific Jira issue.

- POST /experience/jira/ask_jira/invoke
  Invokes the Experience API to answer a question based on a Jira-related query.

## Testing the integration locally

Before running these examples, make sure you have set the environment variables as described above.

### Create Jira Issue

```bash
curl --location --request POST \
    'http://localhost:8080/system/jira/retrievers/create_issue/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "project_key": "PROJ",
        "summary": "Test issue from integration",
        "description": "This is a test issue created using the Jira integration",
        "issue_type": "Task",
        "assignee": "john.doe@example.com",
    }'
```

You can override the auth like this:

```json
curl --location --request POST \
    'http://localhost:8080/system/jira/retrievers/create_issue/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "project_key": "PROJ",
        "summary": "Test issue from integration",
        "description": "This is a test issue created using the Jira integration",
        "issue_type": "Task",
        "assignee": "john.doe@example.com",
        "auth": {
          "jira_url": "{{JIRA_URL}}",
          "jira_username": "{{JIRA_USERNAME}}",
          "jira_api_token": "{{JIRA_API_TOKEN}}"
        }
    }'    
```

### Search Jira Issues

```bash
curl --location --request POST \
    'http://localhost:8080/system/jira/retrievers/search_issues/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "project_key": "PROJ",
        "assignee": "john.doe@example.com",
        "status": "Open",
        "max_results": 10
    }'
```

### Export Jira Issues as CSV

```bash
curl --location --request POST \
    'http://localhost:8080/system/jira/retrievers/export_issues_csv/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "project_key": "PROJ",
        "assignee": "john.doe@example.com",
        "status": "Open",
        "max_results": 100
    }' \
    --output jira_issues.csv
```

### Get Jira Issue

```bash
curl --location --request POST \
    'http://localhost:8080/system/jira/retrievers/get_issue/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "issue_key": "PROJ-123"
    }'
```

### Ask Jira

```bash
curl --location --request POST \
    'http://localhost:8080/experience/jira/ask_jira/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
        "query": "What are the open issues assigned to John Doe in the PROJ project?"
    }'
```

## Troubleshooting

If you encounter authentication errors, double-check that your environment variables are set correctly:

```bash
echo $JIRA_URL
echo $JIRA_USERNAME
echo $JIRA_API_TOKEN
```

Make sure the `JIRA_API_TOKEN` is not your Jira password, but the API token you generated from the Atlassian account management page.

If you're still having issues, ensure that:
1. Your Jira instance is accessible from your current network.
2. Your Jira account has the necessary permissions to perform the actions you're attempting.
3. The project key you're using in your requests actually exists in your Jira instance.

For any other issues, check the application logs for more detailed error messages.
