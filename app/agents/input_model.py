import json
import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field, ValidationError
from fastapi import HTTPException, Request

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class InputModel(BaseModel):
    """Model for incoming request data to specify query, optional context, tools to use, model configuration, and prompt template."""
    # query
    query: str = Field(description="Query to execute against the agent.")
    
    # context
    context: Optional[str] = Field(default=None, description="Stringified JSON of context items.")
    use_context: bool = Field(default=False, description="Whether to use the provided context.")

    # tools list
    tools: Union[str, List[str]] = Field(
        default=[],
        description="List of tool names to use, or a string of comma-separated tool names, or a JSON string of tool names. If empty, all tools will be used.",
    )

    # llm override
    llm_override: Optional[Tuple[str, str]] = Field(
        default=None,
        description="Tuple of (model_host, model_name) to override default model.",
    )

    # prompt template
    prompt_template: Optional[str] = Field(default=None, description="Custom prompt template to use for the agent.")

async def get_input_data(request: Request):
    try:
        # get the data as json
        data: Dict[str, Any] = await request.json()

        # get the input data
        input_data = InputModel(**data)

        # log some debug
        log.debug(f"Validated input data: {input_data}")

        # return the input model
        return input_data
    except json.JSONDecodeError:
        # log the error and raise the exception
        log.error("Invalid JSON received")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValidationError as e:
        # log the error and raise the exception
        log.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=json.loads(e.json()))

