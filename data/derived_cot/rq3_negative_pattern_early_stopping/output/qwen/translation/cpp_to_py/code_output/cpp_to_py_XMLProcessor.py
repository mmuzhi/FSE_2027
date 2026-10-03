import xml.etree.ElementTree as ET
from io import BytesIO

class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.doc = None  # We'll use this to hold the XML tree

    def read_xml(self):
        try:
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            self.doc = tree  # Store the tree for later use
            return root
        except ET.ParseError as e:
            print(f"Error: Could not load XML file: {self.file_name}. {str(e)}")
            return None

    def write_xml(self, file_name):
        if self.doc is None:
            print("Error: No XML document to write.")
            return False
        try:
            self.doc.write(file_name)
            return True
        except Exception as e:
            print(f"Error: Could not write XML file: {file_name}. {str(e)}")
            return False

    def process_xml_data(self, file_name):
        # If the XML hasn't been loaded, try to load it from the given file
        if self.doc is None:
            # Try to parse the new file
            try:
                tree = ET.parse(file_name)
                self.doc = tree
            except ET.ParseError as e:
                print(f"Error: Could not load XML file for processing: {file_name}. {str(e)}")
                return False

        if self.doc is None:
            print("Error: No root element found.")
            return False

        root = self.doc.getroot()
        # Process each "item" element
        for item in root.findall(".//item"):
            # Clear the element: remove all children and set text to None
            while len(item) > 0:
                item.remove(item[0])
            text = item.text
            if text is not None:
                upper_text = text.upper()
                item.text = upper_text
            else:
                item.text = ""  # If there was no text, set to empty string

        # Write the modified XML to the given file
        return self.write_xml(file_name)

    def find_element(self, element_name):
        if self.doc is None:
            return []
        root = self.doc.getroot()
        elements = []
        # Find all elements with the given tag name, including those in child trees
        for elem in root.findall(".//" + element_name):
            elements.append(elem)
        return elements