# -*- coding: utf-8 -*-
"""
Amazon Q tool for querying Amazon Q.

This module provides a tool that uses the Amazon Q querying functionality from the main router.
"""

from langchain.agents import tool

# Import the necessary functions from the main router
from app.routes.amazon_q.amazon_q_router import assume_role_with_token, get_iam_oidc_token, get_qclient, initiate_auth, query_amazon_q


@tool
async def query_amazon_q_tool(username: str, password: str, query: str) -> str:
    """
    Tool for querying Amazon Q.

    Args:
        username (str): Amazon Q username.
        password (str): Amazon Q password.
        query (str): The query to send to Amazon Q.

    Returns:
        str: The response from Amazon Q.
    """
    auth_resp = await initiate_auth(username, password)
    id_token = auth_resp["AuthenticationResult"]["IdToken"]
    iam_token = await get_iam_oidc_token(id_token)
    credentials = await assume_role_with_token(iam_token)
    amazon_q = await get_qclient(credentials)
    return await query_amazon_q(amazon_q, query)
