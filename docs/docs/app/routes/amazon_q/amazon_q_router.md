# Amazon Q Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Amazon Q](./index.md#amazon-q) / Amazon Q Router

> Auto-generated documentation for [app.routes.amazon_q.amazon_q_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py) module.

#### Attributes

- `log` - Setup logging: logging.getLogger(__name__)

- `DEFAULT_MAX_THREADS` - Load environment variables: int(os.getenv('DEFAULT_MAX_THREADS', 4))

- `CLIENT_ID` - Amazon Q Settings: os.getenv('AMAZON_Q_CLIENT_ID')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/amazon_q/templates'))


- [Amazon Q Router](#amazon-q-router)
  - [AmazonQInputModel](#amazonqinputmodel)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [add_custom_routes](#add_custom_routes)
  - [assume_role_with_token](#assume_role_with_token)
  - [get_iam_oidc_token](#get_iam_oidc_token)
  - [get_qclient](#get_qclient)
  - [initiate_auth](#initiate_auth)
  - [query_amazon_q](#query_amazon_q)

## AmazonQInputModel

[Show source in amazon_q_router.py:49](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L49)

Model to validate input data for Amazon Q queries.

#### Signature

```python
class AmazonQInputModel(BaseModel): ...
```



## OutputModel

[Show source in amazon_q_router.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L61)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in amazon_q_router.py:56](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L56)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## add_custom_routes

[Show source in amazon_q_router.py:213](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L213)

#### Signature

```python
def add_custom_routes(app: FastAPI): ...
```



## assume_role_with_token

[Show source in amazon_q_router.py:132](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L132)

Assume IAM role using the IAM OIDC token.

#### Arguments

- `iam_token` *str* - The IAM OIDC token.

#### Returns

- `dict` - The assumed role credentials.

#### Raises

- `HTTPException` - If role assumption fails.

#### Signature

```python
async def assume_role_with_token(iam_token: str) -> dict: ...
```



## get_iam_oidc_token

[Show source in amazon_q_router.py:106](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L106)

Exchange Cognito token for IAM OIDC token.

#### Arguments

- `id_token` *str* - The Cognito ID token.

#### Returns

- `str` - The IAM OIDC token.

#### Raises

- `HTTPException` - If token exchange fails.

#### Signature

```python
async def get_iam_oidc_token(id_token: str) -> str: ...
```



## get_qclient

[Show source in amazon_q_router.py:164](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L164)

Create an Amazon Q client using assumed role credentials.

#### Arguments

- `credentials` *dict* - The assumed role credentials.

#### Returns

- `boto3.client` - The Amazon Q client.

#### Raises

- `HTTPException` - If client creation fails.

#### Signature

```python
async def get_qclient(credentials: dict): ...
```



## initiate_auth

[Show source in amazon_q_router.py:67](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L67)

Initiate authentication with Amazon Cognito.

#### Arguments

- `username` *str* - The username for authentication.
- `password` *str* - The password for authentication.

#### Returns

- `dict` - The authentication response containing tokens.

#### Raises

- `HTTPException` - If authentication fails.

#### Signature

```python
async def initiate_auth(username: str, password: str) -> dict: ...
```



## query_amazon_q

[Show source in amazon_q_router.py:188](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/amazon_q/amazon_q_router.py#L188)

Send a query to Amazon Q and get the response.

#### Arguments

- `amazon_q` - The Amazon Q client.
- `query` *str* - The query to send to Amazon Q.

#### Returns

- `dict` - The response from Amazon Q.

#### Raises

- `HTTPException` - If the query fails.

#### Signature

```python
async def query_amazon_q(amazon_q, query: str) -> dict: ...
```
