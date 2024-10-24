# -*- coding: utf-8 -*-
"""
Pytest for test_cases_agent route.

Description: Tests test_cases_agent route.

Authors: Shrishti
"""

# tests/test_manual_test_cases.py
import pytest
import json
from httpx import AsyncClient
from app.server import app
from app.routes.test_cases_agent.test_cases_agent_router import *
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import AsyncMock, mock_open, patch
from io import BytesIO

client = TestClient(app)

# Mock data for testing
mock_input_model_data = {
    "input": [""],
}

mock_output_model_data = {
    "status": "success",
    "invocationId": "12345",
    "response": [
        {"message": "File generated successfully", "type": "text"}
    ],
}


########## test cases for load_config() ##########


def test_load_config_success():
    """Test loading the config file successfully."""
    mock_config_data = {"key": "value"}  # Example valid config data

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_config_data))), \
         patch("json.load", return_value=mock_config_data):
        result = load_config()
        assert result == mock_config_data


def test_load_config_file_not_found():
    """Test the scenario where the config file is not found."""
    with patch("builtins.open", side_effect=FileNotFoundError), \
         patch("app.routes.test_cases_agent.test_cases_agent_router.log.warning") as mock_log:  # Mocking log to avoid real logging
        with pytest.raises(HTTPException) as exc_info:
            load_config()

        # Verify that the function raises the correct HTTPException
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error"

        # Ensure the log warning is called with the correct message
        mock_log.assert_called_once_with(f"Configuration file not found at {CONFIG_FILE_PATH}")


def test_load_config_invalid_json():
    """Test the scenario where the config file contains invalid JSON."""
    invalid_json_data = "{invalid json}"
    config_file_path = "path/to/config.json"  # test with wrong file path

    with patch("builtins.open", mock_open(read_data=invalid_json_data)), \
         patch("json.load", side_effect=json.JSONDecodeError("Expecting value", invalid_json_data, 0)), \
         patch("app.routes.test_cases_agent.test_cases_agent_router.log.error") as mock_log:
        with pytest.raises(HTTPException) as exc_info:
            load_config()

        # Verify that the function raises the correct HTTPException 
        # such as encountering an invalid JSON format or a missing configuration file.
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error"

        # Ensure the log error is called with the correct message
        mock_log.assert_called_once_with(f"Invalid JSON in configuration file {CONFIG_FILE_PATH}") 


########## test cases for load_assistant_config() ##########


@pytest.mark.asyncio
async def test_load_assistant_config_with_assistant_id():
    # Mock load_config to return a sample configuration
    sample_config = {"mtc_assistant_id": "12345"}
    
    with patch("app.routes.test_cases_agent.test_cases_agent_router.load_config", return_value=sample_config):
        mtc_assistant_id, config = await load_assistant_config("test_id")
        
        assert mtc_assistant_id == "test_id"
        assert config == sample_config


@pytest.mark.asyncio
async def test_load_assistant_config_without_assistant_id():
    # Mock load_config to return a sample configuration
    sample_config = {"mtc_assistant_id": "12345"}
    
    with patch("app.routes.test_cases_agent.test_cases_agent_router.load_config", return_value=sample_config):
        mtc_assistant_id, config = await load_assistant_config(None)
        
        assert mtc_assistant_id == "12345"
        assert config == sample_config


@pytest.mark.asyncio
async def test_load_assistant_config_raises_exception():
    # Mock load_config to raise an exception
    with patch("app.routes.test_cases_agent.test_cases_agent_router.load_config", side_effect=Exception("Some error")):
        with patch("app.routes.test_cases_agent.test_cases_agent_router.log.error") as mock_log_error:
            with pytest.raises(HTTPException) as exc_info:
                await load_assistant_config(None)
                
            # Check that the exception is the correct one
            assert exc_info.value.status_code == 500
            assert exc_info.value.detail == "Internal server error"
            
            # Ensure the error was logged
            mock_log_error.assert_called_once_with("Error while fetching the assistantId for the inputType: Some error")


########## test cases for execute_assistant_executor() ##########


