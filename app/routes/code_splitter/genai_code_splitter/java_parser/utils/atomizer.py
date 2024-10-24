from .splitter import split_with_delimiter,find_end_of_block, find_end_of_comment
from .lexer import generate_token_array, parse_token

def atomizer(source_code, parents):
    src_line_array = split_with_delimiter(source_code,"\n")
    cur_index = 0
    result = []
    child_queue = ""

    while cur_index < len(src_line_array):
        line = src_line_array[cur_index]
        clean_line = line.strip()
        line_tokens = generate_token_array(clean_line)
        type, name = parse_token(line_tokens, clean_line)

        if type in ["class","interface","method"]:
            content, cur_index =  find_end_of_block(src_line_array, cur_index)
            result.append(dict(type=type, name=name, content=child_queue +content, parents=parents))
            child_queue = ""
                        
        elif type == "comments":
            content, cur_index = find_end_of_comment(src_line_array, cur_index)
            result.append(dict(type=type, name=name, content=content, parents=parents))

        elif type == "annotation":
            child_queue += line

        elif type == "attribute":
            result.append(dict(type=type, name=name, content=child_queue+line, parents=parents))
            child_queue = ""

        elif type is None and len(result):
            result[-1]["content"] += line    
            
        elif type in ['package','import','comment'] and len(result) and  result[-1]["type"] in (None, type) :
            result[-1]["content"] += line
            result[-1]["type"] = type
        else:
            result.append(dict(type=type, name=name, content=line, parents=parents))
        cur_index += 1

    return result