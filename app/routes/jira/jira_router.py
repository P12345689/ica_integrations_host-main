# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Jira integration router.

This module provides routes for interacting with Jira, including creating issues,
searching for issues, retrieving issue information, exporting issues as CSV,
and answering Jira-related questions.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import csv
import logging
import os
import traceback
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from jinja2 import Environment, FileSystemLoader
from jira import JIRA, JIRAError
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Define default values
DEFAULT_JIRA_URL = os.getenv("JIRA_URL", "https://jsw.ibm.com")
DEFAULT_JIRA_USERNAME = os.getenv("JIRA_USERNAME")
DEFAULT_JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/jira/templates"))

# New model for JIRA authentication
class JiraAuthModel(BaseModel):
    jira_url: Optional[str] = None
    jira_username: Optional[str] = None
    jira_api_token: Optional[str] = None

class JiraIssueInputModel(BaseModel):
    """Model to validate input data for Jira issue creation."""
    project_key: str = Field(..., description="The project key where the issue will be created")
    summary: str = Field(..., description="The summary of the issue")
    description: str = Field(..., description="The description of the issue")
    issuetype: str = Field(default="Task", description="The type of the issue")
    assignee: Optional[str] = Field(None, description="The username of the assignee")
    auth: Optional[JiraAuthModel] = None

class JiraSearchInputModel(BaseModel):
    """Model to validate input data for Jira issue search."""
    project_key: str = Field(..., description="The project key to search in")
    assignee: Optional[str] = Field(None, description="Filter by assignee (username)")
    status: Optional[str] = Field(None, description="Filter by status")
    issuetype: Optional[str] = Field(None, description="Filter by type")
    max_results: int = Field(default=50, description="The maximum number of results to return")
    auth: Optional[JiraAuthModel] = None

class JiraIssueKeyModel(BaseModel):
    """Model to validate input data for retrieving a Jira issue."""
    issue_key: str = Field(..., description="The key of the Jira issue to retrieve")
    auth: Optional[JiraAuthModel] = None

class JiraQueryInputModel(BaseModel):
    """Model to validate input data for Jira-related queries."""
    query: str = Field(..., description="The Jira-related query")

class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""
    message: str
    type: str = "text"

class OutputModel(BaseModel):
    """Model to structure the output response."""
    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]

async def get_jira_client(auth: Optional[JiraAuthModel] = None) -> JIRA:
    """Create and return a JIRA client instance."""
    jira_url = auth.jira_url if auth and auth.jira_url else DEFAULT_JIRA_URL
    jira_username = auth.jira_username if auth and auth.jira_username else DEFAULT_JIRA_USERNAME
    jira_api_token = auth.jira_api_token if auth and auth.jira_api_token else DEFAULT_JIRA_API_TOKEN
    
    log.info(f"Connecting to Jira instance at URL: {jira_url}")
    return JIRA(server=jira_url, basic_auth=(jira_username, jira_api_token))

def create_jql_query(project_key: str, assignee: Optional[str] = None, status: Optional[str] = None, issuetype: Optional[str] = None) -> str:
    """
    Create a JQL query string with proper escaping.

    Args:
        project_key (str): The project key to search in.
        assignee (Optional[str]): The assignee's username or email.
        status (Optional[str]): The status to filter by. If None, all statuses are included.
        issuetype (Optional[str]): The type to filter by. If None, all issue types are included.

    Returns:
        str: A properly formatted JQL query string.
    """
    jql = f"project = {project_key}"
    if assignee:
        jql += f' AND assignee = "{assignee}"'
    if status:
        jql += f' AND status = "{status}"'
    if issuetype:
        jql += f' AND issuetype = "{issuetype}"'

    log.info(f"Created JQL query: {jql}")
    return jql

async def get_project_statuses(project_key: str, auth: Optional[JiraAuthModel] = None) -> List[str]:
    """
    Retrieve available status options for a given project.

    Args:
        project_key (str): The key of the project to get statuses for.
        auth (Optional[JiraAuthModel]): Optional authentication parameters.

    Returns:
        List[str]: A list of available status options.

    Raises:
        JIRAError: If there's an error retrieving the statuses.
    """
    try:
        jira = await get_jira_client(auth)
        await asyncio.to_thread(jira.project, project_key)
        statuses = await asyncio.to_thread(jira.statuses)
        return list(set(status.name for status in statuses))
    except JIRAError as e:
        log.error(f"JIRAError retrieving statuses for project {project_key}: {str(e)}")
        raise
    except Exception as e:
        log.error(f"Unexpected error retrieving project statuses: {str(e)}")
        raise

