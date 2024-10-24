import re
from .lexer import generate_token_array
from pygments.token import Token
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def split_with_delimiter(text, delimiter):
    pattern = f"({re.escape(delimiter)}+)"
    parts = re.split(pattern, text)
    result = [parts[i] + (parts[i+1] if i+1 < len(parts) else "") for i in range(0, len(parts), 2)]
    return result

def under_token_limit(data, max_limit):
    tokens = tokenizer.tokenize(data)
    token_count = len(tokens)
    return max_limit >= token_count

def extract_body_content(block_code):
    first = block_code.find("{")
    last = block_code.rfind("}")
    while block_code[first+1] not in ("\n"," "):
        first = block_code.find("{", first+1)
        if first == -1:
            raise Exception("Unable to extract body content")
    return block_code[first+2:last], block_code[:first+2], block_code[last:]




def is_balanced(char, stack):
    if char == "{":
        stack.append("{")
    elif char == "}" :
        stack.pop()
    return len(stack) == 0


def find_end_of_block(lines_array, idx):
    class_stack = []
    for i in range(idx, len(lines_array)):
        line_tokens = generate_token_array(lines_array[i])
        for type, value in line_tokens:
            if type in Token.Punctuation and value in ['{','}']: 
                if is_balanced(value, class_stack):
                    return "".join(lines_array[idx:i+1]), i
                
def find_end_of_comment(lines_array, idx):
    for i in range(idx, len(lines_array)):
        if "*/" in lines_array[i]:
            return "".join(lines_array[idx:i+1]), i