from .code_parser import parser
from .code_builder import builder
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def src_under_limit(data, max_limit):
    tokens = tokenizer.tokenize(data)
    token_count = len(tokens)
    return max_limit >= token_count



def chunk(source_code: str, max_chunk_size: int):
    if src_under_limit(source_code, max_chunk_size):
        return {
            1: {
                "id": 1,
                "parents": [0],
                "type": "java_src",
                "name": "java_src",
                "content": source_code,
                "transformed": ""
            }
        }
    else:
        atoms = parser(source_code, max_chunk_size)
        return dict(atoms[0])


def unchunk(chunked_dict: dict, display, usecase_id):
    return builder(chunked_dict, display, usecase_id)
