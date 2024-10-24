# Amazon Q Integration

This integration provides services for interacting with Amazon Q, including authentication and querying functionality.

## Environment Variables

Before using this integration, make sure to export the following environment variables:

```bash
export DEFAULT_MAX_THREADS=4  # Optional, defaults to 4 if not set
export ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME="Llama3.1 70b Instruct"  # Optional, defaults to "Llama3.1 70b Instruct" if not set
export AMAZON_Q_CLIENT_ID="your_client_id"
export AMAZON_Q_USER_POOL_ID="your_user_pool_id"
export AMAZON_Q_REGION="us-west-2"  # Optional, defaults to "us-west-2" if not set
export AMAZON_Q_IDC_APPLICATION_ID="your_idc_application_id"
export AMAZON_Q_IAM_ROLE="your_iam_role"
export AMAZON_Q_APP_ID="your_amazon_q_app_id"
export AMAZON_Q_DEFAULT_USERNAME="your_default_username"  # Optional, can be overridden in the request
export AMAZON_Q_DEFAULT_PASSWORD="your_default_password"  # Optional, can be overridden in the request
```

Make sure to replace the placeholder values with your actual Amazon Q configuration details.

## Endpoints

- POST /experience/amazon_q/ask/invoke
  Invokes the Experience API to authenticate with Amazon Q and ask a question.

- POST /system/amazon_q/auth/invoke
  Invokes the System API to authenticate with Amazon Q.

## Testing the integration locally

### Ask Amazon Q - Experience API

This endpoint authenticates with Amazon Q and sends a query. You can provide the username and password in the request, or use the default values set in the environment variables.

```bash
curl --location --request POST \
    'http://localhost:8080/experience/amazon_q/ask/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "query": "What is EKS?"
    }'

curl --location --request POST \
    'http://localhost:8080/experience/amazon_q/ask/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "username": "your_username",  # Optional if set in environment
        "password": "your_password",  # Optional if set in environment
        "query": "What is EKS?"
    }'
```

### Authenticate with Amazon Q - System API

This endpoint authenticates with Amazon Q and returns the ID token. You can provide the username and password in the request, or use the default values set in the environment variables.

```bash
curl --location --request POST \
    'http://localhost:8080/system/amazon_q/auth/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "username": "your_username",  # Optional if set in environment
        "password": "your_password",  # Optional if set in environment
        "query": "dummy_query"
    }'
```

Note: The "query" field is required in the input model but not used for the authentication endpoint.

## Requirements:

```
# FastAPI and related packages
fastapi==0.103.2
uvicorn==0.23.2
pydantic==2.4.2

# AWS SDK
boto3==1.28.57

# JWT handling
PyJWT==2.8.0

# Template rendering
Jinja2==3.1.2

# Environment variable management
python-dotenv==1.0.0

# Async HTTP client (for potential future use)
httpx==0.25.0

# IBM Consulting Assistants library
libica==0.7.0

# Other utility libraries
python-multipart==0.0.6
```
