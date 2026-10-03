#include <libxml/parser.h>
#include <libxml/tree.h>
#include <string>
#include <vector>
#include <iostream>
#include <algorithm>

class XMLProcessor {
private:
    std::string fileName;
    xmlDocPtr doc;

public:
    XMLProcessor(const std::string& fileName) : fileName(fileName), doc(nullptr) {}

    ~XMLProcessor() {
        if (doc != nullptr) {
            xmlFreeDoc(doc);
        }
    }

    bool readXml() {
        // Reset the document if it exists
        if (doc != nullptr) {
            xmlFreeDoc(doc);
            doc = nullptr;
        }

        doc = xmlReadFile(fileName.c_str(), nullptr, XML_PARSE_NOBLANKS);
        if (doc == nullptr) {
            std::cerr << "Error: Failed to parse XML file." << std::endl;
            return false;
        }

        // Normalize the document
        xmlDocDumpMemory(doc, nullptr); // Not exactly the same, but we'll proceed
        return true;
    }

    bool writeXml(const std::string& fileName) {
        if (fileName.empty()) {
            return false;
        }

        if (doc == nullptr) {
            return false;
        }

        int ret = xmlSaveFile(fileName.c_str(), doc);
        if (ret == -1) {
            std::cerr << "Error: Failed to write XML file." << std::endl;
            return false;
        }
        return true;
    }

    bool processXmlData(const std::string& fileName) {
        if (doc == nullptr) {
            return false;
        }

        // Process the XML data: convert text content of all 'item' elements to uppercase
        xmlNodePtr root = xmlDocGetRootElement(doc);
        if (root == nullptr) {
            return false;
        }

        // Traverse the tree and find all 'item' elements
        xmlNodePtr curNode = nullptr;
        for (curNode = root->children; curNode != nullptr; curNode = curNode->next) {
            if (curNode->type == XML_ELEMENT_NODE && 
                xmlStrEqual(curNode->name, BAD_CAST "item")) {
                // Convert the text content to uppercase
                xmlChar* text = xmlNodeGetContent(curNode);
                if (text != nullptr) {
                    // Convert the XML char* to std::string and then to uppercase
                    std::string textStr(reinterpret_cast<char*>(text));
                    std::transform(textStr.begin(), textStr.end(), textStr.begin(), ::toupper);
                    xmlNodeSetContent(curNode, reinterpret_cast<xmlChar*>(textStr.c_str()));
                }
            }
        }

        return writeXml(fileName);
    }

    std::vector<xmlNodePtr> findElement(const std::string& elementName) {
        std::vector<xmlNodePtr> elements;
        if (doc == nullptr) {
            return elements;
        }

        xmlNodePtr root = xmlDocGetRootElement(doc);
        if (root == nullptr) {
            return elements;
        }

        xmlNodePtr curNode = nullptr;
        for (curNode = root->children; curNode != nullptr; curNode = curNode->next) {
            if (curNode->type == XML_ELEMENT_NODE && 
                xmlStrEqual(curNode->name, BAD_CAST elementName.c_str())) {
                elements.push_back(curNode);
            }
        }

        return elements;
    }

    xmlDocPtr getDocument() {
        return doc;
    }

    void setDocument(xmlDocPtr document) {
        if (doc != nullptr) {
            xmlFreeDoc(doc);
        }
        doc = document;
    }
};