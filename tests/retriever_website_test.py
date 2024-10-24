# -*- coding: utf-8 -*-
"""
Pytest for retriever website route.

Description: Tests retriever website route.

Authors: Gytis Oziunas
"""

import re
import time
from datetime import datetime

from fastapi.testclient import TestClient

from app.routes.retriever_website.retriever_website_router import app

client = TestClient(app)


# print current time in London
def london_time():
    return time.strftime("%Y-%m-%d %H:%M", time.gmtime(time.time()))


def parse_datetime(text):
    # Regex pattern to capture the full datetime
    pattern = r"datetime: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+)"
    match = re.search(pattern, text)

    if match:
        utc_time = time.gmtime()
        utc_datetime = datetime(*utc_time[:6])
        formatted_time = utc_datetime.strftime("%Y-%m-%d %H:%M")
        return formatted_time
    else:
        return "No match found."


def test_retriever_website():
    url = "http://worldtimeapi.org/api/timezone/Europe/London.txt"
    response = client.post("/retriever_website/invoke", json={"url": url})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["response"]) == 1
    assert response.json()["response"][0]["type"] == "text"
    assert response.json()["response"][0]["message"] != ""
    assert parse_datetime(response.json()["response"][0]["message"]) == london_time()


def test_retriever_website_system():
    url = "http://worldtimeapi.org/api/timezone/Europe/London.txt"
    response = client.post("/system/retriever_website/transformers/url_to_text/invoke", json={"url": url})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["response"]) == 1
    assert response.json()["response"][0]["type"] == "text"
    assert response.json()["response"][0]["message"] != ""
    assert parse_datetime(response.json()["response"][0]["message"]) == london_time()
