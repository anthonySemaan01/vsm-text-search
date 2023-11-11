import re
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring


def prettify_xml(elem):
    rough_string = tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


def remove_digits(text):
    return re.sub(r'\d', '', text)

def text_to_xml(text):
    def create_content_xml(content):
        # Create content element
        content_el = Element('content')
        # Split the content into 'dimension' elements
        for line in content:
            words = line.split()
            for word in words:
                dimension_el = SubElement(content_el, 'dimension')
                dimension_el.text = word
        return content_el

    def add_sections_to_xml(lines: list):
        xml_root = Element('xml')
        doc_el = SubElement(xml_root, 'Document')
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

        for line in lines[1:]:
            section_match = section_re.match(line)
            subsection_match = subsection_re.match(line)

            print(f"for line: {line} - section-match: {section_match}")
            print(f"for line {line} - subsection-match: {subsection_match}")
            print("")
            print(f"for line: {line} - current-section: {current_section}")
            print(f"for line {line} - current-subsection: {current_subsection}")
            print("")

            if section_match and not subsection_match:  # Start a new section
                subsections_tag_appended = False
                current_section = SubElement(sections_el, 'section')
                last_accessed_element = current_section
                number_el = SubElement(current_section, 'number')
                number_el.text = section_match.group(1) + '.'
                title_el = SubElement(current_section, 'title')
                for word in section_match.group(2).split():
                    dimension_el = SubElement(title_el, 'dimension')
                    dimension_el.text = word

            elif subsection_match:  # Start a new subsection within the current section
                # if current_subsections is None or not current_section:
                if last_accessed_element is current_section and not subsections_tag_appended:
                    parent_subsections = SubElement(current_section, 'subsections')
                    subsections_tag_appended = True

                current_subsection = SubElement(parent_subsections, 'subsection')
                last_accessed_element = current_subsection
                number_el = SubElement(current_subsection, 'number')
                number_el.text = subsection_match.group(1) + '.'
                title_el = SubElement(current_subsection, 'title')
                for word in remove_digits(section_match.group(2)).split():
                    dimension_el = SubElement(title_el, 'dimension')
                    dimension_el.text = word

            else:  # Content for the current section or subsection
                content_paragraph_lines += 1
                content = create_content_xml([line])
                print(
                    f"before assessment: current_subsections: {current_subsection} --- current_section {current_section}")

                if last_accessed_element is current_section:
                    current_section.append(content)
                elif last_accessed_element is current_subsection:
                    current_subsection.append(content)

        return xml_root, prettify_xml(xml_root)

    # Split the text into lines and filter out empty ones
    lines = [line for line in text.strip().split('\n') if line.strip()]
    print(f"lines: {lines}")
    # Convert to XML
    xml_root, xml_output = add_sections_to_xml(lines)
    return xml_root, xml_output


# Your text goes here
text_document = """
Text Document Search Tool
1. Hello
Life is good
2. Objective
The goal
2.1. Guidelines
Null
2.2. Framework
IDPA course.
"""

# Print the formatted XML
xml_root, xml_output = text_to_xml(text_document)
print(xml_output)

# exptected result

# <xml>
#     <Document>
#         <title> Text Document Search Tool </ title>
#     <sections>
#         <section>
#             <number> 1. </number>
#             <title> hello </title>
#             <content>
#                 <dimension> Life </dimension>
#                 <dimension> is </dimension>
#                 <dimension> good </dimension>
#             </content>
#         </section>
#         <section>
#             <number> 2. </number>
#             <title> Objective </title>
#             <content>
#                 < dimension > The < / dimension >
#                 < dimension > goal < / dimension >
#             </content>
#             <subsections>
#                 <subsection>
#                     <number> 2.1. </number>
#                     <title> Guidelines </title>
#                     <content>
#                         <dimension> Null </dimension>
#                     </content>
#                 </subsection>
#                 <subsection>
#                     <number> 2.2. </number>
#                     <title> Framework </title>
#                     <content>
#                         <dimension> IDPA </dimension>
#                         <dimension> Course </dimension>
#                     </content>
#                 </subsection>
#             <subsections>
#         </section>
#     </sections>
#     </Document>
# </xml>
