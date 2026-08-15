import sys
import xml.etree.ElementTree as ET


class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.doc = ET.ElementTree()

    def read_xml(self):
        self.doc = ET.ElementTree()
        try:
            self.doc = ET.parse(self.file_name)
            return self.doc.getroot()
        except (ET.ParseError, OSError):
            sys.stderr.write("Error: Could not load XML file: " + self.file_name + "\n")
            return None

    def write_xml(self, file_name):
        try:
            if self.doc.getroot() is None:
                with open(file_name, 'w', encoding='utf-8') as f:
                    pass
            else:
                self.doc.write(file_name, encoding='utf-8')
            return True
        except OSError:
            return False

    def process_xml_data(self, file_name):
        root = self.doc.getroot()
        if root is None:
            sys.stderr.write("Error: No root element found.\n")
            return False

        for element in [child for child in root if child.tag == "item"]:
            text = self._get_text(element)
            if text is not None:
                upper_text = text.upper()
                for child in list(element):
                    element.remove(child)
                element.text = upper_text

        return self.write_xml(file_name)

    def find_element(self, element_name):
        root = self.doc.getroot()
        if root is None:
            return []
        return [child for child in root if child.tag == element_name]

    @staticmethod
    def _get_text(element):
        if element.text is not None:
            return element.text
        for child in element:
            if child.tail is not None:
                return child.tail
        return None