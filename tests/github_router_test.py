# -*- coding: utf-8 -*-
"""
Pytest for github route.

Description: Tests github route.

Authors: Gytis Oziunas
"""

from base64 import b64decode, b64encode
from unittest.mock import MagicMock, patch

from github.Repository import Repository

from app.routes.github.github_router import github_operation


# Test list issues
@patch("app.routes.github.github_router.Github")
def test_github_operation_list_issues(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_issue1 = MagicMock()
    mock_issue1.title = "Test Issue 1"
    mock_issue1.number = 1
    mock_issue1.body = "Test Issue Body 1"
    mock_issue2 = MagicMock()
    mock_issue2.title = "Test Issue 2"
    mock_issue2.number = 2
    mock_issue2.body = "Test Issue Body 2"
    mock_repo.get_issues.return_value = [mock_issue1, mock_issue2]

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    repo_url = "https://github.com/user/repo"
    action = "list_issues"
    params = {}
    result = github_operation(token, repo_url, action, params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.get_issues.assert_called_once()
    assert "Test Issue 1" in result and "Test Issue 2" in result


# Test get issue
@patch("app.routes.github.github_router.Github")
def test_github_operation_get_issue(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_issue = MagicMock()
    mock_issue.title = "Test Issue"
    mock_issue.number = 1
    mock_issue.body = "Test Issue Body"
    mock_repo.get_issue.return_value = mock_issue

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    action = "get_issue"
    repo_url = "https://github.com/user/repo"
    params = {"issue_number": 1}
    result = github_operation(token, repo_url, action, params=params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.get_issue.assert_called_once()
    assert "Test Issue" in result


# Test create issue
@patch("app.routes.github.github_router.Github")
def test_github_operation_create_issue(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_issue = MagicMock()
    mock_repo.create_issue.return_value = mock_issue

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    action = "create_issue"
    repo_url = "https://github.com/user/repo"
    params = {"title": "New Test Issue", "body": "New Test Issue Body"}
    result = github_operation(token, repo_url, action, params=params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.create_issue.assert_called_once()
    assert "Issue created" in result


# Test list pull requests
@patch("app.routes.github.github_router.Github")
def test_github_operation_list_pull_requests(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_pr1 = MagicMock()
    mock_pr1.title = "Test PR 1"
    mock_pr1.number = 1
    mock_pr1.body = "Test PR Body 1"
    mock_pr2 = MagicMock()
    mock_pr2.title = "Test PR 2"
    mock_pr2.number = 2
    mock_pr2.body = "Test PR Body 2"
    mock_repo.get_pulls.return_value = [mock_pr1, mock_pr2]

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    repo_url = "https://github.com/user/repo"
    action = "list_prs"
    params = {}
    result = github_operation(token, repo_url, action, params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.get_pulls.assert_called_once()
    assert "Test PR 1" in result and "Test PR 2" in result


# Test get pull request
@patch("app.routes.github.github_router.Github")
def test_github_operation_get_pull_request(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_pr = MagicMock()
    mock_pr.title = "Test PR"
    mock_pr.number = 1
    mock_pr.body = "Test PR Body"
    mock_repo.get_pull.return_value = mock_pr

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    repo_url = "https://github.com/user/repo"
    action = "get_pr"
    params = {"pr_number": 1}
    result = github_operation(token, repo_url, action, params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.get_pull.assert_called_once()
    assert "Test PR" in result


# Test create pull request
@patch("app.routes.github.github_router.Github")
def test_github_operation_create_pull_request(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_pr = MagicMock()
    mock_repo.create_pull.return_value = mock_pr

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    repo_url = "https://github.com/user/repo"
    action = "create_pr"
    params = {
        "title": "New Test PR",
        "body": "New Test PR Body",
        "head": "feature-branch",
        "base": "main",
    }
    result = github_operation(token, repo_url, action, params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.create_pull.assert_called_once()
    assert "PR created" in result


# Test list releases


@patch("app.routes.github.github_router.Github")
def test_github_operation_list_releases(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_release1 = MagicMock()
    mock_release1.title = "Test Release 1"
    mock_release1.tag_name = "v1.0"
    mock_release1.body = "Test Release Body 1"
    mock_release2 = MagicMock()
    mock_release2.title = "Test Release 2"
    mock_release2.tag_name = "v2.0"
    mock_release2.body = "Test Release Body 2"
    mock_repo.get_releases.return_value = [mock_release1, mock_release2]

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    repo_url = "https://github.com/user/repo"
    action = "list_releases"
    params = {}
    result = github_operation(token, repo_url, action, params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.get_releases.assert_called_once()
    assert "Test Release 1" in result and "Test Release 2" in result


# Test create release
@patch("app.routes.github.github_router.Github")
def test_github_operation_create_release(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_release = MagicMock()
    mock_repo.create_git_release.return_value = mock_release

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    repo_url = "https://github.com/user/repo"
    action = "create_release"
    params = {
        "title": "New Test Release",
        "body": "New Test Release Body",
        "tag": "New-Release-Tag",
    }
    result = github_operation(token, repo_url, action, params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.create_git_release.assert_called_once()
    assert "Release created" in result


# Test get file content
@patch("app.routes.github.github_router.Github")
def test_github_operation_get_file_content(mock_github):
    # Mock repository and issues
    mock_repo = MagicMock(spec=Repository)
    mock_file = MagicMock()
    # mock file path and content. name file README.md
    mock_file.path = "path/to/README.md"
    mock_file.decoded_content = b64encode("Test File Content".encode()).decode()
    mock_file.decoded_content = b64decode(mock_file.decoded_content).decode()

    if isinstance(mock_file.decoded_content, str):
        mock_file.decoded_content = mock_file.decoded_content.encode()

    mock_repo.get_contents.return_value = mock_file

    # Configure the mock Github instance to return the mock repository
    mock_github.return_value.get_repo.return_value = mock_repo

    # Call the function under test
    token = "fake-token"
    repo_url = "https://github.com/user/repo"
    action = "get_file"
    params = {"path": "path/to/README.md"}
    result = github_operation(token, repo_url, action, params)

    # Assertions
    mock_github.assert_called_once_with(base_url="https://github.com/api/v3", login_or_token=token)
    mock_repo.get_contents.assert_called_once()
    assert "Test File Content" in result
