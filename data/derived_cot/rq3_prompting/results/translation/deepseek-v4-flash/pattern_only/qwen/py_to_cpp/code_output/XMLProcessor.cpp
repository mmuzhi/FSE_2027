#include <string>
#include <vector>
#include <cctype>
#include <stdexcept>
#include "tinyxml2.h"

class XMLProcessor {
public:
    std::string file_name;
    tinyxml2::XMLElement* root;

    XMLProcessor(const std::string& file_name) : file_name(file_name), root(nullptr) {}

    tinyxml2::XMLElement* read_xml() {
        try {
            if (doc.LoadFile(file_name.c_str()) != tinyxml2::XML_SUCCESS) {
                root = nullptr;
                return nullptr;
            }
            root = doc.RootElement();
            return root;
        } catch (...) {
            root = nullptr;
            return nullptr;
        }
    }

    bool write_xml(const std::string& file_name) {
        try {
            if (root == nullptr) {
                return false;
            }
            tinyxml2::XMLDocument out;
            tinyxml2::XMLNode* cloned = root->DeepClone(&out);
            if (cloned == nullptr) {
                return false;
            }
            out.InsertEndChild(cloned);
            return out.SaveFile(file_name.c_str()) == tinyxml2::XML_SUCCESS;
        } catch (...) {
            return false;
        }
    }

    bool process_xml_data(const std::string& file_name) {
        if (root == nullptr) {
            throw std::runtime_error("'NoneType' object has no attribute 'iter'");
        }
        process_descendants(root);
        return write_xml(file_name);
    }

    std::vector<tinyxml2::XMLElement*> find_element(const std::string& element_name) {
        if (root == nullptr) {
            throw std::runtime_error("'NoneType' object has no attribute 'findall'");
        }
        std::vector<tinyxml2::XMLElement*> result;
        for (tinyxml2::XMLElement* elem = root->FirstChildElement(); elem != nullptr; elem = elem->NextSiblingElement()) {
            if (elem->Name() != nullptr && element_name == elem->Name()) {
                result.push_back(elem);
            }
        }
        return result;
    }

private:
    tinyxml2::XMLDocument doc;

    static void set_element_text(tinyxml2::XMLElement* elem, const std::string& text) {
        tinyxml2::XMLNode* first = elem->FirstChild();
        if (first != nullptr && first->ToText() != nullptr) {
            first->ToText()->SetValue(text.c_str());
        } else {
            tinyxml2::XMLText* newText = elem->GetDocument()->NewText(text.c_str());
            elem->InsertFirstChild(newText);
        }
    }

    static void process_descendants(tinyxml2::XMLElement* parent) {
        std::vector<tinyxml2::XMLElement*> stack;
        std::vector<tinyxml2::XMLElement*> children;
        for (tinyxml2::XMLElement* child = parent->FirstChildElement(); child != nullptr; child = child->NextSiblingElement()) {
            children.push_back(child);
        }
        for (auto it = children.rbegin(); it != children.rend(); ++it) {
            stack.push_back(*it);
        }

        while (!stack.empty()) {
            tinyxml2::XMLElement* current = stack.back();
            stack.pop_back();

            if (current->Name() != nullptr && std::string(current->Name()) == "item") {
                const char* text = current->GetText();
                if (text == nullptr) {
                    throw std::runtime_error("'NoneType' object has no attribute 'upper'");
                }
                std::string s(text);
                for (char& c : s) {
                    c = static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
                }
                set_element_text(current, s);
            }

            std::vector<tinyxml2::XMLElement*> childList;
            for (tinyxml2::XMLElement* child = current->FirstChildElement(); child != nullptr; child = child->NextSiblingElement()) {
                childList.push_back(child);
            }
            for (auto it = childList.rbegin(); it != childList.rend(); ++it) {
                stack.push_back(*it);
            }
        }
    }
};