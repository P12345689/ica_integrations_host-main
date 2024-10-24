---
classification: confidential #Remove this line if it's not IBM Confidential.
status: draft #Status can be draft, reviewed or published.
owner: Mihai Criveti
tags:
    - tutorials
contributors:
reviewers:
---

# Developing your first integration

## Register as a new integration developer

Message `@cmihai` and `@Chris Hay` in the [#assistants-integrations-developers](https://ibm.enterprise.slack.com/archives/C074Y1TMTBK) Slack Channel to register as a new integration developer, or submit a GitHub Issue.

> Note: If you are using a 🪟 Windows Operating System, please make sure first to [install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).
> Powershell/CMD terminals are currently **not** supported.

## Setup libica

First, [install](https://pages.github.ibm.com/destiny/consulting_assistants_api/#installation) and [configure](https://pages.github.ibm.com/destiny/consulting_assistants_api/#configuration) `libica`.

## Download and install `ica_integrations_host`

```bash
git clone git@github.ibm.com:destiny/ica_integrations_host.git # or
git clone https://github.ibm.com/destiny/ica_integrations_host
cd ica_integrations_host
make venv install   # Create a Python venv and install dependencies
make activate       # Get Python venv activate script
. ~/.venv/ica_integrations_host/bin/activate  # Activate your venv.
python3 -m pip install ".[libica_local]"
```

## Test that it's working

Start the FastAPI server using `uvicorn`.
```bash
export ICA_AUTH_TOKENS="dev-only-token"  # Token for authentication to ica_container_host
export ICA_DEV_ROUTES=1                     # Enable development routes
uvicorn app.server:app --host 0.0.0.0 --port 8080 --reload
```

In a new *terminal* window, connect to the REST API using `curl` or a similar client:
=== "command"
    ```bash
    curl --silent \
        --request POST http://localhost:8080/system/wikipedia/retrievers/search/invoke \
        --header "Content-Type: application/json" \
        --header "Integrations-API-Key: dev-only-token" \
        --data-raw '{"search_string": "Python programming", "results_type": "summary" }' | jq
    ```
=== "output"
    The `ica_container_host` REST API will return JSON, in the format required by Integrations. Notice the `status` is `success`, the `response` format includes a `message` of type `text`, and also notice a unique `invocationId` is generated every time you query the API.

    ```json
    {
        "status": "success",
        "response": [
            {
            "message": "Python is a high-level, general-purpose programming language...\n\nSource: [Wikipedia page for Python (programming language)](<https://en.wikipedia.org/wiki/Python_(programming_language)>)",
            "type": "text"
            },
            {
            "message": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/500px-Python-logo-notext.svg.png",
            "type": "image"
            }
        ],
        "invocationId": "8b954ae3-abf5-4756-a906-188175e15f62"
    }
    ```

=== "logs"
    On the terminal where you have started `uvicorn` you should observe requests being made by `ica_container_host` to the Wikipedia API, followed by a  a `200 OK` displayed in the server logs - as the request is being returned to the client.

    ```
    INFO:httpx:HTTP Request: GET https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&utf8=1&srlimit=5&srsearch=Python%20programming "HTTP/1.1 200 OK"
    INFO:httpx:HTTP Request: GET https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts%7Cpageimages&pageids=23862&explaintext=true&exlimit=1&pithumbsize=500&exintro=true "HTTP/1.1 200 OK"
    INFO:     127.0.0.1:35724 - "POST /system/wikipedia/retrievers/search/invoke HTTP/1.1" 200 OK
    ```

???+ tip "Tips"
    - You can define any ICA_AUTH_TOKENS value, and match it in the request `Integrations-API-Key` header.
    - You can generate a secure string for use in production using `python -c "import uuid; print(uuid.uuid4())"`
    - You don't need to use `| jq` if you don't have it installed, it's used to format the result (pretty print the JSON). You can install `jq` on MacOS with `brew install jq`, on Linux with `apt install jq` or `yum install jq` on Debian/Ubuntu and Red Hat distributions respectively.


## Test that the extension API also works

Check that integrations connect to ICA. The joke route uses `langchain_consultingassistants` to generate a joke based on a topic using a large language model. This tests that everything works well:

=== "command"
    ```bash
    curl --silent --location \
        --request POST 'http://localhost:8080/experience/joke/retrievers/get_joke/invoke' \
        --header 'Content-Type: application/json' \
        --header 'Integrations-API-Key: dev-only-token' \
        --data-raw '{"topic": "cats"}'
    ```

=== "output"
    ```json
    {
        "status": "success",
        "invocationId": "e8ebbcb4-a08c-43be-97ee-b7fd7c4c6116",
        "response": [
            {
            "message": "Of course, I'd be happy to! Here's one for you: Why did the cat sit on the keyboard? Because he wanted to type faster! But then he realized that keyboards are only good for sleeping on. *wink*\n\nI hope this brought a smile to your face! If you have any other requests or need assistance with something else, feel free to let me know.",
            "type": "text"
            }
        ]
    }
    ```

=== "logs"
    ```
    INFO:     127.0.0.1:38454 - "POST /experience/joke/retrievers/get_joke/invoke HTTP/1.1" 200 OK
    ```

## Create a new integration

The `make integration` command will generate the boilerplate for a new integration, and add it to the development routes in `./dev/`.

=== "command"
    ```bash
    make integration
    ```

=== "output"
    ```
    Welcome to the IBM Consulting Assistants Integration Builder

    🔨 This tool helps you forge new integrations!

    For more information, see Developing Integrations: 🧑‍💻
    https://pages.github.ibm.com/destiny/consulting_assistants_api/develop/developing_integrations/

    Remember to use the naming convention: my_route

    All new routes are copied to dev/routes instead of app/route. Once they are ready and pass unit testing,
    the process to move them to app/routes can start (includes an architecture and code review).

    Remember to start the server with ICA_DEV_ROUTES=1 to enable development routes.

    2024-05-22 08:39:45,530 - INFO - Starting module generation process...
    [1/4] module_name (example_module): my_integration
    [2/4] module_description (Detailed description of your integration): Detailed description
    [3/4] module_author (Name of the author):
    [4/4] module_email (example@email.com):
    2024-05-22 08:39:53,609 - INFO - Module 'my_integration' successfully copied to dev/app/routes/.
    ```

Make edits to your integration in `dev/app/routes/`. Do not change other routes or code.

### Develop your integration

=== "example_module_router.py"

    ```python
    import json
    import logging
    from typing import List, Any, Dict, Literal
    from uuid import uuid4

    from fastapi import FastAPI, HTTPException, Request
    from libica import ICAClient
    from pydantic import BaseModel, Field, ValidationError
    from typing_extensions import Annotated
    from jinja2 import Environment, FileSystemLoader

    log = logging.getLogger(__name__)

    DEFAULT_MODEL = "Llama3 70B Instruct"

    # Load Jinja2 environment
    template_env = Environment(loader=FileSystemLoader("app/routes/assistant_reviewer/templates"))
    log.info("Jinja2 environment initialized with template directory.")


    class InputModel(BaseModel):
        """Model to validate input data."""

        user_input: str

    class LLMResponseModel(BaseModel):
        """Model to structure the LLM response data."""

        requestType: str
        requestData: Dict[str, Any]
        curlCommand: str
        llmResponse: str


    class ResponseMessageModel(BaseModel):
        """Model to validate the response message."""

        message: str
        type: Literal["text", "image"]


    class OutputModel(BaseModel):
        """Model to structure the output response."""

        status: str = Field(default="success")
        invocationId: str
        response: Annotated[List[ResponseMessageModel], Field(min_length=1)]


    def add_custom_routes(app: FastAPI) -> None:
        """Add custom routes to the FastAPI app.

        Args:
            app (FastAPI): The FastAPI application instance.

        Example:
            >>> from fastapi.testclient import TestClient
            >>> app = FastAPI()
            >>> add_custom_routes(app)
            >>> client = TestClient(app)
            >>> response = client.post("/example_module/invoke", json={"model": "test_model", "prompt": "Hello"})
            >>> response.status_code
            200
            >>> response.json()["status"]
            'success'
        """

        @app.api_route("/example_module/invoke", methods=["POST"])
        async def example_module(request: Request) -> OutputModel:
            """Handle POST requests to the invoke endpoint.

            Args:
                request (Request): The request object containing the input data.

            Returns:
                OutputModel: The structured output response.

            Raises:
                HTTPException: If the JSON is invalid or if validation fails.
            """
            # get the type of request
            request_type = request.method
            log.debug(f"Received {request_type}")

            # get the data
            try:
                data = await request.json()
                input_data = InputModel(**data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON")
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=e.errors())

            # Load and render the prompt template using Jinja2 template
            template = template_env.get_template("prompt_template.jinja")
            rendered_input = template.render(user_input=input_data.user_input)

            # instantiate the LLM client and get the response if it's a POST request
            if request_type == "POST":
                consulting_assistants_model = ICAClient()
                llm_response = consulting_assistants_model.prompt_flow(
                    model_id_or_name=DEFAULT_MODEL, prompt=rendered_input
                )

            if llm_response is None:
                llm_response = "No response from LLM"


            # Load and render the response using Jinja2 template
            template = template_env.get_template("response_template.jinja")
            rendered_response = template.render(llm_response=llm_response)

            # Return the response
            invocation_id = str(uuid4())  # Generate a unique invocation ID
            response_dict = ResponseMessageModel(message=rendered_response, type="text")

            response_data = OutputModel(
                invocationId = invocation_id,
                response = [response_dict]
            )

            return response_data
    ```


=== "templates/response_template.jinja"
    ```jinja
    Received the following LLM Response:

    {{ llm_response }}
    ```

## Submitting a PR

1. Register as a new Integration developer.
2. Include a README.md
3. Do **NOT** include any keys hardcoded in your code, or in the README file.
4. Always run unit tests with `make unittest`.
5. Test all other paths using the available README.
6. Ensure there are no side effects or dependency issues, provide a separate `pyproject.toml` group for your integration, ex: `route_myintegration`.
7. Schedule a [Car Wash session](https://pages.github.ibm.com/destiny/consulting_assistants_api/design/architecture-decisions/) to present your integration.
