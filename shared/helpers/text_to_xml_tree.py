from xml.etree.ElementTree import Element, SubElement
import regex as re
from shared.helpers.clean_text import clean_text


# TODO implement transform_text_to_xml
def transform_text_to_xml(semi_structured_text: str):
    return ""


def preprocessing(elt, depth=0, path=""):
    if elt is None:
        return None
    new_tree = Element(path + str(depth) + ".&" + str(elt.tag.lower()))

    new_path = path + str(depth) + "."
    d = 0

    for key, value in sorted(elt.attrib.items()):
        attr_path = new_path + str(d) + "."
        attr_key = SubElement(new_tree, attr_path + "@" + str(key.lower()))
        attr_value = SubElement(attr_key, attr_path + "0." + "#" + str(value.lower()))
        d += 1

    for child in elt:
        new_tree.append(preprocessing(child, d, new_path))
        d += 1

    if elt.text is not None:
        txt = clean_text(elt.text)
        tokens = txt.split()
        for token in tokens:
            tk = SubElement(new_tree, new_path + str(d) + ".#" + str(token))
            d += 1
    return new_tree


def element_type(element):
    if '@' in element.tag:
        return "attribute"
    elif '&' in element.tag:
        return "element"
    else:
        return "text"


def element_name(element):
    return element.tag.split(".")[-1]


def get_tree(path, tree):
    path_list = path.split(".")
    if len(path_list) == 1:  # 2):
        return tree
    target = int(path_list[1])

    children = []
    for child in tree:
        children.append(child)
    # print("children list: \t"+str(children))
    if len(children) == 0:
        return tree
    else:
        return get_tree(".".join(path_list[1:]), children[target])


def get_path(element):
    return str(re.split('.@|.#|.&', element.tag)[0])


def root_path(element, tree):
    to_return = []
    current = get_path(element).split(".")

    for counter in range(1, len(current)):
        target = ".".join(current[0:counter])
        to_return.append(element_name(get_tree(target, tree))[1:])

    return "/".join(to_return)


def find_term_context(tree):
    term_context_list = []

    for element in tree.iter():
        if element_type(element) == "text":
            term_context_list.append(str(element_name(element)[1:] + "," + root_path(element, tree)))

    return term_context_list
