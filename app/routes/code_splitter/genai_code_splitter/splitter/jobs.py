import json
from ..java_parser.chunker import chunk as java_chunk
from ..java_parser.chunker import unchunk as java_unchunk
from ..genai_integration.payload import prepare_genai_tasks
import os
import logging

log = logging.getLogger(__name__)

usecase_file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "assets", "usecase_list.json"
)

with open(usecase_file_path) as f:
    usecase_list = json.load(f)


async def create_jobs(source_code, usecase_id, genai_platform, response_mode):
    usecase = usecase_list.get(usecase_id)
    parser = usecase["parser"]
    if parser == "java":
        return await java_job(
            source_code, usecase, usecase_id, genai_platform, response_mode
        )


async def java_job(source_code, usecase, usecase_id, genai_platform, response_mode):

    max_no_tokens = usecase["max_no_tokens"]
    log.info(f"Maximum number of tokens for a chunk {max_no_tokens}")

    chunked_entities = java_chunk(source_code, max_no_tokens)

    headers = fetch_headers(chunked_entities)

    chunk_obj = {"headers": headers, "chunked_entities": chunked_entities}

    if response_mode == "chunk_only":
        return format_java_chunk(chunk_obj)

    id_list = usecase.get("genai_platform").get(genai_platform, "genai")

    filter_code = usecase.get("filter_code", None)

    transformed_entities = await prepare_genai_tasks(
        chunk_obj, id_list, genai_platform, filter_code
    )

    output_type = usecase.get("output")

    entity = chunked_entities[1]
    if entity["id"] == 1 and entity["parents"] == [0]:
        file_name = entity["name"]

    result = java_unchunk(transformed_entities, response_mode, usecase_id)
    return result, output_type, file_name


def format_java_chunk(chunk_obj):
    headers = chunk_obj.get("headers")
    chunked_entities = chunk_obj.get("chunked_entities")
    result = ""

    result += "\n-----------HEADER---------------\n\n"

    for header in headers:
        result += header

    result += "\n.......................\n\n"

    stats = {}

    for key, val in chunked_entities.items():
        if val["type"] not in stats:
            stats[val["type"]] = []
        stats.get(val["type"]).append(val["name"])

    for key, val in stats.items():
        val_list = ", ".join(val)
        if val[0] == "java_src":
            result += ""
        elif val[0] in [
            "Package",
            "Import",
            "Comment",
            "Annotation",
            "Method",
            "Attribute",
        ]:
            result += f"{key} : {len(val)}\n.......................\n\n"
        else:
            result += f"{key} : {len(val)}\n{val_list}\n.......................\n\n"

    result += "\n-----------CONTENT---------------\n\n"

    for key, val in chunked_entities.items():
        if val["type"] in [
            "package",
            "import",
            "comment",
            "interface",
            "class",
            "comments",
            "annotation",
            "method",
            "attribute",
        ]:
            result += (
                f"\n\n.........\n {val['type']} : {val['name']} \n"
                + "." * 10
                + f"\n {val['content']} \n"
                + "-" * 80
            )

        elif val["type"] == "java_src":
            result += val["content"]

    entity = chunked_entities[1]
    if entity["id"] == 1 and entity["parents"] == [0]:
        file_name = entity["name"]

    return result, file_name


def fetch_headers(chunked_entities):
    headers = ""
    for item in chunked_entities.values():
        if item["type"] == "method":
            line_items = item.get("content").split("\n")
            for item in line_items:
                headers += item + "\n"
                if not item.strip().startswith("@"):
                    break
    return headers
