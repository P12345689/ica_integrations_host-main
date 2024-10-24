# -*- coding: utf-8 -*-
"""
Graphviz tool for generating diagrams and retrieving information about the Graphviz integration.

This module provides tools that wrap the functionality from the main graphviz router.
"""

from langchain.agents import tool

# Import the generate_png function from the main router
from ..graphviz_router import generate_png


@tool
def generate_graphviz_diagram(syntax: str) -> str:
    """
    Tool for generating a Graphviz diagram from the provided syntax.

    Args:
        syntax (str): The Graphviz syntax (DOT language) to generate the diagram.

    Returns:
        str: The URL of the generated PNG file.

    Example:
        >>> result = generate_graphviz_diagram("digraph G { A -> B; B -> C; C -> A; }")
        >>> assert "http" in result and ".png" in result
    """
    return generate_png(syntax)


@tool
def get_graphviz_info() -> str:
    """
    Tool for getting information about the Graphviz integration.

    Returns:
        str: Information about the Graphviz integration.

    Example:
        >>> info = get_graphviz_info()
        >>> assert "Graphviz" in info
        >>> assert "generate diagrams" in info
    """
    return (
        "The Graphviz integration provides functionality to generate diagrams "
        "using the DOT language. It can create PNG images from Graphviz syntax "
        "and also supports natural language queries to generate diagrams."
    )


@tool
def graphviz_syntax_helper(diagram_type: str) -> str:
    """
    Tool for providing basic Graphviz syntax examples for different diagram types.

    Args:
        diagram_type (str): The type of diagram (e.g., "flowchart", "tree", "network").

    Returns:
        str: A basic Graphviz syntax example for the specified diagram type.

    Example:
        >>> result = graphviz_syntax_helper("flowchart")
        >>> assert "digraph" in result
        >>> assert "->" in result
    """
    examples = {
        "flowchart": """
digraph Flowchart {
    Start -> Process;
    Process -> Decision;
    Decision -> End [label="Yes"];
    Decision -> Process [label="No"];
}
""",
        "tree": """
digraph Tree {
    Root -> Branch1;
    Root -> Branch2;
    Branch1 -> Leaf1;
    Branch1 -> Leaf2;
    Branch2 -> Leaf3;
    Branch2 -> Leaf4;
}
""",
        "network": """
graph Network {
    Server1 -- Server2;
    Server1 -- Server3;
    Server2 -- Server4;
    Server3 -- Server4;
}
""",
    }
    return examples.get(
        diagram_type.lower(),
        "Diagram type not recognized. Available types: flowchart, tree, network.",
    )
