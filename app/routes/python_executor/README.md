# Python Code Executor

> Author: Mihai Criveti
> Status: Development, needs further testing

Python Code Executor is a secure service that executes Python code with various safety measures in place.
It also provides a feature to generate and execute Python code based on user queries using an AI language model.

## Features

- Secure execution of Python code in a restricted environment using RestrictedPython
- Code generation based on natural language queries
- Input sanitization to prevent injection attacks
- Code sanitization to prevent the use of unsafe functions and modules
- Execution with configurable timeout and memory limits
- Comprehensive error handling and logging
- Consistent response format for both successful executions and errors
- Uses AST to block 1. Imports of specific modules 2. Calls to specific built-in functions 3. Use of certain attributes that could lead to unsafe operations

## Limitations

- Currently prevents generating or executing any kind of functions in code.

## Requirements

- Python 3.7+
- FastAPI
- Pydantic
- Jinja2
- libica (for LLM integration)
- RestrictedPython

## Environment Variables

Set the following environment variables to configure the service:

- `PYTHON_EXECUTOR_DEFAULT_TIMEOUT`: Default timeout for code execution in seconds (default: 5)
- `PYTHON_EXECUTOR_DEFAULT_MAX_MEMORY`: Default maximum memory usage in MB (default: 100)
- `PYTHON_EXECUTOR_MAX_TIMEOUT`: Maximum allowed timeout in seconds (default: 30)
- `PYTHON_EXECUTOR_MAX_MEMORY`: Maximum allowed memory usage in MB (default: 500)
- `ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME`: The default AI model to use for code generation (default: "Llama3.1 70b Instruct")
- `PYTHON_EXECUTOR_MAX_INPUT_LENGTH`: Maximum length of user input in characters (default: 1000)

## Endpoints

1. **POST /system/python_executor/execute_code/invoke**
   Executes the provided Python code securely.

2. **POST /experience/python_executor/generate_and_execute/invoke**
   Generates Python code based on a natural language query and executes it securely.

## Usage Examples

### 1. Executing Python Code

To execute Python code directly, send a POST request to the `/system/python_executor/execute_code/invoke` endpoint.

```bash
curl --location --request POST 'http://localhost:8080/system/python_executor/execute_code/invoke' \
     --header "Content-Type: application/json" \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "code": "def custom_sum(numbers):\n    return sum(numbers)\nnumbers = [1, 2, 3, 4, 5]\nresult = custom_sum(numbers)\nprint(result)"
     }'
```

Expected response:
```json
{
    "status": "success",
    "invocationId": "123e4567-e89b-12d3-a456-426614174000",
    "response": [
        {
            "message": "The Python code executed was:\n\nnumbers = [1, 2, 3, 4, 5]\nresult = sum(numbers)\n\nThe result of the execution is:\n\n15",
            "type": "text"
        }
    ]
}
```

### 2. Generating and Executing Code

To generate and execute Python code based on a natural language query, send a POST request to the `/experience/python_executor/generate_and_execute/invoke` endpoint.

```bash
curl --location --request POST 'http://localhost:8080/experience/python_executor/generate_and_execute/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Calculate the factorial of 5"
     }'
```

Expected response:
```json
{
    "status": "success",
    "invocationId": "123e4567-e89b-12d3-a456-426614174001",
    "response": [
        {
            "message": "The Python code executed was:\n\ndef factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n-1)\n\nresult = factorial(5)\n\nThe result of the execution is:\n\n120",
            "type": "text"
        }
    ]
}
```

### 3. Calculating Fibonacci Numbers

```bash
curl --location --request POST 'http://localhost:8080/system/python_executor/execute_code/invoke' \
     --header "Content-Type: application/json" \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "code": "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\nresult = [fibonacci(i) for i in range(10)]"
     }'
```

Expected response:
```json
{
    "status": "success",
    "invocationId": "123e4567-e89b-12d3-a456-426614174002",
    "response": [
        {
            "message": "The Python code executed was:\n\ndef fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\nresult = [fibonacci(i) for i in range(10)]\n\nThe result of the execution is:\n\n[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]",
            "type": "text"
        }
    ]
}
```

### 4. Generating Prime Numbers

```bash
curl --location --request POST 'http://localhost:8080/experience/python_executor/generate_and_execute/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data-raw '{
         "query": "Generate a list of prime numbers up to 50"
     }'
```

Expected response:
```json
{
    "status": "success",
    "invocationId": "123e4567-e89b-12d3-a456-426614174003",
    "response": [
        {
            "message": "The Python code executed was:\n\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nresult = [num for num in range(2, 51) if is_prime(num)]\n\nThe result of the execution is:\n\n[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]",
            "type": "text"
        }
    ]
}
```

## Error Handling

The service provides friendly error messages for various scenarios. All responses, including errors, will have a "success" status and use the ResponseMessageModel format. Examples:

1. Invalid input:
```json
{
    "status": "success",
    "invocationId": "123e4567-e89b-12d3-a456-426614174004",
    "response": [
        {
            "message": "Invalid input: Potentially unsafe code detected",
            "type": "text"
        }
    ]
}
```

2. Execution timeout:
```json
{
    "status": "success",
    "invocationId": "123e4567-e89b-12d3-a456-426614174005",
    "response": [
        {
            "message": "Execution timed out after 5 seconds",
            "type": "text"
        }
    ]
}
```

3. Memory limit exceeded:
```json
{
    "status": "success",
    "invocationId": "123e4567-e89b-12d3-a456-426614174006",
    "response": [
        {
            "message": "Memory limit exceeded: 100MB",
            "type": "text"
        }
    ]
}
```

4. Execution error:
```json
{
    "status": "success",
    "invocationId": "123e4567-e89b-12d3-a456-426614174007",
    "response": [
        {
            "message": "Execution error: division by zero",
            "type": "text"
        }
    ]
}
```

## Security Considerations

- The service uses `RestrictedPython` to create a restricted execution environment, preventing access to system resources and limiting available Python functionality.
- Further restrictions such as using a read-only non-root Red Hat UBI-9 minimal, deploying this integration on a separate container, and applying further restrictions on the container level are required.
- Furthermore, this should run as a code-engine single-use faas container, with no state.
- User input and generated code are sanitized to remove potentially harmful operations.
- Execution time and memory usage are limited to prevent resource exhaustion attacks.
- The service should be deployed behind an API gateway with additional security measures such as rate limiting and authentication.
- Pass the user input through security middleware to prevent prompt injection, consider using the `prompt_defender` integration.

## Deployment

For production deployment, consider the following recommendations:

1. Use a read-only, non-root Red Hat UBI-9 minimal container.
2. Deploy this integration on a separate container with additional restrictions at the container level.
3. Implement as a code-engine single-use FaaS container with no persistent state.
4. Set up comprehensive logging and monitoring.
5. Regularly update and patch all dependencies especially `RestrictedPython` .
6. Implement rate limiting and user authentication at the API gateway level.
