#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <fstream>
#include <tinyxml2.h>

class XMLProcessor {
private:
    std::string file_name;
    tinyxml2::XMLElement* root;
    tinyxml2::XMLDocument doc;

    void process_items_recursive(tinyxml2::XMLElement* element) {
        if (!element) return;
        if (std::string(element->Value()) == "item") {
            const char* text = element->GetText();
            if (text) {
                std::string upper_text = text;
                std::transform(upper_text.begin(), upper_text.end(), upper_text.begin(),
                               [](unsigned char c){ return std::toupper(c); });
                element->SetText(upper_text.c_str());
            } else {
                throw std::runtime_error("Element text is null");
            }
        }
        for (tinyxml2::XMLElement* child = element->FirstChildElement(); child; child = child->NextSiblingElement()) {
            process_items_recursive(child);
        }
    }

public:
    XMLProcessor(std::string file_name) : file_name(std::move(file_name)), root(nullptr) {}

    tinyxml2::XMLElement* read_xml() {
        if (doc.LoadFile(file_name.c_str()) != tinyxml2::XML_SUCCESS) {
            root = nullptr;
            return nullptr;
        }
        root = doc.RootElement();
        return root;
    }

    bool write_xml(const std::string& file_name) {
        if (!root) {
            std::ofstream ofs(file_name);
            return ofs.good();
        }
        tinyxml2::XMLNode* decl = doc.FirstChild();
        if (decl && decl->ToDeclaration()) {
            doc.DeleteChild(decl);
        }
        return doc.SaveFile(file_name.c_str()) == tinyxml2::XML_SUCCESS;
    }

    bool process_xml_data(const std::string& file_name) {
        if (!root) {
            throw std::runtime_error("Root element is null");
        }
        process_items_recursive(root);
        return write_xml(file_name);
    }

    std::vector<tinyxml2::XMLElement*> find_element(const std::string& element_name) {
        if (!root) {
            throw std::runtime_error("Root element is null");
        }
        std::vector<tinyxml2::XMLElement*> elements;
        if (element_name.empty()) {
            return elements;
        }
        for (tinyxml2::XMLElement* child = root->FirstChildElement(element_name.c_str()); child; child = child->NextSiblingElement(element_name.c_str())) {
            elements.push_back(child);
        }
        return elements;
    }
};