
from .utils.atomizer import atomizer
from .utils.splitter import under_token_limit, extract_body_content


def split_class(source_code, parents):
    body, start_code, end_code = extract_body_content(source_code)
    children = atomizer(body, parents)
    new_children = []
    for i in range(len(children)):
        if children[i]["type"] == "attribute":
            start_code += children[i]["content"]
        else:
            new_children.append(children[i])
    
    content = start_code.strip()+ "\n\n" + end_code.strip()
    return content, new_children

def parser(source_code, max_chunk_size):
    current_id = 0
    atoms = {0: {}}
    token_unchecked = []

    list_of_atoms = atomizer(source_code, [current_id])

    for atom in list_of_atoms:
        current_id += 1
        atoms[0][current_id] = dict(id=current_id, parents=atom["parents"],
                                    type=atom["type"], name=atom["name"], content=atom["content"], transformed="")
        token_unchecked.append(current_id)

    while len(token_unchecked):
        id = token_unchecked.pop()
        if atoms[0][id]["type"] == "class" and not under_token_limit(atoms[0][id]["content"], max_limit=max_chunk_size):
            content, children = split_class(
                atoms[0][id]["content"], atoms[0][id]["parents"]+[id])
            atoms[0][id]["content"] = content
            atoms[0][id]["children"] = []
            for child in children:
                current_id += 1
                atoms[0][id]["children"].append(current_id)
                atoms[0][current_id] = dict(
                    id=current_id, parents=child["parents"], type=child["type"], name=child["name"], content=child["content"], transformed="")
                token_unchecked.append(current_id)

    return atoms

