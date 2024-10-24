# Mermaid Diagram

> Author: Chris Hay, Mihai Criveti

This is a Mermaid diagram agent that can be used with integrations in sidekick to visualize data structures and relationships.

## Environment Variables

The following environment variables are used in the Mermaid integration:

- `MERMAID_API_URL`: The URL of the Mermaid API endpoint. Defaults to "https://mermaid.ink".

Before running the application, make sure to set these environment variables in your shell or using a `.env` file. Here's an example:

```bash
export MERMAID_API_URL="https://your-mermaid-api-url"
```

## Endpoints

- ### POST /experience/mermaid/transformers/text_to_image/invoke
  Invokes the experience API to create diagrams. It expects a JSON payload with the query, chart type, style, and direction.

- ### POST /experience/mermaid_service/transformers/text_to_syntax/invoke
  Invokes the experience API to convert natural language to Mermaid syntax. It expects a JSON payload with the query, chart type, style, and direction.

- ### POST /system/mermaid_service/transformers/syntax_to_image/invoke
  Invokes the system API to transform Mermaid syntax to an image. It expects a JSON payload with the Mermaid syntax.

## Testing the Integration Locally

### Organization Chart

To create an organization chart, run the following command:

```bash
curl --request POST "http://localhost:8080/experience/mermaid/transformers/text_to_image/invoke" \
     --header "Content-Type: application/json" \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
           "query": "My (Suman) manager is Abantika and her manager is Svayambhu, my reportee is Gunjan and Projit.",
           "chart_type": "org chart",
           "style": "",
           "direction": ""
         }'
```

### Sequence Diagram

To generate a sequence diagram, run the following command:

```bash
curl --request POST "http://localhost:8080/experience/mermaid/transformers/text_to_image/invoke" \
     --header "Content-Type: application/json" \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
           "query": "shows the interactions between a user and a ticket booking system in booking a seat.",
           "chart_type": "sequence diagram",
           "style": "",
           "direction": ""
         }'
```

### Class Diagram

To generate a class diagram, run the following command:

```bash
curl --request POST "http://localhost:8080/experience/mermaid/transformers/text_to_image/invoke" \
     --header "Content-Type: application/json" \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
           "query": "a person class including first name, last name, dob",
           "chart_type": "class diagram",
           "style": "",
           "direction": ""
         }'
```

### Mermaid Text to Syntax

To convert natural language to Mermaid syntax, run the following command:

```bash
curl --request POST "http://localhost:8080/experience/mermaid_service/transformers/text_to_syntax/invoke" \
     --header "Content-Type: application/json" \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
           "query": "a person class including first name, last name, dob",
           "chart_type": "class diagram",
           "style": "",
           "direction": ""
         }'
```

### Mermaid Syntax to Image

To transform Mermaid syntax to an image, run the following command:

```bash
curl --request POST "http://localhost:8080/system/mermaid_service/transformers/syntax_to_image/invoke" \
     --header "Content-Type: application/json" \
     --header "Integrations-API-Key: dev-only-token" \
     --data-raw '{
           "query": "sequenceDiagram\n    participant User\n    participant Ticket Booking System\n    User->>Ticket Booking System: Accesses booking system\n    Ticket Booking System->>User: Shows available shows\n    User->>Ticket Booking System: Selects a show\n    Ticket Booking System->>User: Shows available seats\n    User->>Ticket Booking System: Selects a seat\n    Ticket Booking System->>User: Confirms seat availability\n    User->>Ticket Booking System: Proceeds to payment\n    Ticket Booking System->>User: Confirms payment and books the seat\n"
         }'
```
