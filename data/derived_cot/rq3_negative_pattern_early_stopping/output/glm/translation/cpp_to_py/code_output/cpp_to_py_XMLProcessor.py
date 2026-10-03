import sys
import xml.etree.ElementTree as ET

class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.doc = None

    def read_xml(self):
        try:
            self.doc = ET.parse(self.file_name)
            return self.doc.getroot()
        except ET.ParseError:
            print(f"Error: Could not load XML file: {self.file_name}", file=sys.stderr)
            return None

    def write_xml(self, file_name):
        if self.doc is None:
            return False
        try:
            self.doc.write(file_name)
            return True
        except Exception:
            return False

    def process_xml_data(self, file_name):
        if self.doc is None:
            print("Error: No root element found.", file=sys.stderr)
            return False
        root = self.doc.getroot()
        for element in root.findall("item"):
            if element.text is not None:
                element.text = element.text.upper()
        return self.write_xml(file_name)

    def find_element(self, element_name):
        if self.doc is None:
            return []
        root = self.doc.getroot()
        return root.findall(element_name)