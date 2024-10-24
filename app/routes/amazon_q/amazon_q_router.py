# -*- coding: utf-8 -*-
"""
Amazon Q Integration Router

This module provides a FastAPI router for interacting with Amazon Q,
including authentication and querying functionality.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from uuid import uuid4

import boto3
import jwt
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field

# Setup logging
log = logging.getLogger(__name__)

# Load environment variables
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")

# Amazon Q Settings
CLIENT_ID = os.getenv("AMAZON_Q_CLIENT_ID")
USER_POOL_ID = os.getenv("AMAZON_Q_USER_POOL_ID")

REGION = os.getenv("AMAZON_Q_REGION", "us-west-2")
IDC_APPLICATION_ID = os.getenv("AMAZON_Q_IDC_APPLICATION_ID")
IAM_ROLE = os.getenv("AMAZON_Q_IAM_ROLE")
AMAZON_Q_APP_ID = os.getenv("AMAZON_Q_APP_ID")

DEFAULT_USERNAME = os.getenv("AMAZON_Q_DEFAULT_USERNAME")
DEFAULT_PASSWORD = os.getenv("AMAZON_Q_DEFAULT_PASSWORD")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/amazon_q/templates"))


class AmazonQInputModel(BaseModel):
    """Model to validate input data for Amazon Q queries."""

    username: Optional[str] = Field(None, description="Amazon Q username (optional if set in environment)")
    password: Optional[str] = Field(None, description="Amazon Q password (optional if set in environment)")
    query: str = Field(..., description="The query to send to Amazon Q")
    citations: Optional[str] = Field("true", description="Include citations in the response (true/false)")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


async def initiate_auth(username: str, password: str) -> dict:
    """
    Initiate authentication with Amazon Cognito.

    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        dict: The authentication response containing tokens.

    Raises:
        HTTPException: If authentication fails.
    """
    client = boto3.client("cognito-idp", region_name=REGION)
    try:
        resp = await asyncio.to_thread(
            client.admin_initiate_auth,
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
            ClientMetadata={
                "username": username,
                "password": password,
            },
        )
        return resp
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="The username or password is incorrect")
    except client.exceptions.UserNotConfirmedException:
        raise HTTPException(status_code=403, detail="User is not confirmed")
    except Exception as e:
        log.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")


async def get_iam_oidc_token(id_token: str) -> str:
    """
    Exchange Cognito token for IAM OIDC token.

    Args:
        id_token (str): The Cognito ID token.

    Returns:
        str: The IAM OIDC token.

    Raises:
        HTTPException: If token exchange fails.
    """
    client = boto3.client("sso-oidc", region_name=REGION)
    try:
        response = await asyncio.to_thread(
            client.create_token_with_iam,
            clientId=IDC_APPLICATION_ID,
            grantType="urn:ietf:params:oauth:grant-type:jwt-bearer",
            assertion=id_token,
        )
        return response["idToken"]
    except Exception as e:
        log.error(f"IAM OIDC token exchange error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"IAM OIDC token exchange error: {str(e)}")


async def assume_role_with_token(iam_token: str) -> dict:
    """
    Assume IAM role using the IAM OIDC token.

    Args:
        iam_token (str): The IAM OIDC token.

    Returns:
        dict: The assumed role credentials.

    Raises:
        HTTPException: If role assumption fails.
    """
    decoded_token = jwt.decode(iam_token, options={"verify_signature": False})
    sts_client = boto3.client("sts", region_name=REGION)
    try:
        response = await asyncio.to_thread(
            sts_client.assume_role,
            RoleArn=IAM_ROLE,
            RoleSessionName="qapp",
            ProvidedContexts=[
                {
                    "ProviderArn": "arn:aws:iam::aws:contextProvider/IdentityCenter",
                    "ContextAssertion": decoded_token["sts:identity_context"],
                }
            ],
        )
        return response["Credentials"]
    except Exception as e:
        log.error(f"Role assumption error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Role assumption error: {str(e)}")


async def get_qclient(credentials: dict):
    """
    Create an Amazon Q client using assumed role credentials.

    Args:
        credentials (dict): The assumed role credentials.

    Returns:
        boto3.client: The Amazon Q client.

    Raises:
        HTTPException: If client creation fails.
    """
    try:
        session = boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
        return session.client("qbusiness", region_name=REGION)
    except Exception as e:
        log.error(f"Amazon Q client creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Amazon Q client creation error: {str(e)}")


async def query_amazon_q(amazon_q, query: str) -> dict:
    """
    Send a query to Amazon Q and get the response.

    Args:
        amazon_q: The Amazon Q client.
        query (str): The query to send to Amazon Q.

    Returns:
        dict: The response from Amazon Q.

    Raises:
        HTTPException: If the query fails.
    """
    try:
        response = await asyncio.to_thread(amazon_q.chat_sync, applicationId=AMAZON_Q_APP_ID, userMessage=query)
        return response
    except Exception as e:
        log.error(f"Amazon Q query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Amazon Q query error: {str(e)}")


def add_custom_routes(app: FastAPI):
    @app.post("/experience/amazon_q/ask/invoke")
    async def ask_amazon_q(request: Request) -> OutputModel:
        """
        Handle POST requests to ask questions to Amazon Q.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = AmazonQInputModel(**data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        username = input_data.username or DEFAULT_USERNAME
        password = input_data.password or DEFAULT_PASSWORD

        if not username or not password:
            raise HTTPException(
                status_code=400,
                detail="Username and password must be provided either in the request or as environment variables",
            )

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                # Authenticate and get Amazon Q client
                auth_resp = await initiate_auth(username, password)
                id_token = auth_resp["AuthenticationResult"]["IdToken"]
                iam_token = await get_iam_oidc_token(id_token)
                credentials = await assume_role_with_token(iam_token)
                amazon_q = await get_qclient(credentials)

                # Query Amazon Q
                q_response = await query_amazon_q(amazon_q, input_data.query)

            # Choose the appropriate template based on the citations parameter
            template_name = "amazon_q_response_with_citations.jinja" if input_data.citations.lower() != "false" else "amazon_q_response_without_citations.jinja"

            # Render the response using the selected template
            response_template = template_env.get_template(template_name)
            rendered_response = response_template.render(
                result=q_response.get("systemMessage", "No response from Amazon Q"),
                sources=q_response.get("sourceAttributions", []),
            )

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[response_message],
            )
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        except Exception as e:
            # For any other exception, return a 500 error
            log.error(f"Unexpected error in ask_amazon_q: {str(e)}")
            return OutputModel(
                status="error",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"An unexpected error occurred: {str(e)}", type="text")],
            )

    @app.post("/system/amazon_q/auth/invoke")
    async def authenticate_amazon_q(request: Request) -> OutputModel:
        """
        Handle POST requests to authenticate with Amazon Q.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or authentication fails.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = AmazonQInputModel(**data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        username = input_data.username or DEFAULT_USERNAME
        password = input_data.password or DEFAULT_PASSWORD

        if not username or not password:
            raise HTTPException(
                status_code=400,
                detail="Username and password must be provided either in the request or as environment variables",
            )

        try:
            auth_resp = await initiate_auth(username, password)
            id_token = auth_resp["AuthenticationResult"]["IdToken"]
            response_message = ResponseMessageModel(message=f"Authentication successful. ID Token: {id_token}")
        except Exception as e:
            log.error(f"Authentication failed: {str(e)}")
            response_message = ResponseMessageModel(message=f"Authentication failed: {str(e)}")

        return OutputModel(invocationId=invocation_id, response=[response_message])


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()
    add_custom_routes(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)
