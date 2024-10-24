# plantuml

> Author: Mihai Criveti

This module handles the routing for PlantUML, which efficiently create UML diagrams with PlantUML


## Endpoints

- ## /plantulm/invoke Invokes the plantulm API to create ULM diagrams.

- ## /system/plantuml/transformers/syntax_to_image/invoke Invokes the system API to transform a ULM diagram into an image.


## Testing the integration locally

### PlantUML API
This is an example of a PlantUML API to create an ULM diagram from text.

```bash
curl --silent --request POST \
     'http://localhost:8080/plantuml/invoke' \
     --header 'Content-Type: application/json' \
     --header 'Integrations-API-Key: dev-only-token' \
     --data '{
          "description": "@startuml\nAlice -> Bob: Hello Bob, how are you?\nBob --> Alice: I am fine, thanks!\n@enduml"
          }'
```

This is an example of a system API used to create an image of the ULM diagram from text.

```bash
curl --silent --request POST \
     'http://localhost:8080/system/plantuml/transformers/syntax_to_image/invoke' \
     --header "Content-Type: application/json" \
     --header 'Integrations-API-Key: dev-only-token' \
     --data '{
          "description": "@startuml\nAlice -> Bob: Hello Bob, how are you?\nBob --> Alice: I am fine, thanks!\n@enduml"
          }'
```
