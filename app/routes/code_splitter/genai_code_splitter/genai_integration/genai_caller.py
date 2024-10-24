import os
import aiohttp
import asyncio
import logging
from libica import ICAClient
from jinja2 import Environment, FileSystemLoader

# Load environment variables from a .env file
genai_adapter_url = os.getenv("GENAI_ADAPTER_URL", None)
template_env = Environment(loader=FileSystemLoader("app/routes/code_splitter/templates"))


log = logging.getLogger(__name__)


async def invoke_genai_adapter(prompt_id: str, inputs: str, headers: str = "") -> str:
    """
    Sends a prompt to the GenAI adapter and retrieves the response.

    Args:
        prompt_id (str): The ID of the prompt to be sent.
        inputs (str): The input data for the prompt.
        headers (str): header contains signature of all the methods.

    Returns:
        str: The result from the GenAI adapter or an error message.
    """
    data = {"prompt_id": prompt_id, "inputs": [inputs], "parameter": {"package": headers}}
    result = ""
    try:
        if data["prompt_id"]:
            log.info("Requesting response from GenAI adapter")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    genai_adapter_url, json=data, ssl=False
                ) as response:
                    if response.status == 200:
                        log.info("Success response from GenAI adapter")
                        result = await response.text()
                        log.info(f"Result generated for prompt : {prompt_id}")
                    return result
    except Exception as ex:
        log.exception("Error while calling GenAI Adapter ", ex)
        return "Error from GenAI Adapter"


async def invoke_ica(template_obj: dict, input: str, headers: str = ""):
    client = ICAClient()
    log.info("Requesting response from ICA adapter")
    template = template_env.get_template(template_obj.get("template_name"))
    rendered_code = template.render(code=input, headers=headers)
    llm_response = await asyncio.to_thread(client.prompt_flow, model_id_or_name=template_obj.get("model"), prompt=rendered_code)
    log.info("Response Generated from ICA adapter")
    if llm_response is None:
        llm_response = "No response from LLM"

    return llm_response
