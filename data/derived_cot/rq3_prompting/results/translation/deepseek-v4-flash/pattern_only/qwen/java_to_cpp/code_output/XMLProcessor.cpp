#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <cctype>
#include <iostream>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <libxml/xmlstring.h>

struct XmlDocDeleter {
    void operator()(xmlDoc* doc) const {
        if (doc) xmlFreeDoc(doc);
    }
};

using XmlDocPtr = std::shared_ptr<xmlDoc>;

class XMLProcessor {
public:
    XMLProcessor(const std::string& fileName)
        : fileName(fileName), document(nullptr) {}

    XmlDocPtr readXml() {
        xmlDocPtr raw = xmlReadFile(fileName.c_str(), nullptr, XML_PARSE_NONET);
        if (!raw) {
            std::cerr << "Failed to parse XML file: " << fileName << std::endl;
            return nullptr;
        }
        document = XmlDocPtr(raw, XmlDocDeleter());
        normalizeDocument(document.get());
        return document;
    }

    bool writeXml(const std::string& outFileName) {
        if (outFileName.empty()) {
            return false;
        }
        if (!document) {
            return false;
        }
        int result = xmlSaveFile(outFileName.c_str(), document.get());
        if (result == -1) {
            std::cerr << "Failed to write XML file: " << outFileName << std::endl;
            return false;
        }
        return true;
    }

    bool processXmlData(const std::string& outFileName) {
        if (!document) {
            return false;
        }
        std::vector<xmlNodePtr> items = findElement("item");
        for (xmlNodePtr item : items) {
            if (item->type == XML_ELEMENT_NODE) {
                xmlChar* content = xmlNodeGetContent(item);
                std::string text = content ? reinterpret_cast<const char*>(content) : "";
                if (content) xmlFree(content);
                std::transform(text.begin(), text.end(), text.begin(),
                               [](unsigned char c) { return std::toupper(c); });
                xmlNodeSetContent(item, reinterpret_cast<const xmlChar*>(text.c_str()));
            }
        }
        return writeXml(outFileName);
    }

    std::vector<xmlNodePtr> findElement(const std::string& elementName) {
        std::vector<xmlNodePtr> elements;
        if (!document) {
            return elements;
        }
        xmlNodePtr root = xmlDocGetRootElement(document.get());
        collectElements(root, elementName, elements);
        return elements;
    }

    XmlDocPtr getDocument() {
        return document;
    }

    void setDocument(XmlDocPtr doc) {
        document = std::move(doc);
    }

private:
    std::string fileName;
    XmlDocPtr document;

    static void collectElements(xmlNodePtr node, const std::string& name,
                                std::vector<xmlNodePtr>& result) {
        if (!node) return;
        if (node->type == XML_ELEMENT_NODE &&
            name == reinterpret_cast<const char*>(node->name)) {
            result.push_back(node);
        }
        for (xmlNodePtr child = node->children; child; child = child->next) {
            collectElements(child, name, result);
        }
    }

    static void normalizeDocument(xmlDocPtr doc) {
        xmlNodePtr root = xmlDocGetRootElement(doc);
        if (root) {
            normalizeNode(root);
        }
    }

    static void normalizeNode(xmlNodePtr node) {
        if (!node) return;
        for (xmlNodePtr child = node->children; child; child = child->next) {
            normalizeNode(child);
        }

        // Merge adjacent text/CDATA nodes
        xmlNodePtr cur = node->children;
        while (cur) {
            xmlNodePtr next = cur->next;
            if ((cur->type == XML_TEXT_NODE || cur->type == XML_CDATA_SECTION_NODE) &&
                next && (next->type == XML_TEXT_NODE || next->type == XML_CDATA_SECTION_NODE)) {
                if (next->content) {
                    xmlNodeAddContent(cur, next->content);
                }
                xmlUnlinkNode(next);
                xmlFreeNode(next);
                continue;
            }
            cur = next;
        }

        // Remove empty text/CDATA nodes
        cur = node->children;
        while (cur) {
            xmlNodePtr next = cur->next;
            if ((cur->type == XML_TEXT_NODE || cur->type == XML_CDATA_SECTION_NODE) &&
                (cur->content == nullptr || xmlStrlen(cur->content) == 0)) {
                xmlUnlinkNode(cur);
                xmlFreeNode(cur);
            }
            cur = next;
        }
    }
};