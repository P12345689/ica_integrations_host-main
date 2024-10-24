import logging
from jinja2 import Environment, FileSystemLoader
from llama_index.core import PromptTemplate

# Constants
TEMPLATES_DIRECTORY = "app/routes/agent_llamaindex/templates"

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def get_prompt_template(input_data, template: str):
    # check if a prompt template is passed
    if input_data.prompt_template:
        # get the prompt template passed from the user
        agent_prompt_template = input_data.prompt_template
        log.debug("Using custom prompt template from API input.")
    else:
        # get the default prompt template
        agent_prompt_template = template_env.get_template(template).render()
        log.debug("Loaded default agent prompt template.")

    # Ensure agent_prompt_template is a valid string
    if not isinstance(agent_prompt_template, str):
        raise ValueError("The prompt template must be a valid string.")

    # Convert input variables list to a single string (if this is the expected format)
    input_variables = ", ".join(["input", "tool_desc", "tool_names"])

    # set the prompt template
    return PromptTemplate(
        template=agent_prompt_template,
        input_variables=input_variables  # Passing as a single string
    )
