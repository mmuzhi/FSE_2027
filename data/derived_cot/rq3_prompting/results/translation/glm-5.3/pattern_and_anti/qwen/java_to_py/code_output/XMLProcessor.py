import traceback
from xml.dom import Node
from xml.dom import minidom


def _get_text_content(node):
    # xml.dom.minidom has no textContent property; emulate the DOM semantics.
    parts = []
    for child in node.childNodes:
        if child.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
            parts.append(child.data)
        elif child.nodeType == Node.ELEMENT_NODE:
            parts.append(_get_text_content(child))
    return "".join(parts)


def _set_text_content(node, text):
    while node.firstChild:
        node.removeChild(node.firstChild)
    node.appendChild(node.ownerDocument.createTextNode(text))


class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.document = None

    def read_xml(self):
        try:
            self.document = minidom.parse(self.file_name)
            self.document.documentElement.normalize()
            return self.document
        except Exception:
            traceback.print_exc()
            return None

    def write_xml(self, file_name):
        if file_name is None or file_name == "":
            return False
        try:
            if self.document is None:
                return False
            with open(file_name, "wb") as f:
                f.write(self.document.toxml(encoding="utf-8"))
            return True
        except Exception:
            traceback.print_exc()
            return False

    def process_xml_data(self, file_name):
        if self.document is None:
            return False
        items = self.document.getElementsByTagName("item")
        for item in items:
            if item.nodeType == Node.ELEMENT_NODE:
                _set_text_content(item, _get_text_content(item).upper())
        return self.write_xml(file_name)

    def find_element(self, element_name):
        elements = []
        if self.document is None:
            return elements
        node_list = self.document.getElementsByTagName(element_name)
        for node in node_list:
            if node.nodeType == Node.ELEMENT_NODE:
                elements.append(node)
        return elements

    def get_document(self):
        return self.document

    def set_document(self, document):
        self.document = document