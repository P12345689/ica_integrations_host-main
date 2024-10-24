# gs_researcher

> Author: wwwwen@cn.ibm.com

This module handles the routing for gs_researcher.

this integration is provided by GreenStar AI Automation tea. With this integration, you can generate more comprehensive reports to user's question.


## Backend Configuration

Integration with GS AGENT depends upon API and token.

|          Key          | Description                                       | Example Value | Default | Required  |
|:---------------------:|:--------------------------------------------------|:--------------------:|:-------:|:---------:|
|     GS_AGENT_API      | GS Agent service endpoint.                        | | | **Yes** |
| GS_AGENT_API_TOKEN | Token for GS Agent service endpoint .             | | | **Yes** |

contact: wwwwen@cn.ibm.com / yzhfyuan@cn.ibm.com to get the API and API token
## Invoke Inputs

The following invoke inputs are supported currently:


## Testing the integration locally

```bash
curl --location --request POST \
        'http://localhost:8080/gs_agents/researcher/invoke' \
        --header 'Content-Type: application/json' \
        --header 'Integrations-API-Key: dev-only-token' \
        --data-raw '{
            "prompt": "analyze nike's KPIs against top competitors"
            }'
```
