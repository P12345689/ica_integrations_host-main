# File Upload Integration

> Author: Mihai Criveti

This integration provides a file management system with a REST API and web interface.
It allows users to generate upload URLs, upload files, manage their files, and ask questions about their uploaded files using a language model.

## Features

- Generate unique upload URLs based on team ID and user email
- Upload files securely
- List, download, and delete files
- Ask questions about uploaded files using natural language
- Simple and intuitive web interface

## Setup

1. Ensure you have Python 3.7+ installed.

2. Install the required dependencies:
   ```
   pip install fastapi uvicorn jinja2 python-multipart python-dotenv
   ```

3. Set up the project structure as follows:
   ```
   /
   ├── README.md
   ├── app/
   │   └── routes/
   │       └── file_upload/
   │           ├── file_upload_router.py
   │           ├── templates/
   │           │   ├── file_upload_ui.html
   │           │   ├── file_query_prompt.jinja
   │           │   └── file_query_response.jinja
   │           ├── static/
   │           │   ├── styles.css
   │           │   └── script.js
   │           └── tools/
   │               └── file_upload_tool.py
   ├── public/
   │   └── userfiles/
   └── main.py
   ```

4. Create a `.env` file in the root directory and add the following variables:
   ```
   BASE_URL=http://localhost:8080
   ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME=Llama3.1 70b Instruct
   DEFAULT_MAX_THREADS=4
   ICA_AUTH_TOKENS=dev-only-token
   ```

5. Update your `main.py` file to include the file upload routes:
   ```python
   from fastapi import FastAPI
   from app.routes.file_upload.file_upload_router import add_custom_routes

   app = FastAPI()

   add_custom_routes(app)
   ```

6. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

## Usage

### Web Interface

Access the web interface by navigating to `http://localhost:8080/file_upload_ui` in your web browser. From there, you can:

1. Generate upload URLs
2. Upload files
3. List, download, and delete files
4. Ask questions about your files

### API Endpoints

You can also interact with the integration programmatically using the following API endpoints:

- POST /system/file_upload/retrievers/get_upload_url/invoke
  Generates and returns a link to the user interface and the user hash.
  It expects a JSON payload with a `team_id` and `user_email`.


- POST /system/file_upload/upload
  Uploads a selected file in `public/userfiles`.
  It expects a JSON payload with a `team_id`, `user_email`, `key` (represents the user hash) and `file_path`.


- GET /system/file_upload/list?key={USER_HASH}&team_id={TEAM_ID}&user_email={USER_EMAIL}
  Lists all files uploaded by the user.
  It expects query parameters with a `key` (represents the user hash), `team_id` and `user_email`.


- DELETE /system/file_upload/delete/{FILE_NAME}?key={USER_HASH}&team_id={TEAM_ID}&user_email={USER_EMAIL}
  Deletes a file uploaded in `public/userfiles` by the user.
  It expects query parameters with a `key` (represents the user hash), `team_id` and `user_email` and a URL parameter with a `file_name`.


- GET /system/file_upload/download/{FILE_NAME}?key={USER_HASH}&team_id={TEAM_ID}&user_email={USER_EMAIL}
  Deletes a file uploaded in `public/userfiles` by the user.
  It expects query parameters with a `key` (represents the user hash), `team_id` and `user_email` and a URL parameter with a `file_name`.


- POST /experience/file_upload/ask_about_files/invoke
  Invokes the ICA client to read file names and information.
  It expects a JSON payload with a `team_id`, `user_email` and `query`.

### Generate Upload URL

This endpoint also generates and displays the user's hash.

```bash
curl --location --request POST \
    'http://localhost:8080/system/file_upload/retrievers/get_upload_url/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "team_id": "team123",
        "user_email": "user@example.com"
    }'
```

### Upload File

```bash
curl --location --request POST \
    'http://localhost:8080/system/file_upload/upload' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "team_id": "team123",
        "user_email": "user@example.com",
        "key": "4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa",
        "file_path": "README.md"
    }'
```

Replace the `key` field with the hash generated from the team ID and user email (displayed when running Generate Upload URL cURL).

### List Files

```bash
curl --location --request GET \
    'http://localhost:8080/system/file_upload/list?key=USER_HASH&team_id=TEAM_ID&user_email=USER_EMAIL' \
    --header 'Integrations-API-Key: dev-only-token'
```

Replace the `key`, `team_id` and `user_email` placeholders with the correct values. For example:

```bash
curl --location --request GET \
    'http://localhost:8080/system/file_upload/list?key=4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa&team_id=team123&user_email=user@example.com' \
    --header 'Integrations-API-Key: dev-only-token'
```

### Delete File

```bash
curl --location --request DELETE \
    'http://localhost:8080/system/file_upload/delete/FILE_NAME?key=USER_HASH&team_id=TEAM_ID&user_email=USER_EMAIL' \
    --header 'Integrations-API-Key: dev-only-token'
```

### Download File

```bash
curl --location --request GET \
    'http://localhost:8080/system/file_upload/download/FILE_NAME?key=USER_HASH&team_id=TEAM_ID&user_email=USER_EMAIL' \
    --header 'Integrations-API-Key: dev-only-token'
```

### Ask About Files

```bash
curl --location --request POST \
    'http://localhost:8080/experience/file_upload/ask_about_files/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data '{
        "team_id": "team123",
        "user_email": "user@example.com",
        "query": "What files do I have?"
    }'
```

## Security Considerations

- This integration uses a simple token-based authentication system.
- Ensure that the `public/userfiles` directory is properly secured and not directly browsable.
- Implement rate limiting and file size restrictions to prevent abuse.
- Implement a file expiration mechanism, to delete files every *n* hours.

## Customization

You can customize this integration by:

- Modifying the `file_upload_ui.html` template to change the user interface.
- Updating the `styles.css` file to alter the appearance of the web interface.
- Extending the `file_upload_router.py` to add new features or endpoints.
- Adjusting the `script.js` file to modify the client-side behavior.
