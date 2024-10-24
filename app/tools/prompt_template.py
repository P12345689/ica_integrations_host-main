# -*- coding: utf-8 -*-
import logging

# Load Jinja2 environment
from jinja2 import Environment, FileSystemLoader

# langchain
from langchain.prompts import PromptTemplate

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# set the templates directory
TEMPLATES_DIRECTORY = "app/tools/templates"
template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))


def get_prompt_template():
    # open the prompt template
    with open(f"{TEMPLATES_DIRECTORY}/agent_prompt.langchain", "r") as f:
        # read the the template
        agent_prompt_template = f.read()
        log.debug(f"Loaded agent prompt template: {agent_prompt_template}")

        # create the template
        prompt_template = PromptTemplate(
            template=agent_prompt_template,
            input_variables=["input", "chat_history", "agent_scratchpad", "path_list"],
        )
        log.debug(f"Created prompt template: {prompt_template}")

        # return the template
        return prompt_template
