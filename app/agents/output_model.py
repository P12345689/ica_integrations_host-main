from typing import Dict, List
from pydantic import BaseModel, Field

class OutputModel(BaseModel):
    """Output format for streamed and non-streamed data."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[Dict[str, str]]