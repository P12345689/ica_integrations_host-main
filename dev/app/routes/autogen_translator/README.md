# autogen_translator Integration

> Author: Dennis Weiss, Max Belitsky, Stan Furrer, Alexandre Carlhammar

This module implements an `autogen` nested group chat using a translator and a critic to translate a text in `languageFrom` to `languageTo`. The *translator-critic architecture* have been inspired by Andrew Ng's [translation agent](https://github.com/andrewyng/translation-agent).

## API Endpoints

### POST /autogen_translator/result

Given a text in language `languageFrom`, translate it to `languageTo`.

```bash
curl -X POST "http://localhost:8080/autogen_translator/result" \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "text": "This is just some sample text, which we want to translate.",
      "languageFrom": "English",
      "languageTo": "Portuguese"
      }'
```

```json
{
    "status": "success",
    "invocationId": "f922884f-e388-4415-9595-f1f5e35a3115",
    "response": [
        {
            "message": "This is the text translated to Portuguese:\n\n\"Este é apenas um texto de amostra, que queremos traduzir.\"",
            "type": "text"
        }
    ]
}
```
