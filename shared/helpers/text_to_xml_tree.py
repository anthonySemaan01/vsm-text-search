from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

import regex as re

from shared.helpers.clean_text import clean_text


def prettify_xml(elem):
    rough_string = tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


def remove_digits(text):
    return re.sub(r'\d', '', text)


def transform_text_to_xml(semi_structured_text: str):
    def create_content_xml(content, content_tag):
        for line in content:
            line = clean_text(line)
            words = line.split()
            for word in words:
                dimension_el = SubElement(content_tag, 'dimension')
                dimension_el.text = word
        return content_tag

    def add_sections_to_xml(lines: list):
        xml_root_element = Element('xml')
        doc_el = SubElement(xml_root_element, 'Document')
        title_el = SubElement(doc_el, 'title')
        for word in lines[0].split():
            dimension_el = SubElement(title_el, 'dimension')
            dimension_el.text = word
        sections_el = SubElement(doc_el, 'sections')

        # Regular expressions for matching section and subsection numbers
        section_re = re.compile(r'^(\d+)\.\s*(.*)')
        subsection_re = re.compile(r'^(\d+\.\d+)\.\s*(.*)')

        # Variables to keep track of current section and subsection
        current_section = None
        parent_subsections = None
        current_subsection = None
        last_accessed_element = None

        content_paragraph_lines = 0
        subsections_tag_appended = False

        for index, line in enumerate(lines[1:], 1):
            section_match = section_re.match(line)
            subsection_match = subsection_re.match(line)

            if section_match and not subsection_match:  # Start a new section
                content_paragraph_lines = 0
                subsections_tag_appended = False
                current_section = SubElement(sections_el, 'section')
                last_accessed_element = current_section
                number_el = SubElement(current_section, 'number')
                number_el.text = section_match.group(1) + '.'
                title_el = SubElement(current_section, 'title')
                for word in clean_text(section_match.group(2)).split():
                    dimension_el = SubElement(title_el, 'dimension')
                    dimension_el.text = word

            elif subsection_match:
                content_paragraph_lines = 0
                if last_accessed_element is current_section and not subsections_tag_appended:
                    parent_subsections = SubElement(current_section, 'subsections')
                    subsections_tag_appended = True

                current_subsection = SubElement(parent_subsections, 'subsection')
                last_accessed_element = current_subsection
                number_el = SubElement(current_subsection, 'number')
                number_el.text = subsection_match.group(1) + '.'
                title_el = SubElement(current_subsection, 'title')
                for word in clean_text(remove_digits(section_match.group(2))).split():
                    dimension_el = SubElement(title_el, 'dimension')
                    dimension_el.text = word

            else:  # Content for the current section or subsection
                content_paragraph_lines += 1

                if content_paragraph_lines == 1:
                    content = Element('content')

                content_element = create_content_xml([line], content)

                done = False
                if index + 1 < len(lines):
                    section_match_nl = section_re.match(lines[index + 1])
                    subsection_match_nl = subsection_re.match(lines[index + 1])
                else:
                    done = True

                if last_accessed_element is current_section and (section_match_nl or subsection_match_nl) or done:
                    current_section.append(content)
                elif last_accessed_element is current_subsection and (section_match_nl or subsection_match_nl) or done:
                    current_subsection.append(content)

        return xml_root_element, prettify_xml(xml_root_element)

    # Convert to XML
    xml_root, xml_output = add_sections_to_xml(
        [line for line in semi_structured_text.strip().split('\n') if line.strip()])
    return xml_root, xml_output


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

