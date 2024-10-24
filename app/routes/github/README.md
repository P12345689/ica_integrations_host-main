# GitHub Integration

> Author: Mihai Criveti

This integration provides functionality for interacting with GitHub repositories, including both public and Enterprise private repos. It now includes features for cloning repositories and performing git fame analysis.

## TODO

1. Conversational history (parse context)
2. Failover if it cant' get repo etc. to print out a nice message


## Usage

To use this integration, follow these steps:

1. Ensure you have the required dependencies installed. Update `requirements.txt` to include:
   ```
   fastapi
   pydantic
   jinja2
   PyGithub
   gitfame
   ```
2. Set up the necessary environment variables (e.g., `DEFAULT_MAX_THREADS`).
3. Include this module in your FastAPI application.

## API Endpoints

### POST /system/github/invoke

Performs various GitHub operations based on the provided action.

#### Supported actions:

- `list_issues`
- `get_issue`
- `create_issue`
- `list_prs`
- `get_pr`
- `create_pr`
- `list_releases`
- `create_release`
- `get_file`

Each action may require different parameters in the params field. Refer to the `github_action_helper` tool for more information on required parameters for each action.

#### Example: List Issues

```bash
export GITHUB_TOKEN=$(gh auth token)

curl --location --request POST 'http://localhost:8080/system/github/invoke' \
  --header 'Content-Type: application/json' \
  --header "Integrations-API-Key: dev-only-token" \
  --data-raw '{
      "repo_url": "https://github.ibm.com/destiny/ica_integrations_host",
      "action": "list_issues",
      "params": {},
      "github_token": "'"${GITHUB_TOKEN}"'"
  }'
```

### POST /experience/github/invoke

This endpoint uses an LLM to interpret natural language queries about GitHub operations and perform the appropriate action.

```bash
curl --location --request POST 'http://localhost:8080/experience/github/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "repo_url": "https://github.ibm.com/destiny/ica_integrations_host",
         "query": "List all open issues in the repository",
         "github_token": "'"${GITHUB_TOKEN}"'"
     }'
```

The LLM can also extract the repo_url from the query:

```bash
curl --location --request POST 'http://localhost:8080/experience/github/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "query": "List all open issues in the repository: https://github.ibm.com/destiny/ica_integrations_host",
         "github_token": "'"${GITHUB_TOKEN}"'"
     }'
```


### NEW: POST /system/github/clone/invoke

This endpoint clones a GitHub repository or updates it if it already exists.

```bash
curl --location --request POST 'http://localhost:8080/system/github/clone/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "repo_url": "https://github.ibm.com/destiny/ica_integrations_host",
         "depth": 0,
         "github_token": "'"${GITHUB_TOKEN}"'"
     }'
```

- `depth`: Optional. Specifies the depth of the clone. Default is 0 for a full clone.

### NEW: POST /system/github/git-fame/invoke

This endpoint runs git fame analysis on a cloned GitHub repository.

```bash
curl --location --request POST 'http://localhost:8080/system/github/git-fame/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "repo_url": "https://github.ibm.com/destiny/ica_integrations_host",
         "exclusions": ["*.md", "models--*"],
         "github_token": "'"${GITHUB_TOKEN}"'"
     }'
```

- `exclusions`: Optional. List of### NEW: POST /system/github/analyze/invoke

This endpoint runs multiple analysis tools on a cloned GitHub repository.

```bash
curl --location --request POST 'http://localhost:8080/system/github/analyze/invoke' \
     --header 'Content-Type: application/json' \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
         "repo_url": "https://github.ibm.com/destiny/ica_integrations_host",
         "analysis_tools": ["fame", "pylint", "scc", "pyreverse"],
         "target_path": ".",
         "exclusions": ["*.md"],
         "github_token": "'"${GITHUB_TOKEN}"'"
     }'
```

- `analysis_tools`: List of analysis tools to run. Supported tools are "fame", "pylint", "scc", and "pyreverse".
- `target_path`: Optional. Specifies the target path or module to analyze within the repository. Default is "app".
- `exclusions`: Optional. List of patterns to exclude from the analysis.

This new endpoint allows for running multiple analysis tools in a single request. It provides a more flexible and comprehensive analysis of the repository compared to the individual git-fame endpoint.
 patterns to exclude from the analysis.


## Tool Example:

sh
curl --location --request POST 'http://localhost:8080/agent_langchain/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
    "query": "{"repo": "https://github.ibm.com/sankris6/demystifier-agents-dev", "action": "get_file", "params": {"path": "utilities/RouteController.py"}, "token": "<yourtoken>"}", "tools": ["github_action"]
}'


## Notes

- Replace `your_github_token_here` with your actual GitHub personal access token.
- For GitHub Enterprise, use the full URL to your GitHub Enterprise instance, e.g., https://github.ibm.com/your-org/your-repo.
- The `github_token` is optional for public repositories but required for private repositories or any operations that require authentication.
- Cloned repositories are stored in the `public/github/` directory.
- Git fame analysis is performed on the cloned repositories. If a repository hasn't been cloned yet, it will be cloned automatically before running the analysis.
- The new analyze endpoint supports multiple analysis tools: git fame, pylint, scc, and pyreverse.
- For git fame analysis, the exclusion "--excl=models/models--*" is always applied in addition to any user-specified exclusions to avoid analyzing LLM binaries.
- The pyreverse tool generates UML diagrams in PNG format, which are saved in a 'pyreverse_output' directory within the cloned repository.

## Tools

This integration provides the following tools that can be used with LangChain or similar frameworks:

- `github_action`: Performs various GitHub operations.
- `get_github_info`: Provides information about the GitHub integration.
- `github_action_helper`: Offers information about different GitHub actions and their required parameters.

These tools can be imported and used as follows:

```python
from langchain.agents import load_tools
from .tools.github_tool import github_action, get_github_info, github_action_helper

tools = load_tools(["github_action", "get_github_info", "github_action_helper"])
```

## Error Handling

- If a repository clone fails, an appropriate error message will be returned.
- If git fame analysis fails (e.g., due to an non-existent repository), an error message will be provided.
- Invalid inputs or missing required parameters will result in appropriate error responses.
- If an unsupported analysis tool is specified, an error message will be returned for that specific tool, while other valid tools will still be executed.
- Results from each analysis tool are provided separately in the response, allowing for partial results even if one tool fails.

For any issues or feature requests, please contact the integration maintainer: Mihai Criveti.