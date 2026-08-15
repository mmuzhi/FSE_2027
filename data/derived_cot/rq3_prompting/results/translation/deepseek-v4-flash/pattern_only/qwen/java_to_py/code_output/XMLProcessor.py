import traceback
from xml.dom import minidom, Node


def _get_text_content(node):
    parts = []
    for child in node.childNodes:
        if child.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
            parts.append(child.data)
        else:
            parts.append(_get_text_content(child))
    return ''.join(parts)


def _set_text_content(node, text):
    for child in list(node.childNodes):
        node.removeChild(child)
    if text is not None:
        node.appendChild(node.ownerDocument.createTextNode(text))


class XMLProcessor:
    def __init__(self, fileName):
        self.fileName = fileName
        self.document = None

    def readXml(self):
        try:
            self.document = minidom.parse(self.fileName)
            self.document.documentElement.normalize()
            return self.document
        except Exception:
            traceback.print_exc()
            return None

    def writeXml(self, fileName):
        if fileName is None or fileName == "":
            return False
        try:
            if self.document is None:
                return False

            old_version = getattr(self.document, 'version', None)
            old_standalone = getattr(self.document, 'standalone', None)
            try:
                self.document.version = "1.0"
                self.document.standalone = "no"
                with open(fileName, 'w', encoding='UTF-8', newline='') as f:
                    self.document.writexml(f, encoding='UTF-8')
            finally:
                self.document.version = old_version
                self.document.standalone = old_standalone

            return True
        except Exception:
            traceback.print_exc()
            return False

    def processXmlData(self, fileName):
        if self.document is None:
            return False

        items = self.document.getElementsByTagName("item")
        for i in range(items.length):
            item = items.item(i)
            if item.nodeType == Node.ELEMENT_NODE:
                _set_text_content(item, _get_text_content(item).upper())

        return self.writeXml(fileName)

    def findElement(self, elementName):
        elements = []
        if self.document is None:
            return elements

        nodeList = self.document.getElementsByTagName(elementName)
        for i in range(nodeList.length):
            node = nodeList.item(i)
            if node.nodeType == Node.ELEMENT_NODE:
                elements.append(node)
        return elements

    def getDocument(self):
        return self.document

    def setDocument(self, document):
        self.document = document