# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Parse python grammar
"""

import ast

import ply.lex as lex
import ply.yacc as yacc

# Define the tokens
tokens = ("CODEBLOCK", "POSSIBLECODE")

# Lexer states to manage code blocks
states = (("codeblock", "exclusive"),)


# Lexer rules
def t_start_codeblock(t):
    r"```"
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.begin("codeblock")


def t_codeblock_end(t):
    r"```"
    t.value = t.lexer.lexdata[t.lexer.code_start : t.lexer.lexpos - 3]
    t.type = "CODEBLOCK"
    t.lexer.lineno += t.value.count("\n")
    t.lexer.begin("INITIAL")
    return t


def t_codeblock_content(t):
    r".|\n"


def t_INITIAL_POSSIBLECODE(t):
    r"[ \t]*def[ \t]+[a-zA-Z_][a-zA-Z0-9_]*[ \t]*\(.*?\):|[ \t]*class[ \t]+[a-zA-Z_][a-zA-Z0-9_]*[ \t]*\(.*?\):"
    return t


def t_ANY_error(t):
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


# Parser rules
def p_document(p):
    """document : elements"""
    p[0] = p[1]


def p_elements_codeblocks(p):
    """elements : elements element
    | element
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_element(p):
    """element : CODEBLOCK
    | POSSIBLECODE
    """
    p[0] = p[1]


def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()


def parse_markdown(input_string: str) -> list:
    """
    Parses the given markdown text and extracts Python code blocks and possible standalone Python code snippets.

    Args:
        input_string (str): The markdown text to parse.

    Returns:
        list: A list of valid Python code blocks and snippets.

    Examples:
        >>> test_input = \"\"\"
        ... Some random text
        ... ```
        ... x = 1
        ... print(x)
        ... ```
        ... More text.
        ... def function_example():
        ...     return "This is detected as a code snippet."
        ... \"\"\"
        >>> parse_markdown(test_input) # doctest: +NORMALIZE_WHITESPACE
        ['x = 1\\nprint(x)', 'def function_example():\\n    return "This is detected as a code snippet."']
    """
    result = parser.parse(input_string, lexer=lexer)
    valid_blocks = []
    for block in result:
        try:
            ast.parse(block)  # Validate if it's valid Python code
            valid_blocks.append(block)
        except SyntaxError:
            pass  # Ignore blocks that are not valid Python
    return valid_blocks


if __name__ == "__main__":
    import doctest

    doctest.testmod()
