import traceback
from typing import List, Optional
from xml.dom import minidom
from xml.dom.minidom import Document, Element, Node


def _get_text_content(node) -> str:
    if node.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
        return node.data
    return "".join(_get_text_content(child) for child in node.childNodes)


def _set_text_content(element: Element, text: str) -> None:
    while element.firstChild is not None:
        element.removeChild(element.firstChild)
    element.appendChild(element.ownerDocument.createTextNode(text))


class XMLProcessor:
    def __init__(self, fileName: str):
        self.fileName = fileName
        self.document: Optional[Document] = None

    def readXml(self) -> Optional[Document]:
        try:
            self.document = minidom.parse(self.fileName)
            self.document.documentElement.normalize()
            return self.document
        except Exception:
            traceback.print_exc()
            return None

    def writeXml(self, fileName: Optional[str]) -> bool:
        if fileName is None or fileName == "":
            return False
        try:
            if self.document is None:
                return False
            with open(fileName, "w", encoding="utf-8") as f:
                self.document.writexml(f)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def processXmlData(self, fileName: str) -> bool:
        if self.document is None:
            return False

        items = self.document.getElementsByTagName("item")
        for i in range(items.length):
            item = items.item(i)
            if item.nodeType == Node.ELEMENT_NODE:
                element = item
                _set_text_content(element, _get_text_content(element).upper())
        return self.writeXml(fileName)

    def findElement(self, elementName: str) -> List[Element]:
        elements: List[Element] = []
        if self.document is None:
            return elements

        nodeList = self.document.getElementsByTagName(elementName)
        for i in range(nodeList.length):
            if nodeList.item(i).nodeType == Node.ELEMENT_NODE:
                elements.append(nodeList.item(i))
        return elements

    def getDocument(self) -> Optional[Document]:
        return self.document

    def setDocument(self, document: Optional[Document]) -> None:
        self.document = document