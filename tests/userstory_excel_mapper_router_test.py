# # -*- coding: utf-8 -*-
# """
# Pytest for userstory excel mapper route.

# Description: Tests userstory excel mapper route.

# Authors: Megha Suresh
# """

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import mock_open, patch, AsyncMock
from uuid import uuid4
from app.routes.userstory_excel_mapper.userstory_excel_mapper_router import *
# from app.models import OutputModel, ResponseMessageModel


# Create a FastAPI instance
app = FastAPI()
add_custom_routes(app)

# Test client for FastAPI
client = TestClient(app)

@pytest.fixture
def mock_get_excel_with_userstories():
    with patch("app.routes.userstory_excel_mapper.userstory_excel_mapper_router.get_excel_with_userstories", new_callable=AsyncMock) as mock_excel:
        mock_excel.return_value = AsyncMock(response=[{"message": "Excel generated successfully"}])
        yield mock_excel

# Example request mock for successful case
class MockRequest:
    def __init__(self, epic_to_us_assistant_id, us_detail_assistant_id, input_type):
        self.epicToUsAssistantId = epic_to_us_assistant_id
        self.usDetailAssistantId = us_detail_assistant_id
        self.inputType = input_type


# Mock config for successful case
mock_config = {
    "UserStory": {
        "epic_us_assistant_id": "22113",
        "us_detail_assistant_id": "8352"
    }
}

@pytest.fixture
def mock_load_config():
    with patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.load_config', return_value=mock_config):
        yield

def test_generate_excel_with_userstories(mock_get_excel_with_userstories):
    # Simulate a request payload
    request_payload = {
        "inputType": "UserStory",
        "input": "Business Objective: Creating an Electronic Census System app for Republic of Bolumbia’s Department of Statistics in the retail domain, to enhance census collecting experience \n - Requirement: \n Login \n Profile \n Submit Forms \n Handle Records \n Peak load management \n Compliance \n Data handling \n Publishing the results"
    }

    # Invoke the API
    response = client.post("/system/us_excel_mapper/generate_excel/invoke", json=request_payload)

    # Verify the initial response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "processing"
    assert "invocationId" in response_data
    assert len(response_data["response"]) == 1
    assert response_data["response"][0]["message"].startswith("\nThe generation of user stories has started")
    

def test_load_config_success():
    # Mock the contents of the config file
    mock_config_data = {"key": "value"}
    
    # Use mock_open to simulate opening and reading the config file
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_config_data))):
        # Call the function
        config = load_config()
        
        # Verify that the config was loaded correctly
        assert config == mock_config_data


def test_load_config_file_not_found():
    # Simulate FileNotFoundError by patching 'open' and making it raise the error
    with patch("builtins.open", side_effect=FileNotFoundError):
        # Assert that an HTTPException is raised
        with pytest.raises(HTTPException) as exc_info:
            load_config()

        # Check that the exception is a 500 Internal Server Error
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error"

def test_load_config_invalid_json():
    # Simulate invalid JSON in the config file
    invalid_json_data = "{invalid json}"

    # Patch 'open' to return the invalid JSON
    with patch("builtins.open", mock_open(read_data=invalid_json_data)):
        # Patch 'json.load' to raise a JSONDecodeError
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            # Assert that an HTTPException is raised
            with pytest.raises(HTTPException) as exc_info:
                load_config()

            # Check that the exception is a 500 Internal Server Error
            assert exc_info.value.status_code == 500
            assert exc_info.value.detail == "Internal server error"


@pytest.mark.asyncio
async def test_parse_request_success():
    # Mock the request body
    request_body = json.dumps({
        "input": "single value",
        "inputType": "UserStory"
    }).encode("utf-8")

    # Mock the request object and its body method
    mock_request = AsyncMock(Request)
    mock_request.body = AsyncMock(return_value=request_body)

    # Expected input after processing
    expected_input_model = InputModel(input=["single value"], inputType="UserStory"), False

    # Call the function and validate the result
    result = await parse_request(mock_request)
    print(f"**result**{result}")
    print(f"**expecr**{expected_input_model}")

    assert result == expected_input_model

@pytest.mark.asyncio
async def test_parse_request_invalid_json():
    # Simulate an invalid JSON in the request body
    invalid_json_body = b"{invalid json}"

    # Mock the request object and its body method
    mock_request = AsyncMock(Request)
    mock_request.body = AsyncMock(return_value=invalid_json_body)

    # Assert that JSONDecodeError is raised
    with pytest.raises(json.JSONDecodeError):
        await parse_request(mock_request)

@pytest.mark.asyncio
async def test_parse_request_invalid_model():
    # Mock the request body with valid JSON but invalid for InputModel schema
    invalid_model_data = json.dumps({
        "input": ["valid array"],
        # Missing required fields for InputModel
    }).encode("utf-8")

    # Mock the request object and its body method
    mock_request = AsyncMock(Request)
    mock_request.body = AsyncMock(return_value=invalid_model_data)

    # Assert that a validation error occurs
    with pytest.raises(ValueError):  # ValueError or ValidationError from Pydantic
        await parse_request(mock_request)

