# Website Tools

[ica_integrations_host Index](../../../../README.md#ica_integrations_host-index) / `attic` / `routes` / [Website](../index.md#website) / [Tools](./index.md#tools) / Website Tools

> Auto-generated documentation for [attic.routes.website.tools.website_tools](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/website/tools/website_tools.py) module.

#### Attributes

- `log` - set the logger: logging.getLogger(__name__)


- [Website Tools](#website-tools)
  - [is_healthy](#is_healthy)
  - [is_healthy_async](#is_healthy_async)
  - [is_website_up](#is_website_up)
  - [is_website_up_async](#is_website_up_async)

## is_healthy

[Show source in website_tools.py:48](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/website/tools/website_tools.py#L48)

This tool will check the health endpoint of the given url.  It will check if the health endpoint returns OK

#### Signature

```python
@tool
def is_healthy(url: str) -> bool: ...
```



## is_healthy_async

[Show source in website_tools.py:59](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/website/tools/website_tools.py#L59)

This tool will check the health endpoint of the given url.  It will check if the health endpoint returns OK

#### Signature

```python
async def is_healthy_async(url: str) -> bool: ...
```



## is_website_up

[Show source in website_tools.py:18](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/website/tools/website_tools.py#L18)

This tool will check if the website is up and running for the passed in url.  It will only check if it returns a 200 response

#### Signature

```python
@tool
def is_website_up(url: str) -> bool: ...
```



## is_website_up_async

[Show source in website_tools.py:30](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/website/tools/website_tools.py#L30)

This tool will check if the website is up and running for the passed in url.  It will only check if it returns a 200 response

#### Signature

```python
async def is_website_up_async(url: str) -> bool: ...
```
