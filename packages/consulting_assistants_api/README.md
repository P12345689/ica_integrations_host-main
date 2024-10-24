# Assistants Extension & Integrations SDK 🤖🔧

[![Build Status](https://v3.travis.ibm.com/destiny/consulting_assistants_api.svg?token=E4rHUNHpL3GkBwESJgRP&branch=main)](https://v3.travis.ibm.com/destiny/consulting_assistants_api)
[![Python 3.9|3.10|3.11](images/python-3.11.svg)](https://www.python.org/downloads/release/python-3118/) [![Coverage Status](images/coverage.svg)](https://pages.github.ibm.com/destiny/consulting_assistants_api/coverage/) [![Pylint](images/pylint.svg)](https://pages.github.ibm.com/destiny/consulting_assistants_api/test/lint/) [![pyright checked](images/pyright-checked-blue.svg)](https://pages.github.ibm.com/destiny/consulting_assistants_api/test/lint/#linting-with-pyright) [![mypy checked](images/mypy-checked-blue.svg)](https://pages.github.ibm.com/destiny/consulting_assistants_api/test/lint/#linting-with-mypy)

This repository contains a Software Development Kit to help build [IBM Consulting Assistants](https://servicesessentials.ibm.com/launchpad/) Extensions and Integrations, consisting of:

- 📚 **libica**:
    Python extension library designed to seamlessly integrate with IBM Consulting Assistants' Extension APIs. It provides a way to interact with various AI models, assistants, prompts, document collections, manage chat sessions, and execute prompts, all through a python library (`libica`). Provides an out of the box retry mechanism with exponential backoff as well as asynchronous support. Implements all the features of the IBM Consulting Assistants Extensions API v4.5.
    Comes with [sample code and Jupyter Notebooks](https://github.ibm.com/destiny/consulting_assistants_api/tree/main/test/sample_code).
- 💻 **icacli**:
    Command-line tool (`icacli`) with shell auto-completion.
    It also offers an interactive "REPL" style CLI.
    It implements all the functions available through **libica**
- 🔗 **langchain_consultingassistants**:
    Provides extensions API integration with langchain.
    It implements all the functions available through **libica**
- 🛠️  **ansible_consultingassistants**:
    Provides extensions API integration with ansible.
    It implements all the functions available through **libica**
- 🐚 **ica.sh**:
    Provides easy to use shell functions for using the IBM Consulting Assistants API.
    Based on curl, provides easy automation and troubleshooting.
- 🦾 **icamock**:
    Mock IBM Consulting Assistants API, BAM and watsonx.ai APIs, used to help you quickly test / develop your integrations. Instantly returns prompt results.

This is part of the Integrations and Extensions ecosystem, also containing:

- 🌐 **integrations_host**:
    Provides a FastAPI server designed to serve integration APIs.
    Easily extensible with new integrations by adding new `app/routes`.
    Integrates with **libica** to provide out of the box extensions support,
    through **libica** or **langchain_consultingassistants** modules.
    Design to run as a secure (podman) container.
- 🔌 **integrations**:
    A number of IBM Consulting Assistants integrations have been developed and are documented [here](https://pages.github.ibm.com/destiny/consulting_assistants_api/integrations/).
- 🔨 **integration_builder**:
    Generates an integration using our standard template, with logging and best practices. On `ica_container_host` - type `make integration`, provide an integration name and it will build a new integration route.

> ⚠️ Obtaining an API Key
>
> For access to an Extension API key contact the IBM Consulting Assistants team and register as an extension developer.
> This library is designed to support existing Extension API developers.

![icacli demo](images/demo/libica.gif)

## 🔑 Key Features

🐍 Installable via pip, with Python 3.11 compatibility, written in modern Python.

📖 Complete [documentation](https://pages.github.ibm.com/destiny/consulting_assistants_api/src/libica/libica/). 100% code documentation coverage, 100% pydocstyle - with full docstring, doctest and type hints, examples and a manpage.

📐 [Complete Architecture Decisions and Design Information](https://pages.github.ibm.com/destiny/consulting_assistants_api/design/) tracks all key architecture decisions and design considerations.

🔐 Secure by default: Integrated CI/CD build with [linters and static analysis tools], currently at 100% pass, including isort, flake8, pylint, mypy, bandit, pydocstyle, pre-commit hooks, ruff, pyright, pip-licenses, fawltydeps, radon, pyroma, pyre, wyre, pytest, coverage.

🛠️ pyproject.toml and `pdm` support, modern Python packaging with full unit testing and static analysis, fully integrated with `make`.

🔗 Support native Python or Langchain style calls.

📦 Built-in per-team caching support with configurable timeouts for retrieving `models`, `tags`, `roles`, `prompts`, `assistants`, `collections`. Can also be disabled. Support for individual `refresh_data` calls.

⚡️ Automatic, configurable retry, with *exponential backoff, with jitter* ensures your API calls succeed without abusing the API.

🔧 Fully configurable via configuration file, or environment, with Pydantic based validation.

📦 Designed to work well and securely in containers, and run on `podman` or `OpenShift` using Red Hat's universal base image.

💻 CLI with both commandline and interactive options, with full `zsh` and `bash` auto-complete support - and a complete manpage.

🐛 Consistent debug and logging support across the tooling ecosystem. Just export `ASSISTANTS_DEBUG=1`.

## 🚀 Getting Started

### 📋 Requirements

🍎 Apple Intel or ARM (ex: M1/M2/M3) Mac, 🐧 Linux or 🪟 Windows Operating System.

🐍 A recent, supported version of Python 3.9, 3.10 or 3.11 - with the `pip` Python package manager.

For more information on installing Python, see the [Help](https://pages.github.ibm.com/destiny/consulting_assistants_api/help/installing-python/) section.

<details markdown="1">

  <summary>👀 Verifying Requirements</summary>

  **Python**

  You can find out what version of Python you are running using:

  ```bash
  python --version
  ```

  **venv, pip and pdm**

  We recommend installing in a Python virtual environment, as a regular user (non-root). You will need `pip` and `pdm` to install `libica`.

  **An official IBM Consulting Assistants Extension ID and Token**

  In order to use the Extensions API, you are required to register as an Extensions owner. If you do not have a key, this project will **not** provide you with one. You will use these in the configuration for the `ASSISTANTS_APP_ID` (`x-extension-app-id`) and `ASSISTANTS_ACCESS_TOKEN` (`x-access-token`).

  **A team API Key**

  You can generate one yourself, for any team you are an owner of. To do so, go to **Settings > My Settings > API Key** and click **Generate API Key** in the IBM Consulting Assistants interface. This corresponds to the `ASSISTANTS_API_KEY` (`x-security-key`) variable.

  **Make (optional)**

  A number of useful `make` targets have been provided in the shipped `Makefile` to help automate the installation steps, such as `make venv` to create a virtual environment, or `make install` to install the library.

  To install `make` refer to your distribution package manager installation guide. For example, on Mac, this would be `brew install make` - while on Red Hat Enterprise Linux, you can use `sudo dnf install make`. On Debian/Ubuntu, `sudo apt install make`.

  **An SSH Configured in IBM GitHub (Optional)**

  Having an SSH key configured lets you clone the GitHub repository without having to type in a password.

  If you do not have an SSH key, you can create a new SSH key using `ssh-keygen`.

  You can add the public key (ex: `id_rsa.pub`) to your [GitHub Account](https://github.ibm.com/settings/keys) in **Settings > Access | SSH and GPG keys > New SSH Key**.

</details>

### 🐍 Installation

A quick getting started guide that installs `pip` and `pdm`, then installs `libica`:

```bash
# Install and / or upgrade pdm and pip
python3 -m pip install --upgrade pip pdm # Upgrade pip and pdm

# Clone a release version of this repository, using either https or ssh:
git clone git@github.ibm.com:destiny/consulting_assistants_api.git --branch v0.8.0 # or:
git clone https://github.ibm.com/destiny/consulting_assistants_api --branch v0.8.0
cd consulting_assistants_api

# Using make to setup a venv:
make venv                       # Create a virtual environment
make activate                   # Tells you how to activate the venv
. ~/.venv/consulting_assistants_api/bin/activate # Activate your venv
make install                    # If you have make

# Alternative, without using make:
python3 -m venv ~/.venv/consulting_assistants_api
python3 -m pip install .        # Install with pip
python3 -m pip install '.[dev]' # Install development dependencies
python3 -m pip install '.[langchain]' # Install langchain libraries

# Create a configuration file
mkdir -p ~/.config/icacli
cp .ica.env.sample ~/.config/icacli/.ica.env

# Edit .ica.env or run setup-config and set your keys:
icacli setup-config

# Check out the manpage or help. Optional
make manpage # Just type `make` to see all build targets!
man icacli
icacli --help

# Try a prompt!
icacli get-models --refresh_data
icacli prompt --model_id_or_name="Llama3.1 70b Instruct" --prompt "What is OpenShift?"
```

Example installation in real time, with developer dependencies:
![Example Demo](images/demo/install.gif)

**Note**: You can also launch the `python3 -m icacli.assistants --help` if you don't have it in your PATH, but have it in your Python module path.
This can be useful on Windows.

Alternatively, you can install this directly from git, if your pip supports it:

```bash
python3 -m pip install \
  libica@git+ssh://git@github.ibm.com/destiny/consulting_assistants_api.git@v0.8.0#egg=libica
```

### ⚙️ Configuration

You must configure your environment with the necessary API credentials. 🔑

Create a `.ica.env` file in ~/.config/icacli/.ica.env or the current directory. You can create one using `icacli setup-config`:

```bash
icacli setup-config # Creates or edits ~/.config/icacli/.ica.env
```

```bash
# ~/.config/icacli/.ica.env - IBM Consulting Assistants Extensions Python library - configuration file
ASSISTANTS_BASE_URL="https://servicesessentials.ibm.com/apis/v1/sidekick-ai"
ASSISTANTS_APP_ID="x-extension-app-id"   # Extension ID
ASSISTANTS_API_KEY="x-security-key"      # Team API key
ASSISTANTS_ACCESS_TOKEN="x-access-token" # Service level token

ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME="Llama2 70B Chat" # Default model
ASSISTANTS_RETRY_ATTEMPTS="3" # Number of retry attempts for API calls.
ASSISTANTS_RETRY_BASE_DELAY="10" # Base delay in seconds for exponential backoff in retries mechanism.
ASSISTANTS_RETRY_MAX_DELAY="200.0" # Maximum delay in seconds for exponential backoff in retries mechanism.

ASSISTANTS_CACHE_DIRECTORY=~/.config/icacli/cache # Directory for caching models, prompts, assistants, collections, tags, roles
ASSISTANTS_CACHE_DURATION_HOURS="24" # Most get commands are cached for this duration, like get-models. Prompt is NOT cached.

ASSISTANTS_DEFAULT_FORMAT=table # Default output (table or json)
ASSISTANTS_TABLEFMT="simple" # Type of table. simple, github, ...
ASSISTANTS_ENABLE_RICH_PRINT=1 # Enable colors / rich printing when running the cli / interactive mode

ASSISTANTS_DEBUG=0 # Enable debug logging
```

### 💻 Using the CLI: icacli

```
usage: icacli [-h] [--format {table,json}]
              {get-models,get-tags,get-roles,get-prompts,get-assistants,get-collections,create-chat-id,remove-chat-id,execute-prompt,get-transaction-response,execute-prompt-async,create-prompt,prompt,setup-config}
              ...

IBM Consulting Assistants - API CLI Tool: A command-line interface for interacting with the extensions API.

positional arguments:
  {get-models,get-tags,get-roles,get-prompts,get-assistants,get-collections,create-chat-id,remove-chat-id,execute-prompt,execute-prompt-async,get-transaction-response,create-prompt,prompt,setup-config,interactive}
                        commands
    get-models          Retrieve a list of available models, allowing for specification of columns and control over pagination.
    get-tags            Fetch a list of tags used within the system. Allows for pagination.
    get-roles           List all roles available, with options to control output volume through pagination.
    get-prompts         Retrieve stored prompts, optionally filtered by tags and roles, with pagination support.
    get-assistants      Fetch a list of assistants, with options to filter by tags and roles and to control the output format and volume.
    get-collections     List collections in the system, including details such as IDs, names, and status, with pagination options.
    create-chat-id      Creates a new chat session ID that can be used to manage and persist context across multiple interactions.
    remove-chat-id      Deletes a specific chat session ID, clearing any stored context or history associated with it.
    execute-prompt      Executes a given prompt against a specified chat session, model, assistant, or collection.
    execute-prompt-async
                        Executes a prompt asynchronously, allowing for operations that might take longer to complete.
    get-transaction-response
                        Retrieves the response for a previously executed asynchronous prompt by its transaction ID.
    create-prompt       Allows for the creation of a new prompt, specifying its scope, title, description, and optional response.
    prompt              Execute a prompt with automatic chat ID management
    setup-config        Setup or update the configuration file.
    interactive         Enter an interactive REPL for executing prompts

options:
  -h, --help            show this help message and exit
  --format {table,json}
                        Output format (default: table).
```

You can find a detailed list of examples on how `icacli` can be used in [test/test_commands.sh](https://github.ibm.com/destiny/consulting_assistants_api/blob/main/test/test_commands.sh)

### 🐛 Debugging

You can turn on debug logging for libica and icacli by exporting `ASSISTANTS_DEBUG=1`

```bash
export ASSISTANTS_DEBUG=1

# You can also turn this for individual commands
ASSISTANTS_DEBUG=1 icacli get-models --refresh
"""
2024-04-12 01:48:58,529 - DEBUG - Starting new HTTPS connection (1): servicesessentials.ibm.com:443
2024-04-12 01:49:03,193 - DEBUG - https://servicesessentials.ibm.com:443 "GET /apis/v1/sidekick-ai/getModels HTTP/1.1" 200 None
...
"""

# You can change any of the ENV variables in the config in a similar way:
ASSISTANTS_TABLEFMT=github icacli get-models
```

**Using it with curl for debugging individual API requests:**

```bash
export CHAT_ID=$(icacli create-chat-id --model_id_or_name="Llama2 70B Chat")

curl -X 'POST' "${ASSISTANTS_BASE_URL}/executePrompt" \
	-H "x-access-token: ${ASSISTANTS_ACCESS_TOKEN}" \
	-H "x-security-key: ${ASSISTANTS_API_KEY}" \
	-H "x-extension-app-id: ${ASSISTANTS_APP_ID}" \
	-H "Content-Type: application/json" \
	-d "{\"prompt\": \"How do I bake a pepperoni pizza that is crispy\",\"modelId\": \"222\", \"chatId\": \"${CHAT_ID}\"}"
```

See also: `ica.sh`, a curl-based commandline tool.

### 👋 Using icacli interactive

You can run `icacli` in interactive mode. A number of commands let you change models, assistants or collections.

```
icacli interactive
```

```
Interactive CLI commands:
/quit - Exit the interactive CLI.
/add <file> - Add a text file to the chat for editing.
/help - Display this help message.
/model - Change to a different model with tab completion.
/collection - Change to a different collection.
/assistant - Change to a different assistant.


📄 [Llama2 70B Chat)]> 1+1
Sure! 1+1 equals 2.

📄 [Llama2 70B Chat)]> /assistant
Enter a tag for the assistant: unified
1. UNIFIED 01: Epic and User Story Creator
2. UNIFIED 02: Story to Python Code  Generator
3. UNIFIED 03: Python Test Case Generator
Choose by number (or 'cancel' to return): 1

🤖 [UNIFIED 01: Epic and User Story Creator)]> /collection
1. TEST
```

### 🛠️  Ansible Library

1. Copy `src/consulting_assistants_ansible/consulting_assistants.py` to `~/.ansible/plugins/modules`
2. Test that the module works: `ansible localhost -m consulting_assistants -a "prompt='Hello, world!' assistant_id='3903'" -M ~/.ansible/plugins/modules`
3. Create a `consulting_assistants_playbook.yml` file, such as:
```yaml
---
# This playbook uses the consulting_assistants module to execute a prompt flow.
- hosts: localhost
  gather_facts: false
  environment:
    ANSIBLE_LIBRARY: ~/.ansible/plugins/modules
  tasks:
    - name: Execute prompt flow
      consulting_assistants:
        prompt: "What is 1+1? Just give me the answer"
        model_id_or_name: "Llama2 70B Chat"
        # assistant_id: "optional-assistant-id"
        # collection_id: "optional-collection-id"
        # system_prompt: "optional-system-prompt"
        # parameters: {"key1": "value1", "key2": "value2"}
        # substitution_parameters: {"key1": "value1", "key2": "value2"}
        # refresh_data: false
      register: consulting_assistants_result

    - name: Print consulting assistants result
      debug:
        var: consulting_assistants_result.response

```
4. Execute the playbook: `ansible-playbook -v consulting_assistants_playbook.yml`
```
PLAY [localhost]

TASK [Execute prompt flow]
*********************************************************
changed: [localhost] => {"changed": true, "response": "  Sure! The answer to 1+1 is 2."}

TASK [Print consulting assistants result]
*********************************************************
ok: [localhost] => {
    "consulting_assistants_result.response": "  Sure! The answer to 1+1 is 2."
}

PLAY RECAP
*********************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### 💻 Using libica in your code

#### Initializing ICAClient

```python
from libica import ICAClient
client = ICAClient()
```

#### Getting detailed help on any function

ICAClient has been designed with detailed docstring help. You can always retrieve the latest help using the `help()` command in python.


```python
from libica import ICAClient
client = ICAClient()

help(client)
"""
class ICAClient(builtins.object)
 |  ICAClient(settings: Optional[libica.libica.Settings] = None)
 |
 |  API Client to interact with IBM Consulting Assistants Extensions v4.5.
 |
 |  This client provides methods to call API endpoints for managing models, tags, roles, assistants, collections, chat IDs, and executing prompts.
 |  It supports caching for models and tags to reduce network requests.
 |
 |  Examples:
 |      >>> client = ICAClient()
...
"""

help(client.prompt_flow) # Most of the time, you will be using `prompt_flow` which creates a chat_id and runs execute_prompt.

"""
prompt_flow(prompt: str, model_id_or_name: Optional[str] = None, assistant_id: Optional[str] = None, collection_id: Optional[str] = None, system_prompt: Optional[str] = None, parameters: Optional[dict] = None, substitution_parameters: Optional[dict] = None, refresh_data: bool = False) -> Optional[str]
    Handle the flow of creating a chat ID and executing a prompt using that chat ID.
...
"""
```

#### Working with models

```python
from libica import ICAClient
client = ICAClient()

# List available models as JSON, refreshing the data from the API (instead of using cache)
client.get_models(refresh_data=True)

# Send a prompt to a model name
response = client.prompt_flow(model_id_or_name="Mixtral 8x7b Instruct", prompt="Who is Ada Lovelace?")
print(response)
"""
Ada Lovelace was an English mathematician and writer, chiefly known for her work on Charles Babbage's early mechanical general-purpose computer.
"""
```

#### Working with assistants

```python
from libica import ICAClient
client = ICAClient()

roles = client.get_roles()  # List roles (supports refresh_data=True)
tags = client.get_tags()    # List tags (supports refresh_data=True)

# List available assistants with the 'SDLC Assistants' tag and the 'Software Developer' role:
assistants = client.get_assistants(tags=['SDLC Assistants'], roles=['Software Developer'], refresh_data=False)
for assistant in assistants:
    if assistant['id']==6858:
        print(assistant['id'],assistant['title'])
"""
6858 Python Code Generator for Efficient and Well-Structured Code
"""

# Send a prompt to an assistant id
response = client.prompt_flow(assistant_id="6858", prompt='Function to add 2 numbers')
"""
def add_numbers(a, b):
    return a + b
"""
```

#### Working with document collections

```python
from libica import ICAClient
client = ICAClient()

collections = client.get_collections(refresh_data=True)

for collection in collections['collections']:
    if (collection['userName']=='MIHAI CRIVETI'):
        print(collection['_id'],collection['collectionName'],collection['documentNames'])
        # CLI equivalent would be: icacli get-collections --columns='_id,collectionName,documentNames'
"""
66142f5a2dd4fae8aa4d5781 IBM Consulting Assistant Extension Developer's Guide ['Sidekick AI API Documentation - Early Adopters 4.5.pdf']
"""

response = client.prompt_flow(collection_id='66142f5a2dd4fae8aa4d5781', prompt='How do I list a collection using the API')
print(response)
"""
To utilize this API, we need to send a GET request to the URL 'https://servicesessentials.ibm.com/apis/v1/sidekick-ai/getCollections'. We also need to include essential headers such as accept, x-access-token, x-security-key, and x-extension-app-id.

The response will then provide us with a list of collections, along with their properties like createdAt, updatedAt, teamId, userEmail, userName, document Names, visibility, collection name, status, tags, roles, and _id.
...
"""
```

#### Working with prompts

```python
from libica import ICAClient
client = ICAClient()

# Create a prompt in your personal prompt library:
client.create_prompt(prompt_title="OpenShift Description",
  prompt_description="Asks the model what is OpenShift",
  model_id_or_name="Granite 13B V2.1",
  scope="mine",
  prompt="What is OpenShift?")
"""
[{'createdOn': '2024-04-12T00:32:17.476+00:00',
  'description': 'Asks the model what is OpenShift',
  'model': '180',
  'modelName': None,
  'modifiedOn': '2024-04-12T00:32:17.476+00:00',
  'visibility': 'PRIVATE',
  'promptId': '0e7d2893-4bcf-4bf2-9b70-d84783c00153',
  'prompt': 'What is OpenShift?',
  'promptTitle': 'OpenShift Description',
  'user': {'name': 'MIHAI CRIVETI', 'email': 'CRMIHAI1@ie.ibm.com'},
  'userEmail': 'CRMIHAI1@ie.ibm.com',
  'tags': [],
  'roles': []}]
"""

for prompt in client.get_prompts(refresh_data=False):
    if prompt["promptId"] == '0e7d2893-4bcf-4bf2-9b70-d84783c00153':
        print(f"{prompt['promptTitle']}, {prompt['model']}")
"""
OpenShift Description, 180
"""
```

#### Working with chat_id and execute_prompt_async

Longer running prompts (ex: > 100s) can use execute_prompt_async to avoid API timeouts.

To use `execute_prompt_async` you first need to create a chat_id.

```python
from libica import ICAClient
client = ICAClient()

chat_id = client.create_chat_id(model_id_or_name="Granite 13B V2.1")
"""
6618826083c816894556fc6c
"""

transaction_id = client.execute_prompt_async(chat_id=chat_id, prompt="What is 1 + 1", model_id_or_name="Granite 13B V2.1")
"""
f9cfcbb3-2174-4f8d-b579-5d9ee48aed54
"""

# You can use get_async_response to keep trying to retrieve the response every `interval` seconds:
response = client.get_async_response(transaction_id=transaction_id, max_wait_time = 60, interval = 5)

print(response)
"""
{'chatId': '6618826083c816894556fc6c',
 'modelId': '180',
 'response': 'The sum of 1 and 1 is 2. This is a basic arithmetic operation in which you combine the values of two numbers to get another number. In this case, you add 1 plus 1 together to get 2. If you have any more math-related questions or need help with something else, feel free to ask!',
 'responseChunks': [],
 'messageTokens': 7,
 'answerTokens': 69,
 'totalUsedTokens': 76}
"""

# Optionally, delete your `chat_id`
client.remove_chat_id(chat_id)
"""
{'message': ''}
"""
```

Note: You can also use `client.execute_prompt` in place of `client.execute_prompt_async` to make this synchronous. This will no longer require
`client.get_transaction_id`, but still requires a `chat_id`. The provided `client.prompt_flow` function can replace the use of `execute_prompt`
by performing all the required steps (creating a `chat_id` and running `execute_prompt` with that `chat_id`, then deleting that `chat_id`)

You can more usage examples in [test/sample_code](https://github.ibm.com/destiny/consulting_assistants_api/tree/main/test/sample_code)

## 📔 Jupyter Notebook

A [sample Jupyter Notebook](https://github.ibm.com/destiny/consulting_assistants_api/tree/main/test/sample_code) is also provided.

## 📖 Library documentation

For mode details, see [the library documentation](https://pages.github.ibm.com/destiny/consulting_assistants_api/src/libica/libica/)

## 🐚 Shell Client

`tools/ica.sh` is a shell tool that uses `curl` and `jq` to make requests to the IBM Consulting Assistants API.

It can be useful as a troubleshooting tool, or to easily include as part of your automation scripts.

#### Example usage:

```bash
export ASSISTANTS_CURL_CACHE_DIR=/tmp/assistants_curl_cache
export ASSISTANTS_BASE_URL="https://servicesessentials.ibm.com/apis/v1/sidekick-ai"
export ASSISTANTS_APP_ID=
export ASSISTANTS_API_KEY=
export ASSISTANTS_ACCESS_TOKEN=

# You can now use commands from your shell, like this, and combine them with commands like 'jq'
getModels | jq
getTags | jq
getRoles | jq
getAssistants | jq
getAssistants_tag | jq
getCollections | jq
getPrompts | jq

# Creating a chatId, and executing prompts:
export CHAT_ID=$(createChatId) # Remember, this expires after 15 min
export MODEL_ID=261 # Llama3.1 70b Instruct
export ASSISTANTS_PROMPT="Hi"
executePrompt
deleteChatId

# Executing prompts Async
executePromptAsync
getTransactionResponse
```

## 🔗 Langchain Library


```python
# Import the langchain_consultingassistants modules
from langchain_consultingassistants import ChatConsultingAssistants

# langchain imports
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# get the prompt template
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")

# set the model
model = ChatConsultingAssistants(model="Llama3.1 70b Instruct")

# set the parser
output_parser = StrOutputParser()

# set the chain
chain = prompt | model | output_parser

# invoke
result = chain.invoke({"topic": "ice cream"})

# result
print(result)
```

## 🔌 Developing Integrations

To develop integrations that call models, prompts, assistants or document collections in ICA, using `libica` see the provided [ica_integrations_host](https://github.ibm.com/destiny/ica_integrations_host) repository. More information on available integrations can be found in the Documentation Integrations page.

## 🪛 Developing libica

This package uses `pdm`. To test everything locally:

```bash
pre-commit run -a
make venv
make install

# Run the test coverage suite and check results
make lint
make unittest
make coverage
coverage report

# Build and test the container
make podman
make podman-run

# Run the container in interactive mode
podman run -it --rm --env-file ~/.config/icacli/.ica.env localhost/ica/icacli /bin/bash

# Build and test the docs
make images
make docs

# Build a package
pdm build

# Try uploading to a local pypi and test it from there
pdm publish --repository http://localhost:5555
```

For more information, refer to [DEVELOPING.md](DEVELOPING.md)

## 🗺️  Roadmap

The current release is v0.8.0, tagged 2024-05-13. If you have any features you'd like to propose, create a GitHub Issue, or slack @cmihai.

The following changes are planned:

### 0.7.0 - 2024-05-01

- [X] Add support for documentNames when searching a collection
- [X] Common logging across all modules, with verbose logging and support for writing logs to a file.
- [X] Documentation improvements and video tutorials.
- [X] Split ICAClient class into multiple files (Base, ICACatalog, ICAClient), make some methods private.
- [X] `icacli interactive` autocomplete via prompt_toolkit (re-implementation).
- [X] Deployment to JFrog Artifactory or similar repository (planned) for simplified dependency management.
- [X] Initial support for `getModel`, `getSecurityKey`, `createSecurityKey`
- [X] Initial support for BAM for use in debugging and local testing.

### 0.8.0 - 2024-05-13

- [X] Switch default model to LLAMA3
- [X] Improvements to retry mechanism after validating the API response.
- [X] Improvements to the langchain library.
- [X] Initial support for BAM and watsonx.ai models, via config file / ENV.
- [X] Major documentation updates, design, carwash program
- [X] First deployment into production (private team)
- [X] Major linting and code quality improvements

### 0.9.0 - 2024-05-20

- [ ] Change the 'ASSISTANTS_BASE_URL=https://servicesessentials.ibm.com/apis/v1/'
- [ ] Catch `^C` in `icacli setup-config`
- [ ] Add an option to clear all cache.
- [ ] Support for Scribeflow APIs (directly).
- [ ] Add `validateSecurityKey` and `validateExtensionAppId` to API and CLI. Future: integrate into error handling / validation.
- [ ] Mock API improvements, providing full YAML for all API paths as an example.
- [ ] Add warnings not just log.debug, log to file, overall improvements in debug logging.
- [ ] Implement caching mechanism for chat_id.
- [ ] Re-order unit tests into groups for optimal rate limiting optimization.
- [ ] Add `validateSecurityKey` and `validateExtensionAppId` validation to API and CLI.
- [ ] Improved support for BAM and watsonx.ai models, configuration file improvements
- [ ] Implement caching mechanism for `chat_id`.
- [ ] Implement caching mechanism for LLM calls.

### 1.0.0 - 2024-06-03

- [ ] Code freeze as we focus on supporting the user community and bugfixes.


## 🎯 Troubleshooting

### Installation

1. Ensure that you have a recent and supported version of Python.
2. Always install a clean `venv`. The `make venv install` targets can set that up for you. Remember to enter your `venv` after, for example: `~.venv/consulting_assistants_api/bin/activate`
3. While most platforms provide binary packages for [pydantic v2](https://pypi.org/project/pydantic/), if your platform is not supported, you may need to have a recent `rust` compiler installed.
4. If you are having issues installing on your local OS, try building the provided `podman` container with `make podman`.

## ❓FAQ

<details markdown="1">
  <summary>How do I obtain API Keys</summary>
  1. To obtain API keys for extension development, please contact the IBM Consulting Assistants Team.
  2. To obtain API keys for your TEAM, you can use the Export API Keys feature.
</details>

<details markdown="1">
  <summary>Where can I deploy my integration?</summary>
  1. Integrations can be deployed either *centrally*, for officially supported integrations.
  2. Or on your own infrastructure, for *community* integrations.
</details>

<details markdown="1">
  <summary>Why do I get a warning every time I run the tool?</summary>
  You are likely using an older or unsupported version of Python.
</details>

## 🪲 Known Issues

- [ ] `libica`: parameters and systemprompt don't work correctly in the current IBM Consulting Assistants Extensions API.
- [ ] `libica`: `substitutionParameters` is not currently implemented / no models exist to allow testing this feature.

## 👀 See Also

* [ica_integrations_host](https://github.ibm.com/destiny/ica_integrations_host) - Leverages libica to build integrations, and provides a secure FastAPI and Red Hat Universal Base Image based container to host integrations.

## 🚩 Reporting Bugs

📋 Please provide a detailed description of your problem, and open an Issue [here](https://github.ibm.com/destiny/consulting_assistants_api/issues)

💬 Join the IBM Consulting Assistants community on [Slack](https://ibm.enterprise.slack.com/archives/C04U5TE3PFV).

## 🧔 About

This project was started to support IBM Consulting Assistants Extensions and Integrations developers, and to provide them with the best possible development experience, using a common, inner-source, well maintained, secure, fully documented set of tools.

**Authors:**

- [Mihai Criveti](https://github.ibm.com/crmihai1/) 📫 <crmihai1@ie.ibm.com>
- [Chris Hay](https://github.ibm.com/chris-hay) 📫 <chris.hay@uk.ibm.com>

## 🙋 Users

The following projects use `libica`. Please submit a PR or reach out if you are using this in your software.

Project Name / URL | Description | Contact
--------------|-------------|------------------
[ica_integrations_host](https://github.ibm.com/destiny/ica_integrations_host) | IBM Consulting Assistants Integration Container | Mihai Criveti/Chris Hay
[Cognitive Architect](https://pages.github.ibm.com/CTOTools/CogArch_Docs/) | Cognitive Architect pilot using Scribeflow and libica | Jenny Ang / Yin Jun Zhang
TBD | Experience Orchestrator Pilot Project | Marco Altea
TBD BMW Pilot Team (Internal) | Planned internal testing with BMW account team| Björn Schmitz
WFM Expert | Work Force Management Expert Integration | Claire Lubash, Othul, Mihai
