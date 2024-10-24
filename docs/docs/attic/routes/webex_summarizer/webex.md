# Webex

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / `attic` / `routes` / [Webex Summarizer](./index.md#webex-summarizer) / Webex

> Auto-generated documentation for [attic.routes.webex_summarizer.webex](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/webex_summarizer/webex.py) module.

- [Webex](#webex)
  - [approximate_token_count](#approximate_token_count)
  - [download_transcript](#download_transcript)
  - [main](#main)
  - [summarize_call](#summarize_call)

## approximate_token_count

[Show source in webex.py:18](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/webex_summarizer/webex.py#L18)

#### Signature

```python
def approximate_token_count(text): ...
```



## download_transcript

[Show source in webex.py:24](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/webex_summarizer/webex.py#L24)

Download the latest meeting transcript within the specified date range.

#### Arguments

- `bearer_token` *str* - Bearer token for authentication.
- `from_date` *str* - Start date for fetching transcripts (YYYY-MM-DD).
- `to_date` *str* - End date for fetching transcripts (YYYY-MM-DD).
- `max_results` *int* - Maximum number of transcripts to fetch.

#### Returns

- `str` - Transcript text.

#### Signature

```python
def download_transcript(bearer_token, from_date, to_date, max_results): ...
```



## main

[Show source in webex.py:75](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/webex_summarizer/webex.py#L75)

#### Signature

```python
def main(): ...
```



## summarize_call

[Show source in webex.py:59](https://github.com/destiny/ica_integrations_host/blob/main/attic/routes/webex_summarizer/webex.py#L59)

Mockup function to process and display the call transcript.

#### Arguments

- `transcript` *str* - Transcript text to be processed.

#### Signature

```python
def summarize_call(transcript): ...
```
