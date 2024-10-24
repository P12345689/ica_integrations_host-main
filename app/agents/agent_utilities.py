# Mapping for tool descriptions with emojis
import json
from typing import Any, Dict, Optional

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

# build response
def build_response(
    status: str,
    invocation_id: str,
    event_counter: int,
    is_final_event: bool,
    message: str,
    response_type: str = "final_answer",
    title: str = "Final Answer",
    generator: str = "agent_llamaindex"
) -> str:
    """Build a JSON response string."""
    response = {
        "status": status,
        "invocation_id": invocation_id,
        "event_id": event_counter,
        "is_final_event": is_final_event,
        "response": [
            {
                "message": message,
                "properties": {
                    "response_type": response_type,
                    "title": title,
                    "generator": generator,
                },
                "type": "text"
            }
        ]
    }

    # return the json
    return json.dumps(response) + "\n"

def clean_message(message: str, response_type: str, config: Optional[Dict[str, Any]] = None) -> str:
    """
    Cleans up the message according to the rules specified in the config.
    Args:
        message (str): The original message content.
        response_type (str): The type of response ('thought', 'action', etc.).
        config (dict): A dictionary containing the cleanup rules.
    Returns:
        str: The cleaned-up message.
    """
    if config is None:
        # Default cleanup rules
        config = {
            'thought': {
                'remove_prefixes': ['Thought: '],
                'remove_lines_starting_with': ['Action', 'Action Input']
            },
            'action': {
                'remove_lines_starting_with': ['Action: '],
                'remove_observation': True
            }
        }

    rules = config.get(response_type, {})

    # Remove specified prefixes
    prefixes = rules.get('remove_prefixes', [])
    for prefix in prefixes:
        if message.startswith(prefix):
            message = message[len(prefix):]

    # Remove lines starting with specified strings
    lines = message.splitlines()
    lines_to_keep = []
    remove_starts = rules.get('remove_lines_starting_with', [])
    for line in lines:
        if not any(line.strip().startswith(s) for s in remove_starts):
            lines_to_keep.append(line)
    message = '\n'.join(lines_to_keep)

    # Remove observation part if specified
    if rules.get('remove_observation', False):
        # Assuming that the observation is after 'Observation:' in the message
        if 'Observation:' in message:
            message = message.split('Observation:')[0].strip()

    return message