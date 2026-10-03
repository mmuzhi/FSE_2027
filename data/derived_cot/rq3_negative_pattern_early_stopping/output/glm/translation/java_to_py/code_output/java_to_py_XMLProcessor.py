import traceback
from xml.dom.minidom import parse, Node

class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.document = None

    def _get_text_content(self, node):
        if node.nodeType == Node.TEXT_NODE:
            return node.data
        text = ""
        for child in node.childNodes:
            text += self._get_text_content(child)
        return text

    def _set_text_content(self, node, text):
        while node.firstChild:
            node.removeChild(node.firstChild)
        node.appendChild(node.ownerDocument.createTextNode(text))

    def read_xml(self):
        try:
            self.document = parse(self.file_name)
            self.document.documentElement.normalize()
            return self.document
        except Exception as e:
            traceback.print_exc()
            return None

    def write_xml(self, file_name):
        if file_name is None or file_name == "":
            return False
        try:
            if self.document is None:
                return False

            with open(file_name, "w", encoding="utf-8") as f:
                self.document.writexml(f, indent="", addindent="", newl="")
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    def process_xml_data(self, file_name):
        if self.document is None:
            return False

        items = self.document.getElementsByTagName("item")
        for i in range(items.length):
            item = items.item(i)
            if item.nodeType == Node.ELEMENT_NODE:
                text_content = self._get_text_content(item)
                self._set_text_content(item, text_content.upper())
        return self.write_xml(file_name)

    def find_element(self, element_name):
        elements = []
        if self.document is None:
            return elements

        node_list = self.document.getElementsByTagName(element_name)
        for i in range(node_list.length):
            if node_list.item(i).nodeType == Node.ELEMENT_NODE:
                elements.append(node_list.item(i))
        return elements

    def get_document(self):
        return self.document

    def set_document(self, document):
        self.document = document