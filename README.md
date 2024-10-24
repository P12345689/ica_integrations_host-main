# ICA Integrations Host 🌐

[![Build Status](https://v3.travis.ibm.com/destiny/ica_integrations_host.svg?token=E4rHUNHpL3GkBwESJgRP&branch=main)](https://v3.travis.ibm.com/destiny/ica_integrations_host)

This is an integrations server that can be used for agents that talk to consulting assistants.

See [DOD.md](./DOD.md) for the definition of done - what an integration needs to include to be considered complete.

## Prerequisites
Install and configure libica prior to running ica_integrations_host installation instructions.

- [Install](https://pages.github.ibm.com/destiny/consulting_assistants_api/#installation) libica
- [Configure](https://pages.github.ibm.com/destiny/consulting_assistants_api/#configuration) libica
  - This requires you to have app-id, API key, access-token and base-url for assistants, as per [here](https://w3.ibm.com/w3publisher/ibm-consulting-assistants-api-access-request)
  - Following correct setup, these prompts will work:
    ```
    icacli get-models --refresh_data
    icacli prompt --model_id_or_name="Llama3 70B Instruct" --prompt "What is OpenShift?"
    ```

## 🐍 Installation

🍎 Apple Intel or ARM (ex: M1/M2/M3) Mac, 🐧 Linux or 🪟 Windows Operating System (using WSL).

> Note: If you are using a 🪟 Windows Operating System, please make sure first to [install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).
> Powershell/CMD terminals are currently **not** supported.

```bash
make venv
make install
. ~/.venv/ica_integrations_host/bin/activate # Activate your venv
pip install .

# Install PyTorch on MacOS (temporary workaround, will add to install)
python3 -m pip install torch==2.3.0 --index-url https://download.pytorch.org/whl/cpu

python3 -m pip install ".[libica_local,routes_sdv]"
uvicorn app.server:app --host 0.0.0.0 --port 8080 --reload
```

## 💻 Running the server locallly

In order to run the server you will need to run the following command. You can export the auth token and enable dev routes:

```bash
export ICA_AUTH_TOKENS="dev-only-token"  # Token for authentication to ica_container_host
export ICA_DEV_ROUTES=1                  # Enable development routes
uvicorn app.server:app --host 0.0.0.0 --port 8080 --reload
```

You can generate a secure token using uuid4.

```
python -c "from uuid import uuid4; print(uuid4())"
```

### 🛠️ Testing Locally
You can test the app locally by running a curl command manually

```bash
curl --silent --location \
    --request POST 'http://localhost:8080/experience/joke/retrievers/get_joke/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"topic": "cats"}'
```

### ⚡️ Testing Remote
You can test the app with my hosted code engine instance of the joke service by running a curl command:

```bash
curl --location --request \
    POST 'https://ica_integrations_host.1eqk2rork3yg.eu-gb.codeengine.appdomain.cloud/experience/joke/retrievers/get_joke/invoke' \
    --header 'Content-Type: application/json' \
    --header 'Integrations-API-Key: dev-only-token' \
    --data-raw '{"topic": "cats"}'
```

## Publishing to IBM Cloud
This is how to publish the ica_integrations_host server to IBM Cloud Code Engine

### Login into IBM Cloud
You need to login to IBM Cloud

```bash
ibmcloud login -sso
```

#### Set the default target
You will also need to have your default target installed
```
ibmcloud target -r eu-gb -g default
```

### Install IBM Cloud Plugins
The following plugins will need to be installed

#### Install the code engine plugin
You will need to install the code engine plugin
```
ibmcloud plugin install code-engine
```

#### Install the container registry plugin
You will need to install the container registry plugin

```
ibmcloud plugin install container-registry
```

### Create a project in IBM Cloud
you can now create the project for hosting ica_integrations_host

```
ibmcloud ce project create --name ica_integrations_host
```

### Build the Containerfile

```
podman build --platform=linux/amd64  -t ica_integrations_host .
```

#### Login into the container registry

```
ibmcloud cr login --client podman
```

#### Ensure you have a namespace in container registry

Name it something unique. Replace ica-integrations-host with your container registry namespace.

```
ibmcloud cr namespace-add ica-integrations-host
```

#### Tag the namespace

Tag it, you will need to use your namespace and plugin name

```
podman tag ica_integrations_host uk.icr.io/ica-integrations-host/ica_integrations_host
```

#### Push the container

```
podman push uk.icr.io/ica-container-host/ica_integrations_host
```

### Create the application

1. Create an application in the Code Engine UI
2. Set the listening port to 8080
3. Ensure you are using the right container

```
private.uk.icr.io/destiny/ica_integrations_host:latest
```

## ❓FAQ

#### How do i obtain API Keys?

1. To obtain API keys for extension development, please contact the IBM Consulting Assistants Team on [#assistants-integrations-core](https://ibm.enterprise.slack.com/archives/C074X0S8GSX)
2. To obtain API keys for your TEAM, you can use the Export API Keys feature.

#### Where can I deploy my integration?

1. Integrations can be deployed either *centrally*, for officially supported integrations.
2. Or on your own infrastructure, for *community* integrations.

## 🪲 Known Issues

- [ ] `libica`: parameters and systemprompt don't work correctly in the current IBM Consulting Assistants Extensions API.
- [ ] `libica`: `substitutionParameters` is not currently implemented / no models exist to allow testing this feature.

## 👀 See Also

* [consulting_assistants_api](https://github.ibm.com/destiny/consulting_assistants_api) -  libica library to connect to ICA Extensions API.

## 🚩 Reporting Bugs

📋 Please provide a detailed description of your problem, and open an Issue [here](https://github.ibm.com/destiny/consulting_assistants_api/issues)

💬 Join the IBM Consulting Assistants community on [Slack](https://ibm.enterprise.slack.com/archives/C04U5TE3PFV).

## 🧔 About

This project was started to support IBM Consulting Assistants Extensions and Integrations developers, and to provide them with the best possible development experience, using a common, inner-source, well maintained, secure, fully documented set of tools.

**Authors:**

- [Mihai Criveti](https://github.ibm.com/crmihai1/) 📫 <crmihai1@ie.ibm.com>
- [Chris Hay](https://github.ibm.com/chris-hay) 📫 <chris.hay@uk.ibm.com>