async def create_jira_issue(issue_data: JiraIssueInputModel) -> str:
    """
    Create a new Jira issue.

    Args:
        issue_data (JiraIssueInputModel): The data for the new issue.

    Returns:
        str: The key of the created issue.

    Raises:
        JIRAError: If there's an error creating the issue.
    """
    log.info(f"Attempting to create Jira issue for project: {issue_data.project_key}")
    try:
        jira = await get_jira_client(issue_data.auth)
        log.info(f"Connected to Jira instance at URL: {jira.server_url}")

        log.info("Creating issue with the following data:")
        log.info(f"Project: {issue_data.project_key}")
        log.info(f"Summary: {issue_data.summary}")
        log.info(f"Description: {issue_data.description[:100]}...") # First 100 chars of description
        log.info(f"Issue Type: {issue_data.issuetype}")
        log.info(f"Assignee: {issue_data.assignee}")

        issue_dict = {
            "project": issue_data.project_key,
            "summary": issue_data.summary,
            "description": issue_data.description,
            "issuetype": {"name": issue_data.issuetype},
        }

        if issue_data.assignee:
            issue_dict["assignee"] = {"name": issue_data.assignee}

        new_issue = await asyncio.to_thread(
            jira.create_issue,
            fields=issue_dict
        )
        log.info(f"Jira issue created successfully. Key: {new_issue.key}")
        return new_issue.key
    except JIRAError as e:
        log.error(f"JIRAError creating issue: {str(e)}")
        log.error(f"JIRA API response: {e.response.text if e.response else 'No response'}")
        log.error(f"JIRA error status: {e.status_code}")
        raise
    except Exception as e:
        log.error(f"Unexpected error creating Jira issue: {str(e)}")
        log.error(f"Traceback: {traceback.format_exc()}")
        raise
    

async def search_jira_issues(jql: str, max_results: int = 50, auth: Optional[JiraAuthModel] = None) -> List[Dict[str, str]]:
    """
    Search for Jira issues using JQL.

    Args:
        jql (str): The JQL query to search for issues.
        max_results (int, optional): The maximum number of results to return. Defaults to 50.
        auth (Optional[JiraAuthModel]): Optional authentication parameters.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing issue information.

    Raises:
        JIRAError: If there's an error searching for issues.
    """
    log.info(f"Searching for Jira issues with JQL: {jql}, max_results: {max_results}")
    
    try:
        jira = await get_jira_client(auth)
        issues = await asyncio.to_thread(jira.search_issues, jql, maxResults=max_results)
        log.info(f"Found {len(issues)} issues")
        
        result = [
            {
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "issuetype": issue.fields.issuetype.name,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                "created": issue.fields.created,
                "updated": issue.fields.updated,
                "description": issue.fields.description,
            }
            for issue in issues
        ]
        log.info(f"Processed {len(result)} issues")
        return result
    except JIRAError as e:
        log.error(f"JIRAError searching issues: {str(e)}")
        raise
    except Exception as e:
        log.error(f"Unexpected error searching Jira issues: {str(e)}")
        raise


async def get_jira_issue(issue_key: str, auth: Optional[JiraAuthModel] = None) -> Dict[str, str]:
    """
    Retrieve information about a Jira issue.

    Args:
        issue_key (str): The key of the issue to retrieve.
        auth (Optional[JiraAuthModel]): Optional authentication parameters.

    Returns:
        Dict[str, str]: A dictionary containing issue information.

    Raises:
        JIRAError: If there's an error retrieving the issue.
    """
    try:
        jira = await get_jira_client(auth)
        issue = await asyncio.to_thread(jira.issue, issue_key)
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name,
            "issuetype": issue.fields.issuetype.name,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
            "reporter": issue.fields.reporter.displayName if issue.fields.reporter else "Unreported",
            "created": issue.fields.created,
            "updated": issue.fields.updated,
            "priority": issue.fields.priority.name if issue.fields.priority else "Unset",
            "labels": ", ".join(issue.fields.labels) if issue.fields.labels else "None",
            "resolution": issue.fields.resolution.name if issue.fields.resolution else "Unresolved",
        }
    except JIRAError as e:
        log.error(f"JIRAError retrieving issue {issue_key}: {str(e)}")
        raise
    except Exception as e:
        log.error(f"Unexpected error retrieving Jira issue: {str(e)}")
        raise

