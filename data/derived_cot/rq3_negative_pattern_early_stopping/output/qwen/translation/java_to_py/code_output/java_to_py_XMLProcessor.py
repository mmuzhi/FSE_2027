import xml.etree.ElementTree as ET
from xml.dom import minidom  # We might need this for pretty printing if required, but the original doesn't specify.

class XMLProcessor:
    def __init__(self, fileName):
        self.fileName = fileName
        self.root = None  # This will be the root element

    def readXml(self):
        try:
            tree = ET.parse(self.fileName)
            self.root = tree.getroot()
            return self.root
        except Exception as e:
            print(f"Error reading XML: {e}")
            return None

    def writeXml(self, fileName):
        if fileName is None or fileName.strip() == "":
            return False
        try:
            if self.root is None:
                return False

            # Create a tree with the root element
            tree = ET.ElementTree(self.root)
            tree.write(fileName, encoding="utf-8", xml_declaration=True)
            return True
        except Exception as e:
            print(f"Error writing XML: {e}")
            return False

    def processXmlData(self, fileName):
        if self.root is None:
            return False

        # Process: convert text content of every 'item' element to uppercase
        for elem in self.root.iter('item'):
            if elem.text is not None:
                elem.text = elem.text.upper()

        return self.writeXml(fileName)

    def findElement(self, elementName):
        elements = []
        if self.root is None:
            return elements

        # Find all elements with the given tag
        for elem in self.root.findall(elementName):
            elements.append(elem)
        return elements

    # Setters and getters
    def getDocument(self):
        # In Java, Document was used. In Python, we return the root element (Element) or None.
        return self.root

    def setDocument(self, document):
        # We assume document is an Element
        self.root = document