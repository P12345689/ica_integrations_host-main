# Wikipedia Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Wikipedia](./index.md#wikipedia) / Wikipedia Router

> Auto-generated documentation for [app.routes.wikipedia.wikipedia_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/wikipedia/wikipedia_router.py) module.

#### Attributes

- `settings` - Settings from pydantic: Settings()

- `log` - Configure logging: logging.getLogger(__name__)

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/wikipedia/templates'))


- [Wikipedia Router](#wikipedia-router)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [ResultsType](#resultstype)
  - [WikipediaSearchInput](#wikipediasearchinput)
  - [add_custom_routes](#add_custom_routes)
  - [search_wikipedia](#search_wikipedia)

## OutputModel

[Show source in wikipedia_router.py:70](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/wikipedia/wikipedia_router.py#L70)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in wikipedia_router.py:63](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/wikipedia/wikipedia_router.py#L63)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## ResultsType

[Show source in wikipedia_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/wikipedia/wikipedia_router.py#L48)

#### Signature

```python
class ResultsType(str, Enum): ...
```



## WikipediaSearchInput

[Show source in wikipedia_router.py:53](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/wikipedia/wikipedia_router.py#L53)

#### Signature

```python
class WikipediaSearchInput(BaseModel): ...
```



## add_custom_routes

[Show source in wikipedia_router.py:160](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/wikipedia/wikipedia_router.py#L160)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## search_wikipedia

[Show source in wikipedia_router.py:78](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/wikipedia/wikipedia_router.py#L78)

Asynchronously searches Wikipedia based on the specified input parameters and returns
formatted response data.

This function first performs a search query to identify relevant Wikipedia pages. If the
search results include disambiguation pages, it provides a list of potential relevant topics.
If a specific page is identified, it fetches a summary or the full content depending on
the `results_type` specified in `search_input`.

#### Arguments

- `search_input` *WikipediaSearchInput* - An instance of WikipediaSearchInput containing
                                     the search string and the desired type of results
                                     ('summary' or 'full').

#### Returns

- `Dict[str,` *Any]* - A dictionary containing the status of the operation and the response.
                The response may include text and/or an image URL. The text includes
                the content fetched from Wikipedia along with a source URL, and if
                available, an image URL associated with the page.

#### Raises

- `httpx.HTTPError` - If there is a problem with the network request.
- `json.JSONDecodeError` - If the response cannot be decoded from JSON.
- `Exception` - For other unforeseen errors that may occur during processing.

#### Signature

```python
async def search_wikipedia(search_input: WikipediaSearchInput) -> Dict[str, Any]: ...
```

#### See also

- [WikipediaSearchInput](#wikipediasearchinput)
