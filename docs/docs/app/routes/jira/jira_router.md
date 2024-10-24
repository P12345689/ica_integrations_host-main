# Jira Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Jira](./index.md#jira) / Jira Router

> Auto-generated documentation for [app.routes.jira.jira_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py) module.

#### Attributes

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/jira/templates'))


- [Jira Router](#jira-router)
  - [JiraIssueInputModel](#jiraissueinputmodel)
  - [JiraIssueKeyModel](#jiraissuekeymodel)
  - [JiraQueryInputModel](#jiraqueryinputmodel)
  - [JiraSearchInputModel](#jirasearchinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [create_jira_issue](#create_jira_issue)
  - [create_jql_query](#create_jql_query)
  - [get_jira_client](#get_jira_client)
  - [get_jira_issue](#get_jira_issue)
  - [get_project_statuses](#get_project_statuses)
  - [search_jira_issues](#search_jira_issues)

## JiraIssueInputModel

[Show source in jira_router.py:45](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L45)

Model to validate input data for Jira issue creation.

#### Signature

```python
class JiraIssueInputModel(BaseModel): ...
```



## JiraIssueKeyModel

[Show source in jira_router.py:59](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L59)

Model to validate input data for retrieving a Jira issue.

#### Signature

```python
class JiraIssueKeyModel(BaseModel): ...
```



## JiraQueryInputModel

[Show source in jira_router.py:63](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L63)

Model to validate input data for Jira-related queries.

#### Signature

```python
class JiraQueryInputModel(BaseModel): ...
```



## JiraSearchInputModel

[Show source in jira_router.py:52](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L52)

Model to validate input data for Jira issue search.

#### Signature

```python
class JiraSearchInputModel(BaseModel): ...
```



## OutputModel

[Show source in jira_router.py:72](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L72)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in jira_router.py:67](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L67)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in jira_router.py:224](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L224)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## create_jira_issue

[Show source in jira_router.py:127](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L127)

Create a new Jira issue.

#### Arguments

- `issue_data` *JiraIssueInputModel* - The data for the new issue.

#### Returns

- `str` - The key of the created issue.

#### Raises

- `JIRAError` - If there's an error creating the issue.

#### Signature

```python
async def create_jira_issue(issue_data: JiraIssueInputModel) -> str: ...
```

#### See also

- [JiraIssueInputModel](#jiraissueinputmodel)



## create_jql_query

[Show source in jira_router.py:83](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L83)

Create a JQL query string with proper escaping.

#### Arguments

- `project_key` *str* - The project key to search in.
- `assignee` *Optional[str]* - The assignee's username or email.
- `status` *Optional[str]* - The status to filter by. If None, all statuses are included.

#### Returns

- `str` - A properly formatted JQL query string.

#### Signature

```python
def create_jql_query(
    project_key: str, assignee: Optional[str] = None, status: Optional[str] = None
) -> str: ...
```



## get_jira_client

[Show source in jira_router.py:78](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L78)

Create and return a JIRA client instance.

#### Signature

```python
async def get_jira_client() -> JIRA: ...
```



## get_jira_issue

[Show source in jira_router.py:192](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L192)

Retrieve information about a Jira issue.

#### Arguments

- `issue_key` *str* - The key of the issue to retrieve.

#### Returns

- `Dict[str,` *str]* - A dictionary containing issue information.

#### Raises

- `JIRAError` - If there's an error retrieving the issue.

#### Signature

```python
async def get_jira_issue(issue_key: str) -> Dict[str, str]: ...
```



## get_project_statuses

[Show source in jira_router.py:102](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L102)

Retrieve available status options for a given project.

#### Arguments

- `project_key` *str* - The key of the project to get statuses for.

#### Returns

- `List[str]` - A list of available status options.

#### Raises

- `JIRAError` - If there's an error retrieving the statuses.

#### Signature

```python
async def get_project_statuses(project_key: str) -> List[str]: ...
```



## search_jira_issues

[Show source in jira_router.py:157](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/jira/jira_router.py#L157)

Search for Jira issues using JQL.

#### Arguments

- `jql` *str* - The JQL query to search for issues.
- `max_results` *int, optional* - The maximum number of results to return. Defaults to 50.

#### Returns

- `List[Dict[str,` *str]]* - A list of dictionaries containing issue information.

#### Raises

- `JIRAError` - If there's an error searching for issues.

#### Signature

```python
async def search_jira_issues(
    jql: str, max_results: int = 50
) -> List[Dict[str, str]]: ...
```
