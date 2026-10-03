import sys
import traceback
from xml.dom import minidom, Node

class XMLProcessor:
    def __init__(self, fileName):
        self.fileName = fileName
        self.document = None

    def readXml(self):
        try:
            self.document = minidom.parse(self.fileName)
            self.document.normalize()
            return self.document
        except Exception as e:
            traceback.print_exc()
            return None

    def writeXml(self, fileName):
        if fileName is None or fileName == "":
            return False
        try:
            if self.document is None:
                return False
            with open(fileName, 'w', encoding='utf-8') as f:
                self.document.writexml(f, encoding='utf-8')
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    def processXmlData(self, fileName):
        if self.document is None:
            return False
        items = self.document.getElementsByTagName("item")
        for item in items:
            if item.nodeType == Node.ELEMENT_NODE:
                element = item
                text_content = []
                for child in element.childNodes:
                    if child.nodeType == Node.TEXT_NODE:
                        text_content.append(child.data)
                original = ''.join(text_content)
                while element.hasChildNodes():
                    element.removeChild(element.firstChild)
                new_text = self.document.createTextNode(original.upper())
                element.appendChild(new_text)
        return self.writeXml(fileName)

    def findElement(self, elementName):
        result = []
        if self.document is None:
            return result
        nodeList = self.document.getElementsByTagName(elementName)
        for node in nodeList:
            if node.nodeType == Node.ELEMENT_NODE:
                result.append(node)
        return result

    def getDocument(self):
        return self.document

    def setDocument(self, document):
        self.document = document