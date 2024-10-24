#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/17
import json
import os
from uuid import uuid4

import requests


def wrap_resp(invocation_id, event_id, chunk, is_final_event=False):
    response = {
        "status": "success",
        "invocationId": invocation_id,
        "event_id": event_id,
        "is_final_event": is_final_event,
        "response": [{"message": chunk, "type": "text"}],
    }
    return json.dumps(response) + "\n"


async def aget_agent_results(agent_type, prompt, params=None):
    gs_aa_api = os.environ["GS_AGENT_API"]
    gs_aa_api_token = os.environ["GS_AGENT_API_TOKEN"]

    headers = {"Content-Type": "application/json", "X-Auth": gs_aa_api_token}
    body = {"prompt": prompt, "agent_type": agent_type, "params": params}

    invocation_id = str(uuid4())
    event_counter = 0

    with requests.post(gs_aa_api, headers=headers, json=body, stream=True) as resp:
        for line in resp.iter_lines():
            # print('debug line: ', line)
            try:
                resp_chunk = line.decode()
                resp_chunk = resp_chunk.lstrip("data: ")
                if "text" not in resp_chunk:
                    continue
                if "llm_end" in resp_chunk:
                    resp_text = json.loads(resp_chunk)["text"]
                    # resp_text_thought = resp_text.split('Action:')[0]
                    resp_txt = resp_text.strip() + "\n\n"
                    yield wrap_resp(invocation_id, event_counter, resp_txt)
                    event_counter += 1
                if "agent_end" in resp_chunk:
                    resp_txt = json.loads(resp_chunk)["text"]
                    try:
                        resp_json = json.loads(resp_txt)
                        if "answer" in resp_json:
                            yield wrap_resp(
                                invocation_id,
                                event_counter,
                                resp_json["answer"].strip(),
                                is_final_event=True,
                            )
                        else:
                            yield wrap_resp(
                                invocation_id,
                                event_counter,
                                resp_txt,
                                is_final_event=True,
                            )
                    except Exception:
                        yield wrap_resp(invocation_id, event_counter, resp_txt, is_final_event=True)

            except Exception:
                print("gs agent resp: ", line)
                print("failed to parse gs agent response. ")
