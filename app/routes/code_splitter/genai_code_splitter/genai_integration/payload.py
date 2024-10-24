import asyncio
import logging
import re

from .genai_caller import invoke_genai_adapter, invoke_ica

log = logging.getLogger(__name__)


async def prepare_genai_tasks(
    chunk_obj: dict, id_list: dict, genai_platform: str, filter_code: dict = None
) -> dict:
    """
    Prepares and executes tasks to invoke the GenAI adapter for transforming content.

    Args:
        chunked_entities (dict): A dictionary containing entities to be processed.
        id_list (dict): A dictionary mapping entity types to prompt IDs.
        genai_platform(str): String specifying the platform of LLM to be used.

    Returns:
        dict: The updated chunked_entities dictionary with transformed content.
    """

    jobs = []
    chunked_entities = chunk_obj.get("chunked_entities")
    headers = chunk_obj.get("headers", "")

    for id, val in chunked_entities.items():
        if val.get("type") in id_list:
            jobs.append(
                (id, val.get("content", ""), id_list.get(val.get("type")))
            )
        else:
            chunked_entities[id]["transformed"] = chunked_entities[id]["content"]

    if genai_platform == "ica":
        tasks = [
            invoke_ica(template, content, headers) for id, content, template in jobs
        ]
    else:
        tasks = [
            invoke_genai_adapter(prompt_id, content, headers) for id, content, prompt_id in jobs
        ]

    log.info("Task list prepared for genai adapter job")
    results = await asyncio.gather(*tasks)

    for (id, _, _), result in zip(jobs, results):
        if genai_platform == "ica" and filter_code:
            start = filter_code.get("start", "<code>")
            end = filter_code.get("end", "</code>")
            pattern = rf'{start}(.*?){end}'
            match = re.search(pattern, result, re.DOTALL)
            chunked_entities[id]["transformed"] = match.group(1) if match else result

        else:
            chunked_entities[id]["transformed"] = result
    return chunked_entities
