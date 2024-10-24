# Configurable CrewAI agent

> Author: Adrian Popa

This module implements a CrewAI Agent. The agent will be configured based on a JSON file received as input or read from a prompt.

## Agent parameters

-   `query`: A string containing the user's question or query.
-   `context`: An array of objects containing additional information related to the query.
-   `use_context`: A boolean indicating whether to use the context information.
-   `llm_override`: ["MODEL_TYPE", "MODEL_NAME"]. An array where MODEL_TYPE a type of model and MODEL_NAME a specific model name. See app.routes.agent_langchain.config for a list of supported model types.
-   `stream`: A boolean indicating whether to stream the output.

## **CrewAI Configuration**

Is given in crewai_config parameter as a JSON.

The main sections of the JSON

### Agent

-   `role`: The role of the agent, such as "Researcher" or "Writer".
-   `goal`: A brief description of the goal of the agent, such as "Uncover the real meaning of information based on the user intent".
-   `backstory`: A longer description of the agent's background and expertise, such as "You are a Senior Research Analyst...".
-   'tools': An array with the list of tools ids available to integrations. Must be a tool deployed in container locally.

### Task

-   `description`: A brief description of the task, including any specific requirements or constraints.
-   `expected_output`: An indication of what output is expected from the agent after completing the task.
-   `agent`: Indicates the agent role that is responsible for the task.


Please consult the samples directory for some integrations samples  

## Testing the integration locally

Create a config JSON file named config.json with the following content. This file contain the agent definition

```json
{
     "query": "Why IBM is an excellent proposal in Consumer Industries. Include IBM strengths compared with competitors and find IBM references. All the strengths must apply to Consumer Industries. Also references must be applicable in consumer industry",
     "context": "[{\"content\":\"What is OpenShift\",\"type\":\"PROMPT\"},{\"content\":\"OpenShift is a containerization and orchestration platform for deploying and managing applications using Kubernetes. It provides a simple and efficient way to manage containers and application services, enabling developers to focus on building their applications instead of managing the underlying infrastructure.\",\"type\":\"ANSWER\"}]",
     "use_context": "True",
     "stream": "True",
     "llm_override": ["AZURE_OPENAI", "scribeflowgpt4o"],
     "crewai_config": {
         "agents": [
             {
                 "role": "Researcher",
                 "goal": "Uncover the real meaning of information based on the user intent",
                 "backstory": "You are a Senior Research Analyst. Your expertise lies in identifying significant facts and trends. You have a knack for dissecting complex data and presenting actionable insights.",
                 "verbose": true,
                 "allow_delegation": false,
                 "tools": ["retrieve_website_content","google_search"],
                 "max_rpm": 60,
                 "max_iter": 40,
                 "max_execution_time": 4200
             },
             {
                 "role": "Writer",
                 "goal": "Craft engaging client document based on research findings",
                 "backstory": "You are a skilled writer specializing in technology topics. Your goal is to present complex information in an accessible and captivating manner.",
                 "verbose": true,
                 "allow_delegation": false,
                 "tools": [],
                 "max_rpm": 30,
                 "max_iter": 20,
                 "max_execution_time": 3600
             }
         ],
         "tasks": [
             {
                 "description": "Conduct a comprehensive analysis on {query}. If search collections tools is available use it to identify available collections and  extract the most appropriate document. Use the query document tool to query for facts that are useful about the task . If an internet search tool is available use it to find up-to-date information and new trends. Identify main facts. Compile your findings in a detailed report. Make sure to check with a human if the draft is good before finalizing your answer.",
                 "expected_output": "A summary document  about {query}",
                 "agent": "Researcher"
             },
             {
                 "description": "Using the insights from the researcher's report, develop an engaging document about {query}. Your document  should be informative yet accessible, catering to a tech-savvy audience. Aim for a narrative that captures relevant information but also signals trends and breakthroughs and their implications for the future.",
                 "expected_output": "A compelling 3 paragraphs document formatted in Markdown about {query}",
                 "agent": "Writer"
             }
         ]
     }
}
```

```bash
curl --location --request POST 'http://localhost:8080/agent_crewai/crewai' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key:dev-only-token' \
    --data @config.json
```


