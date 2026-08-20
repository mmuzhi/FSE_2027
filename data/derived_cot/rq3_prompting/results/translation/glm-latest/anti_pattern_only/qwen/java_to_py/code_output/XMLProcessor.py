import traceback
from typing import List, Optional
from xml.dom import Node
from xml.dom.minidom import Document, Element, parse


def _get_text_content(node):
    """Equivalent of the DOM Level 3 Node.getTextContent() method."""
    node_type = node.nodeType
    if node_type in (Node.ELEMENT_NODE, Node.DOCUMENT_NODE,
                     Node.DOCUMENT_FRAGMENT_NODE):
        parts = []
        for child in node.childNodes:
            if child.nodeType in (Node.COMMENT_NODE,
                                  Node.PROCESSING_INSTRUCTION_NODE):
                continue
            parts.append(_get_text_content(child))
        return "".join(parts)
    if node_type in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE,
                     Node.COMMENT_NODE, Node.PROCESSING_INSTRUCTION_NODE):
        return node.data
    return None


def _set_text_content(node, text):
    """Equivalent of the DOM Level 3 Node.setTextContent() method."""
    while node.firstChild is not None:
        node.removeChild(node.firstChild)
    if text:
        node.appendChild(node.ownerDocument.createTextNode(text))


class XMLProcessor:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.document: Optional[Document] = None

    def read_xml(self) -> Optional[Document]:
        try:
            self.document = parse(self.file_name)
            self.document.documentElement.normalize()
            return self.document
        except Exception:
            traceback.print_exc()
            return None

    def write_xml(self, file_name: str) -> bool:
        if file_name is None or file_name == "":
            return False
        try:
            if self.document is None:
                return False

            with open(file_name, "wb") as stream:
                stream.write(self.document.toxml(encoding="UTF-8"))
            return True
        except Exception:
            traceback.print_exc()
            return False

    def process_xml_data(self, file_name: str) -> bool:
        if self.document is None:
            return False

        items = self.document.getElementsByTagName("item")
        for item in items:
            if item.nodeType == Node.ELEMENT_NODE:
                _set_text_content(item, _get_text_content(item).upper())
        return self.write_xml(file_name)

    def find_element(self, element_name: str) -> List[Element]:
        elements: List[Element] = []
        if self.document is None:
            return elements

        node_list = self.document.getElementsByTagName(element_name)
        for node in node_list:
            if node.nodeType == Node.ELEMENT_NODE:
                elements.append(node)
        return elements

    def get_document(self) -> Optional[Document]:
        return self.document

    def set_document(self, document: Optional[Document]) -> None:
        self.document = document