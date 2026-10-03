import xml.etree.ElementTree as ET
import sys

class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.tree = None

    def read_xml(self):
        try:
            self.tree = ET.parse(self.file_name)
            return self.tree.getroot()
        except (ET.ParseError, FileNotFoundError) as e:
            print(f"Error: Could not load XML file: {self.file_name}", file=sys.stderr)
            return None

    def write_xml(self, file_name):
        try:
            self.tree.write(file_name, encoding='utf-8', xml_declaration=True)
            return True
        except Exception:
            return False

    def process_xml_data(self, file_name):
        if self.tree is None:
            print("Error: No root element found.", file=sys.stderr)
            return False
        root = self.tree.getroot()
        if root is None:
            print("Error: No root element found.", file=sys.stderr)
            return False

        for element in root.findall('item'):
            text = element.text
            if text is not None:
                upper_text = text.upper()
                element.clear()          # remove all children (including text and sub-elements)
                element.text = upper_text

        return self.write_xml(file_name)

    def find_element(self, element_name):
        if self.tree is None:
            return []
        root = self.tree.getroot()
        if root is None:
            return []
        return root.findall(element_name)