@pytest.mark.asyncio
async def test_load_assistant_config_success(mock_load_config):
    # Create a mock request
    mock_request = MockRequest("22113", "8352", "UserStory")

    # Call the function
    epic_us_assistant_id, us_detail_assistant_id, config = load_assistant_config(mock_request)

    # Assertions
    assert epic_us_assistant_id == "22113"
    assert us_detail_assistant_id == "8352"
    assert config == mock_config


@pytest.mark.asyncio
async def test_load_assistant_config_fallback_success(mock_load_config):
    # Create a mock request where epicToUsAssistantId is not "epic_us_assistant_id"
    mock_request = MockRequest("1234", "4567", "UserStory")

    # Call the function
    epic_us_assistant_id, us_detail_assistant_id, config = load_assistant_config(mock_request)

    # Assertions
    assert epic_us_assistant_id == "1234"
    assert us_detail_assistant_id == "4567"
    assert config == mock_config


@pytest.mark.asyncio
async def test_load_assistant_config_error():
    with patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.load_config', side_effect=Exception("Config error")):
        # Create a mock request
        mock_request = MockRequest("epic_us_assistant_id", "us_detail_id_789", "some_input_type")

        # Assert that HTTPException is raised
        with pytest.raises(HTTPException):
            load_assistant_config(mock_request)


# Mock responses for successful execution
mock_responses = [
    {"response": "response_1"},
    {"response": "response_2"},
    {"response": "response_3"},
]

# Mock input list
input_list = ["req_1", "req_2", "req_3"]


@pytest.mark.asyncio
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.invoke_assistant_executor', return_value={"response": "mock_response"})
async def test_execute_assistant_executor_success(mock_invoke_assistant_executor):
    assistant_id = "test_assistant_id"

    # Call the function
    responses = await execute_assistant_executor(input_list, assistant_id)

    # Assertions
    assert len(responses) == len(input_list)
    assert all(response == {"response": "mock_response"} for response in responses)
    mock_invoke_assistant_executor.assert_called_with(assistant_id, "req_3")


@pytest.mark.asyncio
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.invoke_assistant_executor')
async def test_execute_assistant_executor_failure(mock_invoke_assistant_executor):
    assistant_id = "test_assistant_id"
    mock_invoke_assistant_executor.side_effect = Exception("Invoke error")

    # Call the function and assert HTTPException is raised
    with pytest.raises(HTTPException):
        await execute_assistant_executor(input_list, assistant_id)

    mock_invoke_assistant_executor.assert_called()


# Mock data
mock_content_request = InputModel(input=["Business Objective: Creating an Electronic Census System app for Republic of Bolumbia’s Department of Statistics in the retail domain, to enhance census collecting experience \n - Requirement: \n Login \n Profile \n Submit Forms"], inputType="UserStory")
mock_assistant_config = {
    "epic_us_assistant_id": "22113",
    "us_detail_assistant_id": "8352"
}


mock_one_line_user_stories = [OutputModel(status='success', invocationId='3916e92b-5815-46c1-9e57-02fd0d1e20a6', response=[ResponseMessageModel(message="\nUser Stories:\n  **Login**\n  1. User story one.\n  2. User story two.", type='text')])]
mock_detailed_user_stories = [
    {"response": [{"message": "Detailed story one"}, {"message": "Detailed story two"}]}
]
mock_csv_string = "csv_content"
mock_xlsx_response = OutputModel(status="success", invocationId="123", response=[])


@pytest.mark.asyncio
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.load_assistant_config', return_value=("epic_us_id", "detail_us_id", {}))
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.execute_assistant_executor')
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.process_content_into_csv', return_value=mock_csv_string)
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.generate_excel_from_xlsx_builder', return_value=mock_xlsx_response)
async def test_get_excel_with_userstories_success(mock_generate_excel_from_xlsx_builder, mock_process_content_into_csv, mock_execute_assistant_executor, mock_load_assistant_config):
    # Mock behavior for `execute_assistant_executor`
    mock_execute_assistant_executor.side_effect = [
        mock_one_line_user_stories,  # Response for first call
        mock_detailed_user_stories   # Response for second call
    ]
    
    # Call the function
    response = await get_excel_with_userstories(mock_content_request, "mock_file_name")
    
    # Assertions
    assert response == mock_xlsx_response
    mock_load_assistant_config.assert_called_once_with(mock_content_request)
    mock_execute_assistant_executor.assert_called_with(["1. User story one.", "2. User story two."], "detail_us_id")
    mock_process_content_into_csv.assert_called_once_with(mock_detailed_user_stories, {}, "UserStory")
    mock_generate_excel_from_xlsx_builder.assert_called_once_with(mock_csv_string, "mock_file_name")


