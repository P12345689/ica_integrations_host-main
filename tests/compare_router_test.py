# -*- coding: utf-8 -*-
import csv
import io

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.routes.compare.compare_router import add_custom_routes


@pytest.fixture
def app():
    app = FastAPI()
    add_custom_routes(app)
    return app


def test_compare_documents(app):
    client = TestClient(app)
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/experience/compare/compare_documents/invoke",
        json={
            "document1": "Content of first document...",
            "document2": "Content of second document...",
            "instruction": "Compare these legal documents and identify differences",
            "output_format": "markdown",
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert "invocationId" in response.json()


def test_compare_documents_with_input_from_files(app):
    client = TestClient(app)

    csv_result, text_result = create_in_memory_files()

    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    response = client.post(
        "/experience/compare/compare_documents/invoke",
        json={
            "document1": text_result,
            "document2": csv_result,
            "instruction": "Compare this cvs document with text file and identify differences. Spot similarities",
            "output_format": "plain",
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert "invocationId" in response.json()


def create_in_memory_files():
    csv_data = [
        ["Name", "Age", "City"],
        ["Alice", "30", "New York"],
        ["Bob", "25", "San Francisco"],
        ["Charlie", "35", "London"],
    ]

    text_data = """A software developer is like a toy maker,
    but instead of making toys with plastic and wood, they
    make special toys that live inside computers and phones."""

    csv_file = io.StringIO()
    csv_writer = csv.writer(csv_file)
    for row in csv_data:
        csv_writer.writerow(row)
    csv_content = csv_file.getvalue()

    text_file = io.StringIO()
    text_file.write(text_data)
    text_content = text_file.getvalue()

    return csv_content, text_content
