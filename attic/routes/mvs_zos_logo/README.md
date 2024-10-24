# MVS/z/OS Logo Generator Integration

This integration provides services for generating custom logos for MVS and z/OS systems in assembly language format.

## Endpoints

- POST /system/mvs_zos_logo/generate/invoke
  Invokes the System API to generate assembly code for a custom logo based on input text.

- POST /experience/mvs_zos_logo/generate_creative/invoke
  Invokes the Experience API to generate a creative logo based on a theme, using an LLM, and then converts it to assembly code.

## Testing the integration locally

### Generate Logo - System API

This endpoint allows you to generate assembly code for a custom logo.

```bash
curl --location --request POST \
    'http://localhost:8080/system/mvs_zos_logo/generate/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "logo_text": "MVS\nLOGO",
        "start_line": 7,
        "start_column": 15
    }'
```

### Generate Creative Logo - Experience API

This endpoint allows you to generate a creative logo based on a theme and get the corresponding assembly code.

```bash
curl --location --request POST \
    'http://localhost:8080/experience/mvs_zos_logo/generate_creative/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "theme": "Sidekick"
    }'
```

## Note

This integration generates assembly language code for displaying custom logos on MVS and z/OS systems. The creative logo generation feature uses an LLM to create a logo based on a given theme.