@pytest.mark.asyncio
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.load_assistant_config', side_effect=Exception("Config error"))
async def test_get_excel_with_userstories_load_assistant_config_failure(mock_load_assistant_config):
    # Call the function and assert HTTPException is raised
    with pytest.raises(HTTPException):
        await get_excel_with_userstories(mock_content_request, "mock_file_name")


@pytest.mark.asyncio
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.load_assistant_config', return_value=("epic_us_id", "detail_us_id", {}))
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.execute_assistant_executor', side_effect=Exception("Executor error"))
async def test_get_excel_with_userstories_execute_assistant_executor_failure(mock_execute_assistant_executor, mock_load_assistant_config):
    # Call the function and assert HTTPException is raised
    with pytest.raises(HTTPException):
        await get_excel_with_userstories(mock_content_request, "mock_file_name")


@pytest.mark.asyncio
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.load_assistant_config', return_value=("epic_us_id", "detail_us_id", {}))
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.execute_assistant_executor', return_value=mock_one_line_user_stories)
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.process_content_into_csv', side_effect=Exception("CSV processing error"))
async def test_get_excel_with_userstories_process_content_into_csv_failure(mock_process_content_into_csv, mock_execute_assistant_executor, mock_load_assistant_config):
    # Call the function and assert HTTPException is raised
    with pytest.raises(HTTPException):
        await get_excel_with_userstories(mock_content_request, "mock_file_name")


@pytest.mark.asyncio
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.load_assistant_config', return_value=("epic_us_id", "detail_us_id", {}))
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.execute_assistant_executor', return_value=mock_one_line_user_stories)
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.process_content_into_csv', return_value=mock_csv_string)
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.generate_excel_from_xlsx_builder', side_effect=Exception("Excel generation error"))
async def test_get_excel_with_userstories_generate_excel_from_xlsx_builder_failure(mock_generate_excel_from_xlsx_builder, mock_process_content_into_csv, mock_execute_assistant_executor, mock_load_assistant_config):
    # Call the function and assert HTTPException is raised
    with pytest.raises(HTTPException):
        await get_excel_with_userstories(mock_content_request, "mock_file_name")


mock_detailed_user_stories2 = [OutputModel(status='success', invocationId='3916e92b-5815-46c1-9e57-02fd0d1e20a6', response=[ResponseMessageModel(message="Here is the generated user story:\n\n**Title:** Title1\n\n**User Story:**\nUser Story1\n\n**Priority:** High\n\n**Classification:** Account Management\n\n**Constraints:**\n1. Con1. \n\n**Acceptance Criteria:**\n\n1. Ac1\n\n**Validation Rules:**\n\n1. VR1. \n\n**Non-Functional Requirements (NFRs):**\n\n1. Nfr1.", type='text')]), OutputModel(status='success', invocationId='3916e92b-5815-46c1-9e57-02fd0d1e20a6', response=[ResponseMessageModel(message="Here is the generated user story:\n\n**Title:** Title1\n\n**User Story:**\nUser Story2\n\n**Priority:** High\n\n**Classification:** Account Management\n\n**Constraints:**\n1. Con2. \n\n**Acceptance Criteria:**\n\n1. Ac2\n\n**Validation Rules:**\n\n1. VR2. \n\n**Non-Functional Requirements (NFRs):**\n\n1. Nfr2.", type='text')])]
mock_csv_string2 = "Issue Type,Summary,Description,Priority,Classification,Acceptance Criteria\r\nStory,Title1,User Story1,High,Account Management,\"Constraints:\n1. Con1.\n\nAcceptance Criteria:\n1. Ac1\n\nValidation Rules:\n1. VR1.\n\nNon-Functional Requirements (NFRs):\n1. Nfr1.\"\r\nStory,Title1,User Story2,High,Account Management,\"Constraints:\n1. Con2.\n\nAcceptance Criteria:\n1. Ac2\n\nValidation Rules:\n1. VR2.\n\nNon-Functional Requirements (NFRs):\n1. Nfr2.\"\r\n"

@pytest.mark.asyncio
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.execute_assistant_executor')
@patch('app.routes.userstory_excel_mapper.userstory_excel_mapper_router.generate_excel_from_xlsx_builder', return_value=mock_xlsx_response)
async def test_get_excel_with_userstories_success_csv_util(mock_generate_excel_from_xlsx_builder, mock_execute_assistant_executor):
    # Mock behavior for `execute_assistant_executor`
    mock_execute_assistant_executor.side_effect = [
        mock_one_line_user_stories,  # Response for first call
        mock_detailed_user_stories2   # Response for second call
    ]
    
    # Call the function
    response = await get_excel_with_userstories(mock_content_request, "mock_file_name")
    
    # Assertions
    assert response == mock_xlsx_response
    mock_execute_assistant_executor.assert_called_with(["1. User story one.", "2. User story two."], "8352")
    mock_generate_excel_from_xlsx_builder.assert_called_once_with(mock_csv_string2, "mock_file_name")