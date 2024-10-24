# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: GitHub Integration for both Enterprise and public repositories

This module provides routes for various GitHub operations, including retrieving issues,
pull requests, releases, and individual files, as well as creating issues, PRs, tags, and releases.
It also includes LLM support for summarizing issues and other tasks.
"""

import asyncio
import json
import logging
import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Optional, Union
from urllib.parse import urlparse
from uuid import uuid4
from shutil import which

from fastapi import FastAPI, HTTPException, Request
from github import Github, GithubException
from github.ContentFile import ContentFile
from github.Repository import Repository
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to INFO in production

# Set default model and max threads from environment variables
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/github/templates"))

# Set the base directory for cloning repositories
BASE_CLONE_DIR = Path("public/github")


class GitHubInputModel(BaseModel):
    """Model to validate input data for GitHub operations."""

    repo_url: str = Field(..., description="Full URL of the GitHub repository")
    action: str = Field(..., description="Action to perform (e.g., 'list_issues', 'create_pr', 'clone_repo')")
    params: dict = Field(default={}, description="Additional parameters for the action")
    github_token: Optional[str] = Field(None, description="GitHub access token")


class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""

    repo_url: Optional[str] = Field(None, description="Full URL of the GitHub repository")
    query: str = Field(..., description="The input query describing the desired GitHub operation")
    github_token: Optional[str] = Field(None, description="GitHub access token")


class CloneRepoInputModel(BaseModel):
    """Model to validate input data for cloning a repository."""

    repo_url: str = Field(..., description="Full URL of the GitHub repository")
    depth: int = Field(default=0, description="Depth of the clone (default is 0 for full clone)")
    github_token: Optional[str] = Field(None, description="GitHub access token")


class GitFameInputModel(BaseModel):
    """Model to validate input data for git fame analysis."""

    repo_url: str = Field(..., description="Full URL of the GitHub repository")
    exclusions: List[str] = Field(default=[], description="List of patterns to exclude from analysis")
    github_token: Optional[str] = Field(None, description="GitHub access token")

class RepoAnalysisInputModel(BaseModel):
    """Model to validate input data for repository analysis."""

    repo_url: str = Field(..., description="Full URL of the GitHub repository")
    analysis_tools: List[str] = Field(..., description="List of analysis tools to run (e.g., ['fame', 'pylint', 'scc', 'pyreverse'])")
    target_path: str = Field(default="app", description="Target path or module to analyze")
    exclusions: List[str] = Field(default=[], description="List of patterns to exclude from analysis")
    github_token: Optional[str] = Field(None, description="GitHub access token")
    
class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def parse_repo_url(repo_url: str) -> tuple[str, str]:
    """
    Parse the repository URL to extract the base URL and repo name.

    Args:
        repo_url (str): Full URL of the GitHub repository.

    Returns:
        tuple[str, str]: A tuple containing the base URL and repo name.

    Example:
        >>> parse_repo_url("https://github.com/user/repo")
        ('https://github.com', 'user/repo')
    """
    parsed_url = urlparse(repo_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    repo_name = parsed_url.path.strip("/")
    return base_url, repo_name


def github_operation(token: Optional[str], repo_url: str, action: str, params: dict) -> str:
    """
    Perform a GitHub operation based on the given action.

    Args:
        token (Optional[str]): GitHub access token.
        repo_url (str): Full URL of the GitHub repository.
        action (str): Action to perform.
        params (dict): Additional parameters for the action.

    Returns:
        str: Result of the operation.

    Raises:
        ValueError: If the action is not supported or if required parameters are missing.

    Example:
        >>> github_operation(None, "https://github.com/user/repo", "list_issues", {})
        '#1: First issue\n#2: Second issue'
    """
    base_url, repo_name = parse_repo_url(repo_url)
    g = Github(base_url=f"{base_url}/api/v3", login_or_token=token) if token else Github(base_url=f"{base_url}/api/v3")
    repository: Repository = g.get_repo(repo_name)

    if action == "list_issues":
        issues = repository.get_issues()
        return "\n".join([f"#{issue.number}: {issue.title}" for issue in issues])

    elif action == "get_issue":
        issue_number = params.get("issue_number")
        if not issue_number:
            raise ValueError("Issue number is required to get an issue")
        issue = repository.get_issue(number=int(issue_number))
        return f"#{issue.number}: {issue.title}\n\n{issue.body}"

    elif action == "create_issue":
        title = params.get("title")
        body = params.get("body")
        if not title or not body:
            raise ValueError("Title and body are required to create an issue")
        issue = repository.create_issue(title=str(title), body=str(body))
        return f"Issue created: #{issue.number} - {issue.title}"

    elif action == "list_prs":
        prs = repository.get_pulls()
        return "\n".join([f"#{pr.number}: {pr.title}" for pr in prs])

    elif action == "get_pr":
        pr_number = params.get("pr_number")
        if not pr_number:
            raise ValueError("PR number is required to get a pull request")
        pr = repository.get_pull(number=int(pr_number))
        return f"#{pr.number}: {pr.title}\n\n{pr.body}"

    elif action == "create_pr":
        title = params.get("title")
        body = params.get("body")
        head = params.get("head")
        base = params.get("base", "main")
        if not all([title, body, head]):
            raise ValueError("Title, body, and head branch are required to create a PR")
        pr = repository.create_pull(title=str(title), body=str(body), head=str(head), base=str(base))
        return f"PR created: #{pr.number} - {pr.title}"

    elif action == "list_releases":
        releases = repository.get_releases()
        return "\n".join([f"{release.tag_name}: {release.title}" for release in releases])

    elif action == "create_release":
        tag = params.get("tag")
        title = params.get("title")
        body = params.get("body")
        if not all([tag, title, body]):
            raise ValueError("Tag, title, and body are required to create a release")
        release = repository.create_git_release(tag=str(tag), name=str(title), message=str(body))
        return f"Release created: {release.tag_name} - {release.title}"

    elif action == "get_file":
        # TODO: get directories too, or retrieve multiple files.

        path = params.get("path")
        if not path:
            raise ValueError("File path is required")
        content_file: Union[ContentFile, List[ContentFile]] = repository.get_contents(path)
        if isinstance(content_file, list):
            raise ValueError("The specified path is a directory, not a file")
        return content_file.decoded_content.decode()

    else:
        raise ValueError(f"Unsupported action: {action}")


async def clone_or_update_repo(repo_url: str, depth: int = 0, token: Optional[str] = None) -> str:
    """
    Clone a repository or update it if it already exists.

    Args:
        repo_url (str): Full URL of the GitHub repository.
        depth (int): Depth of the clone (default is 0 for full clone).
        token (Optional[str]): GitHub access token.

    Returns:
        str: Result of the operation.

    Raises:
        subprocess.CalledProcessError: If the git command fails.

    Example:
        >>> asyncio.run(clone_or_update_repo("https://github.com/user/repo"))
        'Repository cloned successfully: public/github/user/repo'
    """
    _, repo_name = parse_repo_url(repo_url)
    repo_path = BASE_CLONE_DIR / repo_name

    if token:
        repo_url = repo_url.replace("https://", f"https://{token}@")

    if repo_path.exists():
        log.info(f"Repository already exists: {repo_path}")
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                ["git", "-C", str(repo_path), "pull"],
                capture_output=True,
                text=True,
                check=True,
            )
            return f"Repository updated successfully: {repo_path}\n{result.stdout}"
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to update repository: {e}")
            raise

    log.info(f"Cloning repository: {repo_url}")
    try:
        clone_command = ["git", "clone"]
        if depth > 0:
            clone_command.extend(["--depth", str(depth)])
        clone_command.extend([repo_url, str(repo_path)])
        
        result = await asyncio.to_thread(
            subprocess.run,
            clone_command,
            capture_output=True,
            text=True,
            check=True,
        )
        return f"Repository cloned successfully: {repo_path}\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to clone repository: {e}")
        raise


async def run_git_fame(repo_name: str, exclusions: List[str]) -> str:
    """
    Run git fame on a cloned repository.

    Args:
        repo_name (str): Name of the repository to analyze.
        exclusions (List[str]): List of patterns to exclude from analysis.

    Returns:
        str: Result of the git fame analysis.

    Raises:
        subprocess.CalledProcessError: If the git fame command fails.
        FileNotFoundError: If the repository directory doesn't exist.

    Example:
        >>> asyncio.run(run_git_fame("user/repo", ["*.md"]))
        'Total commits: 100\nTotal files: 50\n...'
    """
    repo_path = BASE_CLONE_DIR / repo_name

    if not repo_path.exists():
        raise FileNotFoundError(f"Repository not found: {repo_path}")

    exclusion_args = [f"--excl='{pattern}'" for pattern in exclusions]
    command = ["git", "fame", "--excl=models/models--*", "-e", "-R"] + exclusion_args + ["."]
    log.info(f"Command: {command} in {repo_path}")

    try:
        result = await asyncio.to_thread(
            subprocess.run,
            command,
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to run git fame: {e}")
        raise


async def run_analysis_tool(repo_path: Path, tool: str, target_path: str, exclusions: List[str]) -> str:
    """
    Run a specified analysis tool on a cloned repository.

    Args:
        repo_path (Path): Path to the cloned repository.
        tool (str): Name of the analysis tool to run.
        target_path (str): Target path or module to analyze.
        exclusions (List[str]): List of patterns to exclude from analysis.

    Returns:
        str: Result of the analysis.

    Raises:
        subprocess.CalledProcessError: If the analysis command fails.
        ValueError: If an unsupported tool is specified.
    """
    if not repo_path.exists():
        raise FileNotFoundError(f"Repository not found: {repo_path}")

    analysis_path = repo_path / target_path
    log.info(f"Running {tool} analysis on {analysis_path}")

    async def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        log.info(f"Current working directory: {os.getcwd()}")
        log.info(f"Executing command: {' '.join(cmd)}")
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                cmd,
                capture_output=True,
                text=True,
                check=check,
            )
            return result
        except subprocess.CalledProcessError as e:
            log.error(f"Command failed: {e}")
            log.error(f"Exit Code: {e.returncode}")
            log.error(f"Stdout: {e.stdout}")
            log.error(f"Stderr: {e.stderr}")
            raise

    if tool == "fame":
        exclusion_args = [f"--excl='{pattern}'" for pattern in exclusions]
        command = ["git", "fame", "--excl=models/models--*", "-e", "-R"] + exclusion_args + ["."]
    elif tool == "pylint":
        command = ["pylint", "."]
    elif tool == "scc":
        scc_path = which("scc")
        if scc_path is None:
            log.error("scc is not installed or not in the system PATH")
            return "Error: scc is not installed or not in the system PATH"
        
        log.info(f"scc found at: {scc_path}")
        
        try:
            version_result = await run_command([scc_path, "--version"], check=False)
            log.info(f"scc version: {version_result.stdout.strip()}")
        except Exception as e:
            log.error(f"Failed to get scc version: {e}")
        
        command = [scc_path, "."]
    elif tool == "pyreverse":
        output_dir = repo_path / "pyreverse_output"
        output_dir.mkdir(exist_ok=True)
        command = ["pyreverse", "-o", "png", "-d", str(output_dir), "."]
    else:
        raise ValueError(f"Unsupported analysis tool: {tool}")

    try:
        # Add the repo path to sys.path for Python-based tools
        original_sys_path = sys.path.copy()
        sys.path.insert(0, str(repo_path))
        
        # Change to the repo directory
        original_cwd = os.getcwd()
        os.chdir(str(analysis_path))
        
        log.info(f"Changed working directory to: {os.getcwd()}")
        log.info(f"Directory contents: {os.listdir('.')}")
        
        result = await run_command(command)
        log.info(f"{tool} analysis completed successfully")
        return f"{tool.upper()} Analysis Result:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to run {tool}: {e}")
        error_message = f"Error running {tool}:\nCommand: {' '.join(command)}\nExit Code: {e.returncode}\nStdout: {e.stdout}\nStderr: {e.stderr}"
        return error_message
    finally:
        # Restore the original working directory and sys.path
        os.chdir(original_cwd)
        sys.path = original_sys_path
        log.info(f"Restored working directory to: {os.getcwd()}")
        
        
def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/github/invoke")
    async def github_route(request: Request) -> OutputModel:
        """
        Handle POST requests for GitHub operations.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the GitHub operation fails.

        Example:
            >>> client = TestClient(app)
            >>> response = client.post("/system/github/invoke", json={"repo_url": "https://github.com/user/repo", "action": "list_issues"})
            >>> response.status_code
            200
        """
        log.info("Received request for GitHub operation")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = GitHubInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    github_operation,
                    input_data.github_token,
                    input_data.repo_url,
                    input_data.action,
                    input_data.params,
                )
                result = future.result()
        except ValueError as e:
            log.error(f"Error in GitHub operation: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except GithubException as e:
            log.error(f"GitHub API error: {str(e)}")
            raise HTTPException(status_code=e.status, detail=str(e))
        except Exception as e:
            log.error(f"Error performing GitHub operation: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to perform GitHub operation")

        log.info(f"GitHub operation completed: {input_data.action}")
        response_message = ResponseMessageModel(message=result)
        return OutputModel(invocationId=invocation_id, response=[response_message])
    
    
    @app.post("/experience/github/invoke")
    async def github_experience(request: Request) -> OutputModel:
        """
        Handle POST requests for GitHub operations with LLM support.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.

        Example:
            >>> client = TestClient(app)
            >>> response = client.post("/experience/github/invoke", json={"repo_url": "https://github.com/user/repo", "query": "List all open issues"})
            >>> response.status_code
            200
        """
        log.info("Received request for GitHub experience")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ExperienceInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        # Render the prompt using Jinja2
        prompt_template = template_env.get_template("prompt.jinja")
        rendered_prompt = prompt_template.render(query=input_data.query, repo_url=input_data.repo_url)
        log.debug(f"Rendered prompt: {rendered_prompt}")

        # Call the LLM
        client = ICAClient()

        async def call_prompt_flow():
            """Async wrapper for the LLM call."""
            log.debug("Calling LLM")
            return await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt,
            )

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                llm_response_future = executor.submit(asyncio.run, call_prompt_flow())
                llm_response = llm_response_future.result()
            log.debug(f"Received LLM response: {llm_response}")

            # Process LLM response and perform GitHub operation if needed
            action_data = json.loads(llm_response)
            if action_data.get("action"):
                github_result = github_operation(
                    input_data.github_token,
                    action_data["repo_url"],
                    action_data["action"],
                    action_data.get("params", {}),
                )
                final_response = f"LLM Analysis:\n{action_data.get('analysis', '')}\n\nGitHub Operation Result:\n{github_result}"
            else:
                final_response = f"LLM Analysis:\n{action_data.get('analysis', '')}"

        except json.JSONDecodeError as e:
            log.error(f"Error parsing JSON from LLM response: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing LLM response")
        except Exception as e:
            log.error(f"Error in GitHub experience: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to process GitHub experience")

        log.info("GitHub experience request processed successfully")
        response_message = ResponseMessageModel(message=final_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])
    
    
    @app.post("/system/github/clone/invoke")
    async def clone_repo(request: Request) -> OutputModel:
        """
        Handle POST requests for cloning or updating a GitHub repository.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the cloning operation fails.

        Example:
            >>> client = TestClient(app)
            >>> response = client.post("/system/github/clone/invoke", json={"repo_url": "https://github.com/user/repo", "depth": 0})
            >>> response.status_code
            200
        """
        log.info("Received request to clone or update repository")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = CloneRepoInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            result = await clone_or_update_repo(input_data.repo_url, input_data.depth, input_data.github_token)
        except subprocess.CalledProcessError as e:
            log.error(f"Error cloning or updating repository: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to clone or update repository: {e.stderr}")
        except Exception as e:
            log.error(f"Unexpected error during repository operation: {str(e)}")
            raise HTTPException(status_code=500, detail="Unexpected error during repository operation")

        log.info("Repository cloned or updated successfully")
        response_message = ResponseMessageModel(message=result)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/system/github/git-fame/invoke")
    async def git_fame_analysis(request: Request) -> OutputModel:
        """
        Handle POST requests for running git fame on a cloned GitHub repository.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the git fame operation fails.

        Example:
            >>> client = TestClient(app)
            >>> response = client.post("/system/github/git-fame/invoke", json={"repo_url": "https://github.com/user/repo", "exclusions": ["*.md"]})
            >>> response.status_code
            200
        """
        log.info("Received request for git fame analysis")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = GitFameInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            # First, ensure the repository is cloned and up-to-date
            # Use depth=0 for a full clone
            await clone_or_update_repo(input_data.repo_url, depth=0, token=input_data.github_token)

            # Extract repo_name from repo_url for git fame
            _, repo_name = parse_repo_url(input_data.repo_url)

            # Then run git fame
            result = await run_git_fame(repo_name, input_data.exclusions)
        except FileNotFoundError as e:
            log.error(f"Repository not found: {str(e)}")
            raise HTTPException(status_code=404, detail="Repository not found")
        except subprocess.CalledProcessError as e:
            log.error(f"Error running git fame: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to run git fame: {e.stderr}")
        except Exception as e:
            log.error(f"Unexpected error during git fame analysis: {str(e)}")
            raise HTTPException(status_code=500, detail="Unexpected error during git fame analysis")

        log.info("Git fame analysis completed successfully")
        response_message = ResponseMessageModel(message=result)
        return OutputModel(invocationId=invocation_id, response=[response_message])
    
    
    @app.post("/system/github/analyze/invoke")
    async def analyze_repo(request: Request) -> OutputModel:
        """
        Handle POST requests for running various analysis tools on a cloned GitHub repository.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the analysis operation fails.

        Example:
            >>> client = TestClient(app)
            >>> response = client.post("/system/github/analyze/invoke", 
            ...     json={
            ...         "repo_url": "https://github.com/user/repo",
            ...         "analysis_tools": ["fame", "pylint"],
            ...         "target_path": "app/routes/github",
            ...         "exclusions": ["*.md"]
            ...     })
            >>> response.status_code
            200
        """
        log.info("Received request for repository analysis")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.info(f"Received input data: {data}")
            input_data = RepoAnalysisInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            # First, ensure the repository is cloned and up-to-date
            log.info(f"Cloning or updating repository: {input_data.repo_url}")
            await clone_or_update_repo(input_data.repo_url, depth=0, token=input_data.github_token)

            # Extract repo_name from repo_url for analysis
            _, repo_name = parse_repo_url(input_data.repo_url)
            repo_path = BASE_CLONE_DIR / repo_name
            log.info(f"Repository path: {repo_path}")

            # Run each specified analysis tool
            results = []
            for tool in input_data.analysis_tools:
                log.info(f"Running analysis tool: {tool}")
                try:
                    result = await run_analysis_tool(repo_path, tool, input_data.target_path, input_data.exclusions)
                    results.append(result)
                except ValueError as e:
                    log.error(f"Error with {tool}: {str(e)}")
                    results.append(f"Error with {tool}: {str(e)}")
                except subprocess.CalledProcessError as e:
                    log.error(f"Error running {tool}: {e.stderr}")
                    results.append(f"Error running {tool}: {e.stderr}")

            final_result = "\n\n".join(results)

        except FileNotFoundError as e:
            log.error(f"Repository not found: {str(e)}")
            raise HTTPException(status_code=404, detail="Repository not found")
        except Exception as e:
            log.error(f"Unexpected error during repository analysis: {str(e)}")
            raise HTTPException(status_code=500, detail="Unexpected error during repository analysis")

        log.info("Repository analysis completed successfully")
        response_message = ResponseMessageModel(message=final_result)
        return OutputModel(invocationId=invocation_id, response=[response_message])