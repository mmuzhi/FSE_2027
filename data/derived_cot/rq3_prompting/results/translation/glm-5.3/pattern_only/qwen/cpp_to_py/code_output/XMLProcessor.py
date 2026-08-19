import sys
import xml.etree.ElementTree as ET


class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        # Equivalent of TiXmlDocument: an ElementTree whose root is None until loaded.
        self.doc = ET.ElementTree()

    def read_xml(self):
        try:
            self.doc = ET.parse(self.file_name)
        except (ET.ParseError, OSError):
            # LoadFile clears the document before loading, so on failure it is empty.
            self.doc = ET.ElementTree()
            print(f"Error: Could not load XML file: {self.file_name}", file=sys.stderr)
            return None
        return self.doc.getroot()

    def write_xml(self, file_name):
        try:
            root = self.doc.getroot()
            if root is None:
                # TinyXML saves an empty document as an empty file and returns true.
                with open(file_name, "wb"):
                    pass
            else:
                self.doc.write(file_name, encoding="utf-8", xml_declaration=False)
            return True
        except OSError:
            return False

    def process_xml_data(self, file_name):
        root = self.doc.getroot()
        if root is None:
            print("Error: No root element found.", file=sys.stderr)
            return False

        for element in list(root.findall("item")):
            text = element.text  # GetText(): None when there is no text child
            if text is not None:
                upper_text = text.upper()
                # Clear() removes children but keeps attributes; then a new text node is linked.
                for child in list(element):
                    element.remove(child)
                element.text = upper_text
        return self.write_xml(file_name)

    def find_element(self, element_name):
        elements = []
        root = self.doc.getroot()
        if root is None:
            return elements

        elements.extend(root.findall(element_name))
        return elements