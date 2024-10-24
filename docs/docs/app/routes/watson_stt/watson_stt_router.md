# Watson Stt Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Watson Stt](./index.md#watson-stt) / Watson Stt Router

> Auto-generated documentation for [app.routes.watson_stt.watson_stt_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py) module.

#### Attributes

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/watson_stt/templates'))


- [Watson Stt Router](#watson-stt-router)
  - [AudioFormatEnum](#audioformatenum)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [STTInputModel](#sttinputmodel)
    - [STTInputModel().validate_audio_url](#sttinputmodel()validate_audio_url)
  - [add_custom_routes](#add_custom_routes)
  - [download_file](#download_file)
  - [generate_llm_response](#generate_llm_response)
  - [transcribe_audio](#transcribe_audio)

## AudioFormatEnum

[Show source in watson_stt_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L48)

#### Signature

```python
class AudioFormatEnum(str, Enum): ...
```



## OutputModel

[Show source in watson_stt_router.py:79](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L79)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in watson_stt_router.py:74](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L74)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## STTInputModel

[Show source in watson_stt_router.py:56](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L56)

Model to validate input data for speech-to-text conversion.

#### Signature

```python
class STTInputModel(BaseModel): ...
```

### STTInputModel().validate_audio_url

[Show source in watson_stt_router.py:63](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L63)

#### Signature

```python
@validator("audio_url")
def validate_audio_url(cls, v): ...
```



## add_custom_routes

[Show source in watson_stt_router.py:226](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L226)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## download_file

[Show source in watson_stt_router.py:85](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L85)

Download a file from a URL and save it temporarily.

#### Arguments

- `url` *str* - The URL of the file to download.

#### Returns

- `tuple[str,` *str]* - A tuple containing the path to the temporary file and its content type.

#### Raises

- `HTTPException` - If there's an error downloading the file.

#### Signature

```python
async def download_file(url: str) -> tuple[str, str]: ...
```



## generate_llm_response

[Show source in watson_stt_router.py:184](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L184)

Generate a response using an LLM based on the transcript.

#### Arguments

- `transcript` *str* - The transcribed text.

#### Returns

- `str` - The LLM-generated response.

#### Raises

- `HTTPException` - If there's an error in the LLM API call.

#### Signature

```python
async def generate_llm_response(transcript: str) -> str: ...
```



## transcribe_audio

[Show source in watson_stt_router.py:122](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/watson_stt/watson_stt_router.py#L122)

Transcribe audio using the specified model and options.

#### Arguments

audio_file (Union[UploadFile, str]): The audio file to transcribe or path to the file.
- `content_type` *str* - The content type of the audio file.
- `model` *str* - The model to use for speech recognition.
- `timestamps` *bool* - Whether to include timestamps for each word.
- `max_alternatives` *int* - Maximum number of alternative transcripts.

#### Returns

- `dict` - The transcription results.

#### Raises

- `HTTPException` - If there's an error in the API call.

#### Signature

```python
async def transcribe_audio(
    audio_file: Union[UploadFile, str],
    content_type: str,
    model: str,
    timestamps: bool,
    max_alternatives: int,
) -> dict: ...
```
