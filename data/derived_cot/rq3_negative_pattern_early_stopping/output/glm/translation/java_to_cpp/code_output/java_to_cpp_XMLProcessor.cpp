#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

#include "tinyxml2.h"

class XMLProcessor {
private:
    std::string fileName;
    tinyxml2::XMLDocument* document;

    std::string getTextContent(tinyxml2::XMLNode* node) {
        if (node->ToText()) {
            return node->Value() ? node->Value() : "";
        }
        std::string text;
        for (tinyxml2::XMLNode* child = node->FirstChild(); child != nullptr; child = child->NextSibling()) {
            text += getTextContent(child);
        }
        return text;
    }

    void setTextContent(tinyxml2::XMLElement* element, const std::string& text) {
        while (element->FirstChild()) {
            element->DeleteChild(element->FirstChild());
        }
        element->SetText(text.c_str());
    }

    void getElementsByTagNameHelper(tinyxml2::XMLElement* root, const std::string& elementName, std::vector<tinyxml2::XMLElement*>& elements) {
        if (root == nullptr) return;
        if (root->Name() != nullptr && std::string(root->Name()) == elementName) {
            elements.push_back(root);
        }
        for (tinyxml2::XMLElement* child = root->FirstChildElement(); child != nullptr; child = child->NextSiblingElement()) {
            getElementsByTagNameHelper(child, elementName, elements);
        }
    }

public:
    XMLProcessor(const std::string& fileName) : fileName(fileName), document(nullptr) {}

    ~XMLProcessor() {
        delete document;
    }

    XMLProcessor(const XMLProcessor&) = delete;
    XMLProcessor& operator=(const XMLProcessor&) = delete;

    tinyxml2::XMLDocument* readXml() {
        try {
            document = new tinyxml2::XMLDocument();
            if (document->LoadFile(fileName.c_str()) != tinyxml2::XML_SUCCESS) {
                std::cerr << "Error parsing XML: " << document->ErrorStr() << std::endl;
                delete document;
                document = nullptr;
                return nullptr;
            }
            return document;
        } catch (const std::exception& e) {
            std::cerr << "Exception: " << e.what() << std::endl;
            if (document) {
                delete document;
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
        try {
            if (document->SaveFile(fileName.c_str()) != tinyxml2::XML_SUCCESS) {
                std::cerr << "Error writing XML: " << document->ErrorStr() << std::endl;
                return false;
            }
            return true;
        } catch (const std::exception& e) {
            std::cerr << "Exception: " << e.what() << std::endl;
            return false;
        }
    }

    bool processXmlData(const std::string& fileName) {
        if (document == nullptr) {
            return false;
        }

        std::vector<tinyxml2::XMLElement*> items = findElement("item");
        for (tinyxml2::XMLElement* element : items) {
            std::string text = getTextContent(element);
            std::transform(text.begin(), text.end(), text.begin(),
                           [](unsigned char c){ return std::toupper(c); });
            setTextContent(element, text);
        }
        return writeXml(fileName);
    }

    std::vector<tinyxml2::XMLElement*> findElement(const std::string& elementName) {
        std::vector<tinyxml2::XMLElement*> elements;
        if (document == nullptr) {
            return elements;
        }

        tinyxml2::XMLElement* root = document->RootElement();
        if (root != nullptr) {
            getElementsByTagNameHelper(root, elementName, elements);
        }
        return elements;
    }

    tinyxml2::XMLDocument* getDocument() {
        return document;
    }

    void setDocument(tinyxml2::XMLDocument* document) {
        if (this->document != document) {
            delete this->document;
            this->document = document;
        }
    }
};