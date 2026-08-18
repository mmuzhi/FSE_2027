#include <tinyxml2.h>

#include <algorithm>
#include <cctype>
#include <cstdio>
#include <string>
#include <vector>

class XMLProcessor {
private:
    std::string fileName;
    tinyxml2::XMLDocument* document;

    // Mimics org.w3c.dom.Node.getTextContent(): concatenates all descendant text.
    static std::string getTextContent(const tinyxml2::XMLNode* node) {
        std::string result;
        for (const tinyxml2::XMLNode* child = node->FirstChild(); child != nullptr;
             child = child->NextSibling()) {
            if (child->ToText() != nullptr) {
                const char* value = child->Value();
                if (value != nullptr) {
                    result += value;
                }
            } else {
                result += getTextContent(child);
            }
        }
        return result;
    }

    // Mimics org.w3c.dom.Node.setTextContent(): replaces all children with a single text node.
    static void setTextContent(tinyxml2::XMLElement* element, const std::string& text) {
        while (tinyxml2::XMLNode* child = element->FirstChild()) {
            element->DeleteChild(child);
        }
        element->SetText(text.c_str());
    }

    // Java's String.toUpperCase() (ASCII behavior matches the classic "C" locale).
    static std::string toUpperCase(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(),
                       [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
        return s;
    }

    // Mimics org.w3c.dom.Document.getElementsByTagName():
    // all descendant elements in document (pre-)order, supporting the "*" wildcard.
    static void collectElementsByTagName(tinyxml2::XMLNode* node, const std::string& name,
                                         std::vector<tinyxml2::XMLElement*>& out) {
        for (tinyxml2::XMLNode* child = node->FirstChild(); child != nullptr;
             child = child->NextSibling()) {
            tinyxml2::XMLElement* element = child->ToElement();
            if (element != nullptr) {
                const char* elementName = element->Name();
                if (name == "*" || (elementName != nullptr && name == elementName)) {
                    out.push_back(element);
                }
                collectElementsByTagName(element, name, out);
            }
        }
    }

public:
    explicit XMLProcessor(const std::string& fileName)
        : fileName(fileName), document(nullptr) {}

    ~XMLProcessor() { delete document; }

    tinyxml2::XMLDocument* readXml() {
        tinyxml2::XMLDocument* parsed = new tinyxml2::XMLDocument();
        if (parsed->LoadFile(this->fileName.c_str()) != tinyxml2::XML_SUCCESS) {
            // e.printStackTrace()
            std::fprintf(stderr, "java.lang.Exception: %s\n", parsed->ErrorStr());
            delete parsed;
            // On failure the previous document (if any) is left untouched, as in Java.
            return nullptr;
        }
        // getDocumentElement().normalize(): tinyxml2 never produces adjacent
        // text nodes while parsing, so normalization is a no-op here.
        this->document = parsed;
        return this->document;
    }

    bool writeXml(const std::string& fileName) {
        if (fileName.empty()) { // null is not representable for std::string
            return false;
        }
        if (this->document == nullptr) {
            return false;
        }
        if (this->document->SaveFile(fileName.c_str()) != tinyxml2::XML_SUCCESS) {
            // TransformerException -> printStackTrace()
            std::fprintf(stderr, "javax.xml.transform.TransformerException: %s\n",
                         this->document->ErrorStr());
            return false;
        }
        return true;
    }

    bool processXmlData(const std::string& fileName) {
        if (this->document == nullptr) {
            return false;
        }
        std::vector<tinyxml2::XMLElement*> items;
        collectElementsByTagName(this->document, "item", items);
        for (tinyxml2::XMLElement* element : items) { // all collected nodes are elements
            setTextContent(element, toUpperCase(getTextContent(element)));
        }
        return writeXml(fileName);
    }

    std::vector<tinyxml2::XMLElement*> findElement(const std::string& elementName) {
        std::vector<tinyxml2::XMLElement*> elements;
        if (this->document == nullptr) {
            return elements;
        }
        collectElementsByTagName(this->document, elementName, elements);
        return elements;
    }

    tinyxml2::XMLDocument* getDocument() const { return document; }

    // Takes ownership of the given document (old one is released like Java's GC would).
    void setDocument(tinyxml2::XMLDocument* document) {
        if (this->document != document) {
            delete this->document;
        }
        this->document = document;
    }
};