@pytest.mark.asyncio
async def test_execute_assistant_executor_success():
    input_list = [{"user_story": "test story 1"}, {"user_story": "test story 2"}]
    assistant_id = "test_assistant"

    expected_responses = [
        {"message": "Response 1", "type": "text"},
        {"message": "Response 2", "type": "text"}
    ]

    # Patch the invoke_assistant_executor to return mocked results
    with patch("app.routes.test_cases_agent.test_cases_agent_router.invoke_assistant_executor", side_effect=expected_responses):
        responses = await execute_assistant_executor(input_list, assistant_id)
        assert responses == expected_responses


@pytest.mark.asyncio
async def test_execute_assistant_executor_empty_list():
    input_list = []
    assistant_id = "test_assistant"

    responses = await execute_assistant_executor(input_list, assistant_id)
    assert responses == []  # Expect empty result if input list is empty


@pytest.mark.asyncio
async def test_execute_assistant_executor_internal_error(): 
    input_list = [{"user_story": "test story"}]
    assistant_id = "test_assistant"

    # Patch invoke_assistant_executor to raise an exception
    with patch("app.routes.test_cases_agent.test_cases_agent_router.invoke_assistant_executor", side_effect=HTTPException(status_code=500, detail="Internal server error")):
        with pytest.raises(HTTPException) as exc_info:
            await execute_assistant_executor(input_list, assistant_id)
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal server error"


@pytest.mark.asyncio
async def test_execute_assistant_executor_json_formatting():  # This testcase verifies whether the JSON object (a dictionary) from input_list is converted into a string
    input_list = [{"key1": "value1", "key2": "value2"}]
    assistant_id = "test_assistant"

    # The expected formatted item structure (ignoring spaces and newlines)
    expected_substring = "'key1': 'value1'"
    
    # Patch the invoke_assistant_executor to capture the argument
    with patch("app.routes.test_cases_agent.test_cases_agent_router.invoke_assistant_executor") as mock_invoke:
        await execute_assistant_executor(input_list, assistant_id)

        # Extract the formatted item from the mock call
        formatted_item = mock_invoke.call_args[0][1]
        
        # Instead of comparing the entire string, check key-value pairs and structure
        assert "'key1': 'value1'" in formatted_item
        assert "'key2': 'value2'" in formatted_item
        assert '{' not in formatted_item
        assert '}' not in formatted_item


########## test cases for invoke_assistant_executor() ##########


@pytest.mark.asyncio
async def test_invoke_assistant_executor_success():
    # Mock `assistant_executor` to return a successful response
    with patch('app.routes.test_cases_agent.test_cases_agent_router.assistant_executor', new_callable=AsyncMock) as mock_assistant_executor:
        mock_assistant_executor.return_value = {
            "status": "success",
            "invocationId": "12345",
            "response": [{"message": "Success", "type": "text"}]
        }

        response = await invoke_assistant_executor("assistant_id_1", "formatted_item_1")

        assert response == {
            "status": "success",
            "invocationId": "12345",
            "response": [{"message": "Success", "type": "text"}]
        }
        mock_assistant_executor.assert_awaited_once_with({
            "assistant_id": "assistant_id_1",
            "prompt": "formatted_item_1"
        })


@pytest.mark.asyncio
async def test_invoke_assistant_executor_failure():
    # Mock `assistant_executor` to raise an exception
    with patch('app.routes.test_cases_agent.test_cases_agent_router.assistant_executor', new_callable=AsyncMock) as mock_assistant_executor:
        mock_assistant_executor.side_effect = Exception("Internal error")

        with pytest.raises(Exception, match="Internal error"):
            await invoke_assistant_executor("assistant_id_1", "formatted_item_1")


@pytest.mark.asyncio
async def test_invoke_assistant_executor_invalid_json():
    # Test case to check handling of invalid JSON in the request
    with patch('app.routes.test_cases_agent.test_cases_agent_router.assistant_executor', new_callable=AsyncMock) as mock_assistant_executor:
        mock_assistant_executor.side_effect = Exception("Invalid JSON")

        with pytest.raises(Exception, match="Invalid JSON"):
            await invoke_assistant_executor("assistant_id_1", "invalid_formatted_item")


