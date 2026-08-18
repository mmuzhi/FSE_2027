import sys
import xml.etree.ElementTree as ET


class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.doc = ET.ElementTree()

    def read_xml(self):
        try:
            self.doc = ET.parse(self.file_name)
        except Exception:
            print(f"Error: Could not load XML file: {self.file_name}", file=sys.stderr)
            return None
        return self.doc.getroot()

    def write_xml(self, file_name):
        try:
            self.doc.write(file_name, encoding='utf-8')
            return True
        except Exception:
            return False

    def process_xml_data(self, file_name):
        root = self.doc.getroot()
        if root is None:
            print("Error: No root element found.", file=sys.stderr)
            return False

        for element in root.findall('item'):
            if element.text is not None:
                upper_text = element.text.upper()
                # Equivalent of Clear() + LinkEndChild(new TiXmlText(...))
                for child in list(element):
                    element.remove(child)
                element.text = upper_text
        return self.write_xml(file_name)

    def find_element(self, element_name):
        elements = []
        root = self.doc.getroot()
        if root is None:
            return elements
        for element in root.findall(element_name):
            elements.append(element)
        return elements