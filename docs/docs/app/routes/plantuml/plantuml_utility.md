# Plantuml Utility

[ica_integrations_host Index](../../../README.md#ica_integrations_host-index) / [App](../../index.md#app) / [Routes](../index.md#routes) / [Plantuml](./index.md#plantuml) / Plantuml Utility

> Auto-generated documentation for [app.routes.plantuml.plantuml_utility](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_utility.py) module.

#### Attributes

- `plantuml_alphabet` - Useful lambdas: string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'

- `PLANTUML_IMAGE_TYPE` - Server names: os.getenv('PLANTUML_IMAGE_TYPE', 'png')


- [Plantuml Utility](#plantuml-utility)
  - [decode_plantuml](#decode_plantuml)
  - [encode_plantuml](#encode_plantuml)
  - [generate_uml_image](#generate_uml_image)

## decode_plantuml

[Show source in plantuml_utility.py:61](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_utility.py#L61)

Decodes PlantUML text from base64 encoding and zlib compression.

#### Arguments

- `data` *str* - Encoded PlantUML text.

#### Returns

- `str` - Decoded PlantUML text.

#### Examples

```python
>>> decode_plantuml("SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd91m00")
'@startuml\nAlice -> Bob: Hello\n@enduml'
```

#### Signature

```python
def decode_plantuml(data: str) -> str: ...
```



## encode_plantuml

[Show source in plantuml_utility.py:42](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_utility.py#L42)

Encodes PlantUML text using zlib compression and base64 encoding.

#### Arguments

- `data` *str* - PlantUML text to encode.

#### Returns

- `str` - Encoded PlantUML text.

#### Examples

```python
>>> encode_plantuml("@startuml\nAlice -> Bob: Hello\n@enduml")
'SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd91m00'
```

#### Signature

```python
def encode_plantuml(data: str) -> str: ...
```



## generate_uml_image

[Show source in plantuml_utility.py:81](https://github.ibm.com/destiny/ica_integrations_host/blob/main/app/routes/plantuml/plantuml_utility.py#L81)

Generates a UML diagram from the provided description using a PlantUML server.

#### Arguments

- `description` *str* - The PlantUML description of the UML diagram.

#### Returns

- `str` - Filename of the generated image.

#### Raises

- `HTTPException` - If there is an error generating the UML diagram.

#### Examples

```python
>>> import asyncio
>>> filename = asyncio.run(generate_uml_image("@startuml\nAlice -> Bob: Hello\n@enduml"))
>>> print(filename)
uml_92f8d7a6-f0b5-4e2a-8d2d-1e9b9f4c6e3e.png
```

#### Signature

```python
async def generate_uml_image(description: str) -> str: ...
```
