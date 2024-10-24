import json
from typing import List,  Union
from app.tools.get_llamaindex_tools import get_tools

# tool list
# TODO: replace with *top 5* agents from the MRKL
ALL_TOOLS = get_tools(
    [
        "google_search_full",
        "google_search",
        "retrieve_website_content",
        "mermaid_create_diagram",
        "docbuilder_tool_markdown_to_pptx_docx",
        "summarize_text_tool",
        "get_system_time",
        "get_collections_tool",
        "query_documents_tool",
        "ai_vision_image_recognition",
        "pii_masker_tool",
        "get_prompts_tool",
        "get_assistants_tool",
        "wikipedia_search",
        "create_chart",
        "firefly_tool",
        "ask_prompt",
        "compare_tool",
        "assistant_executor_tool",
        "plantuml_tool",
        "code_splitter"
    ]
)

# Mapping for tool descriptions with emojis
TOOL_DESCRIPTIONS = {
    "google_search_full": "🔍 Google Search - Full",
    "google_search": "🔍 Google Search",
    "retrieve_website_content": "🌐 Retrieve Website Content",
    "mermaid_create_diagram": "📊 Mermaid Create Diagram",
    "docbuilder_tool_markdown_to_pptx_docx": "📄 Convert Markdown to PPTX/DOCX",
    "summarize_text_tool": "✍️ Summarize Text",
    "get_system_time": "🕒 Get System Time",
    "get_collections_tool": "📚 Get Collections",
    "query_documents_tool": "📑 Query Documents",
    "ai_vision_image_recognition": "🖼️ AI Vision - Image Recognition",
    "pii_masker_tool": "🔒 PII Masking Tool",
    "get_prompts_tool": "💡 Get Prompts",
    "get_assistants_tool": "🤖 Get Assistants",
    "wikipedia_search": "📖 Wikipedia Search",
    "create_chart": "📈 Create Chart",
    "firefly_tool": "🕵️ Firefly Tool",
    "ask_prompt": "❓ Ask Prompt",
    "compare_tool": "⚖️ Compare Tool",
    "assistant_executor_tool": "🤖 Assistant Executor Tool",
    "plantuml_tool": "🌱 PlantUML Diagram Generator",
    "code_splitter": "⛙ Code Splitter Tool"
}

def parse_tools_input(tools_input: Union[str, List[str]]) -> List[str]:
    """Parse tool names from input."""
    
    # check if we got a list of tools
    if isinstance(tools_input, list):
        # return the tools as a list
        return tools_input
    
    # check if the tools list is a string
    if isinstance(tools_input, str):
        try:
            # load the tools as json
            parsed = json.loads(tools_input)

            # checj if it's a list
            if isinstance(parsed, list):
                # return the parsed version
                return parsed
        except json.JSONDecodeError:
            # error, sto strip the tool list and return it
            return [tool.strip() for tool in tools_input.split(",") if tool.strip()]
        
    # no tools
    return []


def get_selected_tools(tool_names: Union[str, List[str]]) -> List[str]:
    """Retrieve selected tools based on tool names input."""
    parsed_tool_names = parse_tools_input(tool_names)

    # check if we have parsed tool names
    if not parsed_tool_names:
        # no parsed tool names, so return all tools
        return ALL_TOOLS
    
    # just return the parsed tool list
    return [tool for tool in ALL_TOOLS if tool.metadata.name in parsed_tool_names]


