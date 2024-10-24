import re
import json
from pygments.lexers import JavaLexer
from pygments.token import Token

def generate_token_array(code):
    lexer = JavaLexer()
    return list(lexer.get_tokens(code))
        

def find_name(line, specific_word):
    pattern = rf'{re.escape(specific_word)}\s+(\w+)'
    match = re.search(pattern, line)
    if match:
        following_word = match.group(1)
        return following_word
    else:
        return "Annonymous"


def find_method_name(line):
    pattern = rf'\s+(\w+)\s*\('     # Closing paranthesis for method declaration is not included as it might be closed in next line
    match = re.search(pattern, line)
    if match:
        method_name = match.group(1)
        return method_name
    else:
        return 'Annonymous'

def parse_token(line_tokens, line):
    if (Token.Keyword.Namespace, 'package') in line_tokens:
        name = 'Package'
        return "package", name
    elif line.startswith("import") or (Token.Keyword.Namespace, 'import') in line_tokens or (Token.Keyword.Namespace, 'import static') in line_tokens:
        name = "Import"
        return "import", name
    elif line.startswith("//") or line_tokens[0][0] == Token.Comment.Single :
        name = "Comment"
        return "comment", name
    
    elif (Token.Keyword.Declaration, 'interface') in line_tokens:
        name = find_name(line, 'interface')
        return "interface", name
    elif (Token.Keyword.Declaration, 'class') in line_tokens:
        name = find_name(line, 'class')
        return "class", name
    elif line.startswith("/*"):
        name = "Comment"
        return "comments", name
    
    elif line.startswith("@") or line_tokens[0][0] == Token.Name.Decorator :
        name = "Annotation"
        return "annotation", name
    elif Token.Name.Function in [type for type, value in line_tokens]:
        name = find_method_name(line)
        return "method", name
    
    elif Token.Keyword.Declaration in [type for type, value in line_tokens] :
        name = "Attribute"
        return "attribute", name
    else:
        name = "Attribute"
        return "attribute", name
    
