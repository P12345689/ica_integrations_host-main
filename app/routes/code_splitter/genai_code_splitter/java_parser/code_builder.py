import logging

from .utils.splitter import extract_body_content

log = logging.getLogger(__name__)

def builder(atoms, display, usecase_id):
    queue = [id for id in atoms.keys()]
    flow = []

    while queue:
        i = queue.pop(0)
        if i not in flow:
            flow.append(i)
            children = atoms[i].get("children", [])
            if len(children):
                queue = children + queue

    src = ""
    cnt = 1
    child_map = {}

    for id in flow:
        if atoms[id].get("type", "") not in ("comment", "comments"):
            if display == "chunk_and_process":
                child_map[id] = cnt
                immediate_parent = atoms[id].get("parents", "")[-1]
                immediate_parent_srno = child_map.get(immediate_parent, 0)
                src += "\n***************************************************\n"
                src += f'CHUNKED DATA :: {cnt} ({atoms[id].get("name","")})'
                src += (
                    f"  (--Reference :: {str(immediate_parent_srno)} )"
                    if immediate_parent_srno > 1
                    else ""
                )
                src += "\n***************************************************\n"
                src += "\n" + atoms[id].get("content", "") + "\n"
                src += "\n***************************************************\n"
                if usecase_id == "Java_X_to_Java_Y_Conversion":
                    src += (
                        "Converted Java Code :: "
                        + str(cnt)
                        + "  ( "
                        + atoms[id].get("name", "")
                        + " )"
                    )
                else:
                    src += (
                        "Generated Result :: "
                        + str(cnt)
                        + "  ( "
                        + atoms[id].get("name", "")
                        + " )"
                    )
                src += "\n***************************************************\n"
                src += "\n" + atoms[id].get("transformed", "") + "\n"
                cnt += 1
            else:
                src = unchunk_java(atoms, 0)

    return src


def unchunk_java(atoms, parents):
    try:
        src = ""
        for atom, val in atoms.items():
            if parents == val["parents"][-1]:
                if "children" in val:
                    # body = val.get("transformed", None) if val.get("transformed", None) else "//Unable to Convert/n"+val["content"]
                    body = (
                        val.get("transformed", None)
                        if val.get("transformed", None)
                        else val["content"]
                    )
                    content, start_code, end_code = extract_body_content(body)
                    src += start_code + content
                    children = {child: atoms[child] for child in val["children"]}
                    src += unchunk_java(children, val["id"])
                    src += end_code

                elif parents == val["parents"][-1]:
                    # body = val.get("transformed", None) if val.get("transformed", None) else "//Unable to Convert/n"+val["content"]
                    body = (
                        val.get("transformed", None)
                        if val.get("transformed", None)
                        else val["content"]
                    )
                    src += body
        return src
    except Exception as ex:
        log.exception(ex)
        return ""
