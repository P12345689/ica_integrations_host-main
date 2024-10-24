# -*- coding: utf-8 -*-

import pytest


@pytest.fixture()
def bar_test_data():
    return {
        "chart_type": "bar",
        "data": {"x": ["A", "B", "C"], "y": [10, 20, 30]},
        "title": "Test Bar Chart",
    }


@pytest.fixture()
def scatter_test_data():
    return {"x": [1, 2, 3], "y": [10, 20, 30]}


@pytest.fixture()
def bar_test_values():
    return {"x": ["A", "B", "C"], "y": [10, 20, 30]}


@pytest.fixture()
def mock_request_data():
    return {"query": "Generate a bar chart showing sales data"}


@pytest.fixture()
def bad_mock_request_data():
    return {"querty": "Generate a bar chart showing sales data"}


@pytest.fixture()
def bar_csv_test_data():
    return {
        "chart_type": "bar",
        "csv_data": "X,Y\nA,1\nB,4\nC,2",
        "sheet_name": "Employee Data",
        "title": "Sample Bar Chart CSV",
    }


@pytest.fixture()
def wrong_csv_test_data():
    return {
        "csv_data": "X,Y\nA,1\nB,4\nC,2",
        "sheet_name": "Employee Data",
        "title": "Sample Bar Chart CSV",
    }


@pytest.fixture()
def mock_correct_csv_data():
    return {
        "csv_data": "Name,Age,City\nJohn,30,New York\nJane,25,Los Angeles\nBob,35,Chicago",
        "sheet_name": "Employee_Data",
    }


@pytest.fixture()
def mock_wrong_csv_data():
    return {
        "dict_1": "Name,Age,City\nJohn,30,New York\nJane,25,Los Angeles\nBob,35,Chicago",
        "sheet_name": "Employee Data",
    }


@pytest.fixture()
def mock_csv_str():
    return "Name,Age,City\nJohn,30,New York\nJane,25,Los Angeles\nBob,35,Chicago"


@pytest.fixture()
def mock_non_csv_str():
    return 42


@pytest.fixture()
def mock_sheet_str():
    return "Sheet1"


@pytest.fixture()
def mock_experience_xlsx_query():
    return {
        "query": "Create an XLSX file with a list of 5 popular books, including their titles, authors, and publication years."
    }


@pytest.fixture()
def mock_experience_xlsx_query_bad_format():
    return {
        "data": "Create an XLSX file with a list of 5 popular books, including their titles, authors, and publication years."
    }
