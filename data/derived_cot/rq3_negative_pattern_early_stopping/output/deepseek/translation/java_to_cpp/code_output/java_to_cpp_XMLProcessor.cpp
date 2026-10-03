#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <stdexcept>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <libxml/xpath.h>
#include <libxml/xpathInternals.h>
#include <cstring>

class XMLProcessor {
private:
    std::string fileName;
    xmlDocPtr document;

public:
    XMLProcessor(const std::string& fileName) : fileName(fileName), document(nullptr) {}

    ~XMLProcessor() {
        if (document != nullptr) {
            xmlFreeDoc(document);
        }
    }

    XMLProcessor(const XMLProcessor&) = delete;
    XMLProcessor& operator=(const XMLProcessor&) = delete;
    XMLProcessor(XMLProcessor&&) = delete;
    XMLProcessor& operator=(XMLProcessor&&) = delete;

    xmlDocPtr readXml() {
        try {
            document = xmlParseFile(fileName.c_str());
            if (document == nullptr) {
                std::cerr << "Error: could not parse file " << fileName << std::endl;
                return nullptr;
            }
            xmlNodePtr root = xmlDocGetRootElement(document);
            if (root != nullptr) {
                // Normalize document: not strictly needed in libxml2, but mimic Java's normalize
            }
            return document;
        } catch (const std::exception& e) {
            std::cerr << "Exception in readXml: " << e.what() << std::endl;
            if (document != nullptr) {
                xmlFreeDoc(document);
                document = nullptr;
            }
            return nullptr;
        }
    }

    bool writeXml(const std::string& fileName) {
        if (fileName.empty()) {
            return false;
        }
        if (document == nullptr) {
            return false;
        }
        if (xmlSaveFormatFileEnc(fileName.c_str(), document, "UTF-8", 1) == -1) {
            std::cerr << "Error: could not write to file " << fileName << std::endl;
            return false;
        }
        return true;
    }

    bool processXmlData(const std::string& fileName) {
        if (document == nullptr) {
            return false;
        }

        // Get all elements named "item"
        std::vector<xmlNodePtr> items = findElement("item");
        for (xmlNodePtr item : items) {
            if (item != nullptr && item->type == XML_ELEMENT_NODE) {
                xmlNodePtr child = item->children;
                while (child != nullptr) {
                    if (child->type == XML_TEXT_NODE) {
                        xmlChar* content = xmlNodeGetContent(child);
                        if (content != nullptr) {
                            std::string upper = (const char*)content;
                            for (char& c : upper) {
                                c = toupper(c);
                            }
                            xmlNodeSetContent(child, (const xmlChar*)upper.c_str());
                            xmlFree(content);
                        }
                        break; // only first text child? Java's getTextContent returns concatenated text.
                        // But in Java, element.getTextContent() returns concatenated text of all text descendants.
                        // To match exactly, we would need to replace all text content.
                        // However, for simplicity, we mimic Java's behavior by replacing the whole text content of the element.
                        // Actually, Java's setTextContent replaces existing content. So we should replace all children.
                        // Let's do that properly: remove all children, then add a text node.
                    }
                    child = child->next;
                }
                // Proper replacement:
                xmlNodePtr textNode = xmlNewDocText(document, (const xmlChar*)"");
                if (textNode != nullptr) {
                    // Get the full text content (Java's getTextContent() concatenates all text descendants)
                    xmlChar* fullContent = xmlNodeGetContent(item);
                    std::string upper = (fullContent ? (const char*)fullContent : "");
                    for (char& c : upper) {
                        c = toupper(c);
                    }
                    xmlNodeSetContent(textNode, (const xmlChar*)upper.c_str());
                    // Replace all children of item with this single text node
                    xmlNodePtr cur = item->children;
                    while (cur != nullptr) {
                        xmlNodePtr next = cur->next;
                        xmlUnlinkNode(cur);
                        xmlFreeNode(cur);
                        cur = next;
                    }
                    xmlAddChild(item, textNode);
                    if (fullContent) xmlFree(fullContent);
                }
            }
        }
        return writeXml(fileName);
    }

    std::vector<xmlNodePtr> findElement(const std::string& elementName) {
        std::vector<xmlNodePtr> result;
        if (document == nullptr) {
            return result;
        }

        // Use XPath to find all elements with given name
        xmlXPathContextPtr xpathCtx = xmlXPathNewContext(document);
        if (xpathCtx == nullptr) {
            return result;
        }

        std::string xpathExpr = "//" + elementName;
        xmlXPathObjectPtr xpathObj = xmlXPathEvalExpression((const xmlChar*)xpathExpr.c_str(), xpathCtx);
        if (xpathObj == nullptr) {
            xmlXPathFreeContext(xpathCtx);
            return result;
        }

        xmlNodeSetPtr nodes = xpathObj->nodesetval;
        if (nodes != nullptr) {
            for (int i = 0; i < nodes->nodeNr; ++i) {
                xmlNodePtr node = nodes->nodeTab[i];
                if (node->type == XML_ELEMENT_NODE) {
                    result.push_back(node);
                }
            }
        }

        xmlXPathFreeObject(xpathObj);
        xmlXPathFreeContext(xpathCtx);
        return result;
    }

    xmlDocPtr getDocument() const {
        return document;
    }

    void setDocument(xmlDocPtr doc) {
        if (document != nullptr) {
            xmlFreeDoc(document);
        }
        document = doc;
    }
};