import logging
from jinja2 import Environment, FileSystemLoader
from langchain.prompts import PromptTemplate

# Constants
TEMPLATES_DIRECTORY = "app/routes/agent_langchain/templates"

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def get_prompt_template(input_data, template:str):
    # check if a prompt template is passed
    if input_data.prompt_template:
        # get the prompt template passed from the user
        agent_prompt_template = input_data.prompt_template
        log.debug("Using custom prompt template from API input.")
    else:
        # get the default prompt template
        agent_prompt_template = template_env.get_template(template).render()
        log.debug("Loaded default agent prompt template.")

    # set the prompt template
    return PromptTemplate(
        template=agent_prompt_template,
        input_variables=["input", "context", "chat_history", "agent_scratchpad"],
    )