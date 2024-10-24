# autogen_newsletter_generator Integration

> Author: Stan Furrer, Dennis Weiss

This module implements an `autogen` nested group chat using three other integration.

-   `autogen_translator`: Translate a text in `languageFrom` to `languageTo`.
-   `autogen_email`: Given a text, generate an Email.
-   `autogen_websurfer`: Given a URL surfe and scrape for specific informations.

It generate and send by email a newsletter given `language`, `industryOfInterest`, `email`.

## API Endpoints

### POST /autogen_newslettre_generator/result

Given `language`, `industryOfInterest`, `email`, send newletter about `industryOfInterest` in language `language` via email to `email`.

```bash
curl -X POST "http://localhost:8080/autogen_newslettre_generator/result" \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{
      "language": "English",
      "industryOfInterest": "Banks",
      "email": "user-user@ibm.com"
      }'
```

```json
{
    "status": "success",
    "invocationId": "f922884f-e388-4415-9595-f1f5e35a3115",
    "response": [
        {
            "message": "Dear Participant, here is the news ... Best Regards, IBM Consulting assistant.",
            "type": "text"
        }
    ]
}
```
