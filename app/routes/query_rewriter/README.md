# Query Rewriter

> Author: Mihai Criveti, adapted by Matt Colman

This module handles the routing for query_rewriter.

Generates assistants from provided description.

## Endpoints

- **POST /query_rewriter/invoke**
  Invokes the prompt builder process. It expects a JSON payload with a text `input`.


## Testing the integration locally

```bash
curl --silent --location --request POST 'http://localhost:8080/query_rewriter/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{ "input": "Summarise the purpose of OWASP ASVS" }' | jq
```

To format the response nicely:

```bash
curl --silent --location --request POST 'http://localhost:8080/query_rewriter/invoke' \
  --header 'Content-Type: application/json' \
  --header 'Integrations-API-Key: dev-only-token' \
  --data-raw '{ "input": "Summarise the purpose of OWASP ASVS" }' \
  | jq -r '.response[].message | gsub("\\n"; "\n")'
```

### Example Result

```json
{
  "status": "success",
  "response": [
    {
      "message": "**Summarize the Purpose of OWASP ASVS**\n=====================================\n\nPlease provide a concise summary of the primary objective and key aspects of the OWASP Application Security Verification Standard (ASVS). \n\nIn your response, use the following format:\n\n* Use headings to separate main sections\n* Utilize bold text to highlight important terms or concepts\n* Include a brief overview of the ASVS and its purpose\n* List the key aspects of the standard using bullet points or a.\n\n## Example Responses\n\n**Example #1**\n===============\n\n**Overview of OWASP ASVS**\n-------------------------\n\nThe **OWASP Application Security Verification Standard (ASVS)** is a comprehensive standard for web application security testing. Its primary objective is to provide a basis for testing web applications to ensure they are secure and compliant with industry standards.\n\n**Key Aspects of ASVS**\n-----------------------\n\n* **Verification**: ASVS focuses on verifying the security of web applications through a set of requirements and tests.\n* **Application Security**: The standard specifically targets web application security, covering aspects such as authentication, authorization, and data protection.\n* **Level-Based Approach**: ASVS uses a level-based approach, with three levels of verification: Level 1 (basic), Level 2 (standard), and Level 3 (advanced).\n* **Comprehensive Requirements**: The standard includes a comprehensive set of requirements covering security controls, data validation, and error handling.\n\n**Example #2**\n===============\n\n**Introduction to OWASP ASVS**\n-----------------------------\n\nThe **OWASP Application Security Verification Standard (ASVS)** is an open-source standard for web application security. Its main purpose is to provide a framework for ensuring the security and integrity of web applications.\n\n**Primary Objectives**\n--------------------\n\n* **Improve Web Application Security**: ASVS aims to improve the overall security posture of web applications by providing a set of security requirements and testing guidelines.\n* **Provide a Framework for Testing**: The standard offers a framework for testing web applications, enabling organizations to identify and address security vulnerabilities.\n\n**Key Components**\n------------------\n\n| Component | Description |\n| --- | --- |\n| **Verification Requirements** | A set of requirements for verifying the security of web applications. |\n| **Testing Guidelines** | Guidelines for testing web applications against the verification requirements. |\n| **Security Controls** | A set of security controls for protecting web applications against common threats. |\n\n## Further instructions:\n\nWait for the user input before replying. Adapt the example and prompt to whatever the user input request is.",
      "type": "text"
    }
  ],
  "invocationId": "a7c292ae-75d5-4b33-bc11-2168cbb9232a"
}
```
