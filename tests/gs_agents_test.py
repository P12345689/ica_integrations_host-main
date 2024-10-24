# -*- coding: utf-8 -*-
"""
must set up 3 env variable before start this script
export ICA_DEV_ROUTES=1
export GS_AGENT_API=
export GS_AGENT_API_TOKEN=
"""

from fastapi.testclient import TestClient

from app.server import app

client = TestClient(app)


def test_gs_researcher_endpoint():
    test_data = {"prompt": "Hi,"}
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post("/gs_agents/researcher/invoke", json=test_data, headers=headers)
    assert response.status_code == 200
