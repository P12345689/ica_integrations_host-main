# Intelligent Prompt Router Integration

> Author: Mihai Criveti

This integration provides services for routing prompts to the best model, assistant, or document collection based on a configuration file and cosine similarity matching.

## Endpoints

- POST /experience/prompt_router/route_prompt/invoke
  Invokes the Experience API to route a prompt to the best option and return the response.

- POST /system/prompt_router/get_configuration/invoke
  Invokes the System API to retrieve the current prompt router configuration.

## Testing the integration locally

### Route Prompt - Experience API

This endpoint routes a prompt to the best option based on the configuration and cosine similarity.

#### Example 1: General Knowledge Query

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt_router/route_prompt/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "prompt": "What are the top insights on IBM?",
        "context": {}
    }'
```

This general knowledge query is likely to be routed to a powerful, general-purpose model like Llama3.1 70b Instruct or GPT-4.

#### Example 2: Code Generation

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt_router/route_prompt/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "prompt": "Generate a Java class for a simple banking application with methods for deposit and withdrawal",
        "context": {}
    }'
```

This code-related prompt is likely to be routed to the Granite 34B Code Instruct V2 model or the Generate Java Code assistant.

#### Example 3: Multilingual Task

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt_router/route_prompt/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "prompt": "Translate the following English text to Spanish and French: The quick brown fox jumps over the lazy dog.",
        "context": {}
    }'
```

This multilingual task is likely to be routed to the Granite 20b Multilingual model or the Mixtral Large model.

#### Example 4: Long Context Analysis

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt_router/route_prompt/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "prompt": "Analyze the following long research paper on quantum computing and summarize the key findings in bullet points. [Insert long research paper text here]",
        "context": {}
    }'
```

This task involving a long context is likely to be routed to models with large context windows like OpenAI GPT4 32K or Claude 2 (100K).

#### Example 5: IBM Financial Information

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt_router/route_prompt/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "prompt": "What were IBM's total revenues for the last fiscal year according to their most recent Form 10-K?",
        "context": {}
    }'
```

This query about IBM's financial information is likely to be routed to the IBM Form 10k document collection.

#### Example 6: Dialogue-Oriented Task

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt_router/route_prompt/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "prompt": "You are a customer service chatbot. Engage in a conversation with a customer who is having trouble with their internet connection.",
        "context": {}
    }'
```

This dialogue-oriented task is likely to be routed to the Granite 13B V2.1 model, which is optimized for dialogue use cases.

#### Example 7: Using Context to Influence Routing

```bash
curl --location --request POST \
    'http://localhost:8080/experience/prompt_router/route_prompt/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "prompt": "Explain the concept of object-oriented programming",
        "context": {
            "preferred_type": "model",
            "preferred_language": "Python"
        }
    }'
```

This example shows how additional context can influence the routing. The preferred type "model" might steer it towards a general-purpose model, while the Python preference might favor a code-oriented model like Granite 34B Code Instruct V2.

### Get Configuration - System API

This endpoint retrieves the current prompt router configuration.

```bash
curl --location --request POST \
    'http://localhost:8080/system/prompt_router/get_configuration/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token'
```

## Configuration

The prompt router uses a configuration file located at `app/routes/model_router/config/prompt_router_config.json`. This file contains the available options for routing, including models, assistants, and document collections.

## Customization

To add new models, assistants, or document collections, update the `prompt_router_config.json` file with the new options, including their descriptions. The router will automatically consider these new options when matching prompts.

## Dependencies

This integration requires the following Python packages:

- fastapi
- pydantic
- jinja2
- scikit-learn
- numpy

Install them using:

```bash
pip install fastapi pydantic jinja2 scikit-learn numpy
```

## Note

The current implementation uses cosine similarity for matching prompts to the best option. The routing for assistants and document collections is not yet fully implemented and may return placeholder messages. Implement these routings in the `route_prompt` function when ready.

## Debugging

If you're not getting the expected routing results, you can:

1. Check the logs for detailed ranking information.
2. Adjust the descriptions in the configuration file to better match the intended use cases.
3. Modify the `rank_options` function in `prompt_router.py` to fine-tune the ranking algorithm.

## Performance Considerations

The cosine similarity calculation can become computationally expensive with a large number of options. If you experience performance issues with many options, consider:

1. Implementing a pre-filtering step based on option types or categories.
2. Using more efficient similarity calculation methods for large-scale comparisons.
3. Caching frequently used similarity results.

## Feedback and Improvement

The effectiveness of the routing can be improved over time by:

1. Analyzing logs to understand common routing patterns.
2. Gathering user feedback on the appropriateness of selected options.
3. Periodically reviewing and updating the descriptions and configuration based on actual usage patterns.

Remember that the goal is to route prompts to the most appropriate option, which may not always be the most powerful or newest model. The context of the task, efficiency, and specific capabilities of each option should all be considered in the routing decision.