@pytest.mark.asyncio
async def test_invoke_assistant_executor_empty_response():
    # Mock `assistant_executor` to return an empty response
    with patch('app.routes.test_cases_agent.test_cases_agent_router.assistant_executor', new_callable=AsyncMock) as mock_assistant_executor:
        mock_assistant_executor.return_value = {}

        response = await invoke_assistant_executor("assistant_id_1", "formatted_item_1")

        assert response == {}
        mock_assistant_executor.assert_awaited_once_with({
            "assistant_id": "assistant_id_1",
            "prompt": "formatted_item_1"
        })


########## test cases for parse_request() ##########


@pytest.mark.asyncio
async def test_parse_request_valid_input():
    # Arrange
    mock_csv_input = "Issue Type,Summary,Description,Priority\nStory,Sample Story,Description,Medium"
    mock_json_output = [{"Issue Type": "Story", "Summary": "Sample Story", "Description": "Description", "Priority": "Medium"}]
    
    request_body = {
        "input": mock_csv_input,
        "mtcAssistantId": "1234"
    }
    
    request = AsyncMock(spec=Request)
    request.body.return_value = json.dumps(request_body).encode("utf-8")

    with patch("app.routes.test_cases_agent.test_cases_agent_router.csv_to_json", return_value=mock_json_output) as mock_csv_to_json, \
         patch("app.routes.test_cases_agent.test_cases_agent_router.transform_json_data", return_value=mock_json_output) as mock_transform_json_data:
        
        # Act
        user_story_list, mtc_assistant_id = await parse_request(request)

        # Assert
        assert user_story_list == mock_json_output
        assert mtc_assistant_id == "1234"
        mock_csv_to_json.assert_called_once_with(mock_csv_input)
        mock_transform_json_data.assert_called_once_with(mock_json_output)


@pytest.mark.asyncio
async def test_parse_request_invalid_json():
    # Arrange
    request_body = "invalid json"
    
    request = AsyncMock(spec=Request)
    request.body.return_value = request_body.encode("utf-8")

    # Act & Assert
    with pytest.raises(json.JSONDecodeError):
        await parse_request(request)


########## test cases for generate_excel_from_xlsx_builder() ##########


# Constants used in tests
MOCK_CSV_STRING = "name,age\nJohn,30\nJane,25"
MOCK_FILE_NAME = "test_file.xlsx"
MOCK_OUTPUT = {"file": "mock_xlsx_content"}

@pytest.mark.asyncio
@patch("app.routes.test_cases_agent.test_cases_agent_router.httpx.AsyncClient")
async def test_generate_excel_success(mock_async_client):
    """Test a successful response from the xlsx_builder API."""
    
    # Mocking the response
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_OUTPUT
    
    # Setting the mock to return the mocked response
    mock_async_client.return_value.__aenter__.return_value.post.return_value = mock_response

    # Mocking the OutputModel to return the expected result when model_validate is called
    with patch("app.routes.test_cases_agent.test_cases_agent_router.OutputModel.model_validate") as mock_model_validate:
        mock_model_validate.return_value = MOCK_OUTPUT
        
        # Call the function
        result = await generate_excel_from_xlsx_builder(MOCK_CSV_STRING, MOCK_FILE_NAME)
        
        # Assertions
        mock_async_client.return_value.__aenter__.return_value.post.assert_called_once_with(
            f"{SERVER_NAME}/system/xlsx_builder/generate_xlsx/invoke",
            headers={"Accept": "application/json", "Content-Type": "application/json", "Integrations-API-Key": API_KEY},
            json={"csv_data": {"Sheet1": MOCK_CSV_STRING}, "file_name": MOCK_FILE_NAME}
        )
        assert result == MOCK_OUTPUT


# The function is making an async HTTP request to the xlsx_builder API, and the API may return an invalid response 400 or 500 instead of 200
@pytest.mark.asyncio
@patch("app.routes.test_cases_agent.test_cases_agent_router.httpx.AsyncClient")
async def test_generate_excel_invalid_response(mock_async_client):
    """Test an invalid response from the xlsx_builder API."""
    
    # Mocking the response
    mock_response = AsyncMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Invalid response"}
    
    # Setting the mock to return the mocked response
    mock_async_client.return_value.__aenter__.return_value.post.return_value = mock_response

    # Call the function
    with pytest.raises(Exception):
        await generate_excel_from_xlsx_builder(MOCK_CSV_STRING, MOCK_FILE_NAME)


