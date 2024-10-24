# -*- coding: utf-8 -*-
"""
Pytest for docbuilder route.

Description: Tests docbuilder route.

Authors: Mihai Criveti
"""

from fastapi.testclient import TestClient

from app.server import app

client = TestClient(app)


def test_docbuilder_endpoint():
    test_data = {
        "input_text": "Various kinds of boat",
        "template_type": "IBM Consulting Green",
    }
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post("/experience/docbuilder/generate_docs/invoke", json=test_data, headers=headers)
    assert response.status_code == 200
