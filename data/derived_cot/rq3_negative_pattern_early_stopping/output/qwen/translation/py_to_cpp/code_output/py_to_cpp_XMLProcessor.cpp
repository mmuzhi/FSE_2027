#include <pugixml.hpp>
#include <string>
#include <vector>

class XMLProcessor {
private:
    std::string file_name;
    pugi::xml_node root;

    void process_item_nodes(pugi::xml_node node) {
        if (node && node.name() && !strcmp(node.name(), "item")) {
            if (node.text()) {
                std::string text = node.text().as_string();
                node.text().set(text.c_str());
            }
        }
        for (pugi::xml_node child : node.children()) {
            process_item_nodes(child);
        }
    }

    void find_elements(pugi::xml_node node, const std::string& tag, std::vector<pugi::xml_node>& result) {
        if (node && node.name() && !strcmp(node.name(), tag.c_str())) {
            result.push_back(node);
        }
        for (pugi::xml_node child : node.children()) {
            find_elements(child, tag, result);
        }
    }

public:
    XMLProcessor(const std::string& file_name) : file_name(file_name), root(nullptr) {}

    pugi::xml_node read_xml() {
        try {
            pugi::xml_document doc;
            doc.load_file(file_name.c_str());
            root = doc.root();
            return root;
        } catch (...) {
            return nullptr;
        }
    }

    bool write_xml(const std::string& file_name) {
        try {
            if (!root) return false;
            pugi::xml_document doc;
            doc.assign_node(root);
            doc.save_file(file_name.c_str());
            return true;
        } catch (...) {
            return false;
        }
    }

    bool process_xml_data(const std::string& file_name) {
        try {
            if (root) {
                process_item_nodes(root);
            }
            return write_xml(file_name);
        } catch (...) {
            return false;
        }
    }

    std::vector<pugi::xml_node> find_element(const std::string& element_name) {
        std::vector<pugi::xml_node> result;
        if (root) {
            find_elements(root, element_name, result);
        }
        return result;
    }
};