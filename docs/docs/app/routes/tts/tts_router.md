# Tts Router

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Tts](./index.md#tts) / Tts Router

> Auto-generated documentation for [app.routes.tts.tts_router](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py) module.

#### Attributes

- `SERVER_NAME` - Load the server URL from an environment variable (localhost or remote): os.getenv('SERVER_NAME', 'http://127.0.0.1:8080')

- `template_env` - Load Jinja2 environment: Environment(loader=FileSystemLoader('app/routes/tts/templates'))


- [Tts Router](#tts-router)
  - [AudioFormatEnum](#audioformatenum)
  - [OutputModel](#outputmodel)
  - [ResponseMessageModel](#responsemessagemodel)
  - [SpecificVoiceInputModel](#specificvoiceinputmodel)
  - [TTSInputModel](#ttsinputmodel)
  - [Voice](#voice)
  - [VoiceFeatures](#voicefeatures)
  - [VoiceListResponse](#voicelistresponse)
  - [add_custom_routes](#add_custom_routes)
  - [generate_speech](#generate_speech)
  - [get_specific_voice](#get_specific_voice)
  - [list_voices](#list_voices)

## AudioFormatEnum

[Show source in tts_router.py:48](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L48)

#### Signature

```python
class AudioFormatEnum(str, Enum): ...
```



## OutputModel

[Show source in tts_router.py:100](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L100)

Model to structure the output response.

#### Signature

```python
class OutputModel(BaseModel): ...
```



## ResponseMessageModel

[Show source in tts_router.py:95](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L95)

Model to validate the response message.

#### Signature

```python
class ResponseMessageModel(BaseModel): ...
```



## SpecificVoiceInputModel

[Show source in tts_router.py:90](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L90)

Model to validate input data for getting a specific voice.

#### Signature

```python
class SpecificVoiceInputModel(BaseModel): ...
```



## TTSInputModel

[Show source in tts_router.py:82](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L82)

Model to validate input data for text-to-speech conversion.

#### Signature

```python
class TTSInputModel(BaseModel): ...
```



## Voice

[Show source in tts_router.py:68](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L68)

Model for voice information.

#### Signature

```python
class Voice(BaseModel): ...
```



## VoiceFeatures

[Show source in tts_router.py:63](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L63)

Model for voice features.

#### Signature

```python
class VoiceFeatures(BaseModel): ...
```



## VoiceListResponse

[Show source in tts_router.py:78](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L78)

Model for the response of listing all voices.

#### Signature

```python
class VoiceListResponse(BaseModel): ...
```



## add_custom_routes

[Show source in tts_router.py:235](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L235)

#### Signature

```python
def add_custom_routes(app: FastAPI) -> None: ...
```



## generate_speech

[Show source in tts_router.py:179](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L179)

Generate speech from text using the specified voice and format.

#### Arguments

- `text` *str* - The text to convert to speech.
- `voice` *str* - The voice to use for speech synthesis.
- `format` *AudioFormatEnum* - The audio format for the output file.
- `rate` *Optional[int]* - The sampling rate for the audio (where applicable).
- `endianness` *Optional[str]* - The endianness for audio/l16 format.

#### Returns

- `str` - The filename of the generated audio file.

#### Raises

- `HTTPException` - If there's an error in the API call or file saving process.

#### Signature

```python
async def generate_speech(
    text: str,
    voice: str,
    format: AudioFormatEnum,
    rate: Optional[int] = None,
    endianness: Optional[str] = None,
) -> str: ...
```

#### See also

- [AudioFormatEnum](#audioformatenum)



## get_specific_voice

[Show source in tts_router.py:138](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L138)

Get information about a specific voice.

#### Arguments

- `voice` *str* - The name of the voice to get information about.
- `customization_id` *Optional[str]* - The GUID of a custom model.

#### Returns

- [Voice](#voice) - Information about the specified voice.

#### Raises

- `HTTPException` - If there's an error in the API call.

#### Signature

```python
async def get_specific_voice(
    voice: str, customization_id: Optional[str] = None
) -> Voice: ...
```

#### See also

- [Voice](#voice)



## list_voices

[Show source in tts_router.py:106](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/tts/tts_router.py#L106)

List all available voices.

#### Returns

- [VoiceListResponse](#voicelistresponse) - The list of all available voices.

#### Raises

- `HTTPException` - If there's an error in the API call.

#### Signature

```python
async def list_voices() -> VoiceListResponse: ...
```

#### See also

- [VoiceListResponse](#voicelistresponse)