########## test cases for generate_file_path() ##########


@pytest.mark.asyncio
async def test_generate_file_path_success():
    """Test the successful generation of file path and URL."""
    
    mock_uuid = "test-uuid"
    expected_file_name = f"xlsx_{mock_uuid}.xlsx"
    expected_file_path = f"{PUBLIC_DIR}/{expected_file_name}"
    expected_file_url = f"{SERVER_NAME}/{expected_file_path}"

    # Patch uuid4 and os.makedirs to simulate environment
    with patch("app.routes.test_cases_agent.test_cases_agent_router.uuid4", return_value=mock_uuid), \
         patch("os.makedirs") as mock_makedirs:
        
        file_name, file_url = await generate_file_path()

        # Assert file name and URL are generated correctly
        assert file_name == expected_file_name
        assert file_url == expected_file_url
        
        # Assert that os.makedirs is called with the correct path
        mock_makedirs.assert_called_once_with(os.path.dirname(expected_file_path), exist_ok=True)


@pytest.mark.asyncio
async def test_generate_file_path_directory_creation(): 
    """Test that the directory is created if it does not exist."""

    mock_uuid = "test-uuid"
    expected_file_name = f"xlsx_{mock_uuid}.xlsx"
    expected_file_path = f"{PUBLIC_DIR}/{expected_file_name}"

    # Patch uuid4 and os.makedirs to simulate environment
    with patch("app.routes.test_cases_agent.test_cases_agent_router.uuid4", return_value=mock_uuid), \
         patch("os.makedirs") as mock_makedirs:
        
        await generate_file_path()

        # Assert os.makedirs is called with correct directory
        mock_makedirs.assert_called_once_with(os.path.dirname(expected_file_path), exist_ok=True)


@pytest.mark.asyncio
async def test_generate_file_path_unique_file_name():
    """Test that a unique file name is generated every time."""

    # Generate two different mock UUIDs to simulate different runs
    mock_uuid_1 = "uuid-1"
    mock_uuid_2 = "uuid-2"

    with patch("app.routes.test_cases_agent.test_cases_agent_router.uuid4", side_effect=[mock_uuid_1, mock_uuid_2]):
        file_name_1, _ = await generate_file_path()
        file_name_2, _ = await generate_file_path()

        # Assert that the two file names are different
        assert file_name_1 != file_name_2
        assert file_name_1 == f"xlsx_{mock_uuid_1}.xlsx"
        assert file_name_2 == f"xlsx_{mock_uuid_2}.xlsx"


@pytest.mark.asyncio
async def test_generate_file_path_makedirs_failure():
    """Test that an error is raised when os.makedirs fails."""

    mock_uuid = "test-uuid"
    with patch("app.routes.test_cases_agent.test_cases_agent_router.uuid4", return_value=mock_uuid), \
         patch("os.makedirs", side_effect=OSError("Permission denied")) as mock_makedirs:
        
        with pytest.raises(OSError, match="Permission denied"):
            await generate_file_path()
        
        mock_makedirs.assert_called_once()


########## test cases for get_excel_with_testcases() ##########


@pytest.mark.asyncio
async def test_get_excel_with_testcases_config_error():
    # Arrange
    mtcAssistantId = "invalid_assistant_id"
    userStoryList = InputModel(input=["story_1", "story_2"])
    file_name = "test_excel.xlsx"

    # Act and Assert
    with pytest.raises(HTTPException) as exc_info:
        await get_excel_with_testcases(mtcAssistantId, userStoryList, file_name)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal server error"


@pytest.mark.asyncio
async def test_get_excel_with_testcases_executor_error():
    # Arrange
    mtcAssistantId = "assistant_id_1"
    userStoryList = InputModel(input=["invalid_story"])
    file_name = "test_excel.xlsx"

    # Act and Assert
    with pytest.raises(HTTPException) as exc_info:
        await get_excel_with_testcases(mtcAssistantId, userStoryList, file_name)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal server error"
