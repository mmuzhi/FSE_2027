import sys
from xml.dom import minidom
from xml.dom import Node

class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.doc = None

    def read_xml(self):
        self.doc = None
        try:
            self.doc = minidom.parse(self.file_name)
        except Exception:
            sys.stderr.write("Error: Could not load XML file: " + self.file_name + "\n")
            return None
        return self.doc.documentElement

    def write_xml(self, file_name):
        if self.doc is None:
            return False
        try:
            enc = self.doc.encoding or "utf-8"
            write_encoding = self.doc.encoding or None
            with open(file_name, "w", encoding=enc, newline="") as f:
                self.doc.writexml(f, encoding=write_encoding, newl="")
            return True
        except Exception:
            return False

    def process_xml_data(self, file_name):
        root = self.doc.documentElement if self.doc is not None else None
        if root is None:
            sys.stderr.write("Error: No root element found.\n")
            return False

        for child in list(root.childNodes):
            if child.nodeType == Node.ELEMENT_NODE and child.nodeName == "item":
                text = None
                if child.childNodes:
                    first = child.childNodes[0]
                    if first.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
                        text = first.data
                if text is not None:
                    upper_text = ''.join(chr(ord(ch) - 32) if 'a' <= ch <= 'z' else ch for ch in text)
                    if child.attributes is not None:
                        for attr_name in list(child.attributes.keys()):
                            child.removeAttribute(attr_name)
                    for grandchild in list(child.childNodes):
                        child.removeChild(grandchild)
                    child.appendChild(self.doc.createTextNode(upper_text))

        return self.write_xml(file_name)

    def find_element(self, element_name):
        if self.doc is None:
            return []
        root = self.doc.documentElement
        if root is None:
            return []
        elements = []
        for child in root.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and child.nodeName == element_name:
                elements.append(child)
        return elements