def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/jira/retrievers/create_issue/invoke")
    async def create_jira_issue_route(request: Request) -> OutputModel:
        """
        Handle POST requests to create a new Jira issue.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or there's an error creating the issue.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = JiraIssueInputModel(**data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        try:
            issue_key = await create_jira_issue(input_data)

            response_message = ResponseMessageModel(message=f"Jira issue created successfully. Issue key: {issue_key}")
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except JIRAError as e:
            log.error(f"JIRAError in create_jira_issue_route: {str(e)}")
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except Exception as e:
            log.error(f"Unexpected error in create_jira_issue_route: {str(e)}")
            raise HTTPException(status_code=500, detail="Error creating Jira issue")

    @app.post("/system/jira/retrievers/search_issues/invoke")
    async def search_jira_issues_route(request: Request) -> OutputModel:
        """
        Handle POST requests to search for Jira issues.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or there's an error searching for issues.
        """
        invocation_id = str(uuid4())
        log.info(f"Received search issues request. Invocation ID: {invocation_id}")

        try:
            data = await request.json()
            log.info(f"Received data: {data}")
            input_data = JiraSearchInputModel(**data)
            log.info(f"Parsed input data: {input_data}")
        except Exception as e:
            log.error(f"Error parsing input data: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        # Only use non-empty strings for filtering
        status = input_data.status if input_data.status and input_data.status.strip() else None
        issuetype = input_data.issuetype if input_data.issuetype and input_data.issuetype.strip() else None
        assignee = input_data.assignee if input_data.assignee and input_data.assignee.strip() else None

        jql = create_jql_query(input_data.project_key, assignee, status, issuetype)
        
        try:
            issues = await search_jira_issues(jql, input_data.max_results, input_data.auth)
            log.info(f"Retrieved {len(issues)} issues")

            response_message = ResponseMessageModel(
                message=f"Found {len(issues)} issues:\n\n" + "\n".join(
                    [f"Issue {i + 1}:\n" + "\n".join([f"{key}: {value}" for key, value in issue.items()]) for i, issue in enumerate(issues)]
                )
            )
            log.info(f"Created response message with {len(issues)} issues")
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except JIRAError as e:
            log.error(f"JIRAError in search_jira_issues_route: {str(e)}")
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except Exception as e:
            log.error(f"Unexpected error in search_jira_issues_route: {str(e)}")
            raise HTTPException(status_code=500, detail="Error searching Jira issues")
        
    @app.post("/system/jira/retrievers/export_issues_csv/invoke")
    async def export_jira_issues_csv_route(request: Request) -> StreamingResponse:
        """
        Handle POST requests to export Jira issues as CSV.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            StreamingResponse: A streaming response containing the CSV data.
            or
            JSONResponse: A JSON response if no issues are found or an error occurs.

        Raises:
            HTTPException: If the input is invalid or there's an error exporting issues.
        """
        log.info("Received request to export Jira issues as CSV")
        try:
            data = await request.json()
            log.info(f"Received data: {data}")
            input_data = JiraSearchInputModel(**data)
            log.info(f"Parsed input data: {input_data}")
        except Exception as e:
            log.error(f"Error parsing input data: {str(e)}")
            return JSONResponse(status_code=422, content={"error": str(e)})

        # Only use non-empty strings for filtering
        status = input_data.status if input_data.status and input_data.status.strip() else None
        issuetype = input_data.issuetype if input_data.issuetype and input_data.issuetype.strip() else None
        assignee = input_data.assignee if input_data.assignee and input_data.assignee.strip() else None

        jql = create_jql_query(input_data.project_key, assignee, status, issuetype)
        log.info(f"Created JQL query for CSV export: {jql}")

        try:
            issues = await search_jira_issues(jql, input_data.max_results, input_data.auth)
            log.info(f"Retrieved {len(issues)} issues for CSV export")

            if not issues:
                log.info("No issues found matching the criteria")
                return JSONResponse(
                    content={"message": "No issues found matching the criteria."},
                    status_code=200,
                )

            output = StringIO()
            writer = csv.DictWriter(
                output,
                fieldnames=[
                    "key",
                    "summary",
                    "status",
                    "issuetype",
                    "assignee",
                    "created",
                    "updated",
                    "description"
                ],
            )
            writer.writeheader()
            writer.writerows(issues)
            log.info(f"Created CSV with {len(issues)} issues")

            response = StreamingResponse(iter([output.getvalue()]), media_type="text/csv")
            response.headers["Content-Disposition"] = f"attachment; filename=jira_issues_{input_data.project_key}.csv"
            log.info("Returning CSV StreamingResponse")
            return response
        except JIRAError as e:
            log.error(f"JIRAError in export_jira_issues_csv_route: {str(e)}")
            return JSONResponse(status_code=e.status_code, content={"error": str(e)})
        except Exception as e:
            log.error(f"Unexpected error in export_jira_issues_csv_route: {str(e)}")
            return JSONResponse(status_code=500, content={"error": "Error exporting Jira issues"})
        
    @app.post("/system/jira/retrievers/get_issue/invoke")
    async def get_jira_issue_route(request: Request) -> OutputModel:
        """
        Handle POST requests to retrieve a Jira issue.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or there's an error retrieving the issue.
        """
        invocation_id = str(uuid4())
        log.info(f"Received get issue request. Invocation ID: {invocation_id}")

        try:
            data = await request.json()
            log.info(f"Received data: {data}")
            input_data = JiraIssueKeyModel(**data)
            log.info(f"Parsed input data: {input_data}")
        except Exception as e:
            log.error(f"Error parsing input data: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            issue = await get_jira_issue(input_data.issue_key, input_data.auth)
            log.info(f"Retrieved issue: {issue['key']}")

            # Format the issue details as a string
            issue_details = "\n".join([f"{key}: {value}" for key, value in issue.items()])
            
            response_message = ResponseMessageModel(
                message=f"Issue details for {input_data.issue_key}:\n\n{issue_details}"
            )
            log.info("Created response message with issue details")
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except JIRAError as e:
            log.error(f"JIRAError in get_jira_issue_route: {str(e)}")
            if e.status_code == 404:
                error_message = f"Jira issue {input_data.issue_key} not found"
            else:
                error_message = f"JIRA API Error: {str(e)}"
            return OutputModel(
                status="error",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=error_message)]
            )
        except Exception as e:
            log.error(f"Unexpected error in get_jira_issue_route: {str(e)}")
            log.error(traceback.format_exc())
            return OutputModel(
                status="error",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"Error retrieving Jira issue: {str(e)}")]
            )

    @app.post("/experience/jira/ask_jira/invoke")
    async def ask_jira(request: Request) -> OutputModel:
        """
        Handle POST requests to ask Jira-related questions.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or there's an error processing the query.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = JiraQueryInputModel(**data)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

        prompt_template = template_env.get_template("jira_prompt.jinja")
        rendered_prompt = prompt_template.render(query=input_data.query)

        client = ICAClient()

        async def call_prompt_flow():
            return await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt,
            )

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                formatted_result_future = executor.submit(asyncio.run, call_prompt_flow())
                formatted_result = formatted_result_future.result()

            response_template = template_env.get_template("jira_response.jinja")
            rendered_response = response_template.render(result=formatted_result)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error in ask_jira: {str(e)}")
            log.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="Error processing Jira query")

    @app.get("/system/jira/retrievers/get_project_statuses/invoke")
    async def get_project_statuses_route(project_key: str, auth: Optional[JiraAuthModel] = None) -> OutputModel:
        """
        Handle GET requests to retrieve available status options for a project.

        Args:
            project_key (str): The key of the project to get statuses for.
            auth (Optional[JiraAuthModel]): Optional authentication parameters.

        Returns:
            OutputModel: The structured output response containing available statuses.

        Raises:
            HTTPException: If there's an error retrieving the statuses.
        """
        invocation_id = str(uuid4())

        try:
            statuses = await get_project_statuses(project_key, auth)
            response_message = ResponseMessageModel(message=f"Available statuses for project {project_key}:\n\n" + "\n".join(statuses))
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except JIRAError as e:
            log.error(f"JIRAError in get_project_statuses_route: {str(e)}")
            raise HTTPException(status_code=e.status_code, detail=str(e))
        except Exception as e:
            log.error(f"Unexpected error in get_project_statuses_route: {str(e)}")
            raise HTTPException(status_code=500, detail="Error retrieving project statuses")


if __name__ == "__main__":
    import doctest
    doctest.testmod()