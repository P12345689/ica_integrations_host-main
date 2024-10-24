# -*- coding: utf-8 -*-
"""
Pytest for chart route.

Description: Tests chart route.

Authors: Andrei Colhon
"""

from unittest import mock
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.routes.chart import chart_router
from app.routes.chart.chart_router import generate_chart
from app.server import app

client = TestClient(app)


def test_valid_bar_chart(bar_test_data):
    test_data = bar_test_data
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/system/chart/generate_chart/invoke", json=test_data, headers=headers
    )
    assert response.status_code == 200


def test_invalid_chart(bar_test_values):
    test_data = {
        "chart_type": "bad",
        "data": bar_test_values,
        "title": "Test Bad Chart",
    }
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/system/chart/generate_chart/invoke", json=test_data, headers=headers
    )
    assert response.status_code == 400


def test_invalid_data(bar_test_values):
    test_data = {
        "chart_type": 435,
        "data": bar_test_values,
        "title": "Test Bad Chart",
    }
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/system/chart/generate_chart/invoke", json=test_data, headers=headers
    )
    assert response.status_code == 422


def test_chartinputmodel(bar_test_values):
    cim = chart_router.ChartInputModel(
        chart_type="bar",
        data=bar_test_values,
        title="Bar Chart Showcase",
    )
    assert cim.chart_type == "bar"
    assert cim.data == bar_test_values
    assert cim.title == "Bar Chart Showcase"


def test_experienceinputmodel():
    eim = chart_router.ExperienceInputModel(query="build a chart for me")
    assert eim.query == "build a chart for me"


def test_responsemessagemodel():
    rmm = chart_router.ResponseMessageModel(message="the message", type="text")
    assert rmm.message == "the message"
    assert rmm.type == "text"


def test_outputmodel():
    response_message = chart_router.ResponseMessageModel(
        message="the message", type="text"
    )
    om = chart_router.OutputModel(
        status="success", invocationId="testId", response=[response_message]
    )
    assert om.status == "success"
    assert om.invocationId == "testId"
    assert om.response == [response_message]


def test_generate_bar_chart(bar_test_values):
    data = bar_test_values
    with (
        mock.patch("app.routes.chart.chart_router.plt.savefig") as mock_savefig,
        mock.patch("app.routes.chart.os.makedirs") as mock_makedirs,
    ):
        url = generate_chart("bar", data, "Bar Chart")
        mock_savefig.assert_called_once()
        mock_makedirs.assert_called_once()
        assert "http://127.0.0.1:8080/public/chart/chart_" in url


def test_generate_pie_chart():
    data = {"values": [30, 40, 30], "labels": ["A", "B", "C"]}
    with (
        mock.patch("app.routes.chart.chart_router.plt.savefig") as mock_savefig,
        mock.patch("app.routes.chart.os.makedirs") as mock_makedirs,
    ):
        url = generate_chart("pie", data, "Pie Chart")
        mock_savefig.assert_called_once()
        mock_makedirs.assert_called_once()
        assert "http://127.0.0.1:8080/public/chart/chart_" in url


def test_generate_line_chart(scatter_test_data):
    data = scatter_test_data
    with (
        mock.patch("app.routes.chart.chart_router.plt.savefig") as mock_savefig,
        mock.patch("app.routes.chart.os.makedirs") as mock_makedirs,
    ):
        url = generate_chart("line", data, "Line Chart")
        mock_savefig.assert_called_once()
        mock_makedirs.assert_called_once()
        assert "http://127.0.0.1:8080/public/chart/chart_" in url


def test_generate_scatter_chart(scatter_test_data):
    data = scatter_test_data
    with (
        mock.patch("app.routes.chart.chart_router.plt.savefig") as mock_savefig,
        mock.patch("app.routes.chart.os.makedirs") as mock_makedirs,
    ):
        url = generate_chart("scatter", data, "Scatter Chart")
        mock_savefig.assert_called_once()
        mock_makedirs.assert_called_once()
        assert "http://127.0.0.1:8080/public/chart/chart_" in url


def test_generate_histogram_chart():
    data = {"values": [1, 2, 2, 3, 3, 3]}
    with (
        mock.patch("app.routes.chart.chart_router.plt.savefig") as mock_savefig,
        mock.patch("app.routes.chart.os.makedirs") as mock_makedirs,
    ):
        url = generate_chart("histogram", data, "Histogram Chart")
        mock_savefig.assert_called_once()
        mock_makedirs.assert_called_once()
        assert "http://127.0.0.1:8080/public/chart/chart_" in url


def test_generate_chart_invalid_type(scatter_test_data):
    data = scatter_test_data
    with pytest.raises(ValueError) as exc_info:
        generate_chart("invalid_type", data, "Invalid Chart")
    assert "Unsupported chart type: invalid_type" in str(exc_info.value)


@pytest.mark.asyncio
async def test_generatechartroute_endpoint_success(bar_test_data):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        test_data = bar_test_data
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/chart/generate_chart/invoke", json=test_data, headers=headers
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_generatechartroutecsv_endpoint_success(bar_csv_test_data):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        test_data = bar_csv_test_data
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/chart/generate_csv_chart/invoke", json=test_data, headers=headers
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_generatechartroutecsv_endpoint_bad_data(wrong_csv_test_data):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        test_data = wrong_csv_test_data
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/chart/generate_csv_chart/invoke", json=test_data, headers=headers
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generatechartroutecsv_endpoint_bad_request():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        test_data = {
            "chart_type": "bad",
            "csv_data": "X,Y\nA,1\nB,4\nC,2",
            "sheet_name": "Employee Data",
            "title": "Sample Bar Chart CSV",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/chart/generate_csv_chart/invoke", json=test_data, headers=headers
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_generatechartexperience_endpoint_success(mock_request_data):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        with mock.patch(
            "app.routes.chart.chart_router.generate_chart"
        ) as mock_generate:
            query = mock_request_data
            headers = {
                "Content-Type": "application/json",
                "Integrations-API-Key": "dev-only-token",
            }
            response = await ac.post(
                "/experience/chart/generate_chart/invoke", json=query, headers=headers
            )
    assert response.status_code == 200
    assert "status" in response.text
    mock_generate.assert_called_once()


@pytest.mark.asyncio
async def test_generatechartexperience_endpoint_failure(bad_mock_request_data):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        with mock.patch(
            "app.routes.chart.chart_router.generate_chart"
        ) as mock_generate:
            query = bad_mock_request_data
            headers = {
                "Content-Type": "application/json",
                "Integrations-API-Key": "dev-only-token",
            }
            response = await ac.post(
                "/experience/chart/generate_chart/invoke", json=query, headers=headers
            )
    assert response.status_code == 422
