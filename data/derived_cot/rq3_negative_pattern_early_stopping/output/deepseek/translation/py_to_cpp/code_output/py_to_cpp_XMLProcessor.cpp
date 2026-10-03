#include <string>
#include <vector>
#include <cctype>
#include <algorithm>
#include <stdexcept>
#include <pugixml.hpp>

class XMLProcessor {
private:
    std::string file_name;
    pugi::xml_document doc;
    pugi::xml_node root;

public:
    XMLProcessor(const std::string& file_name)
        : file_name(file_name), root(nullptr) {}

    /**
     * Reads the XML file and returns the root element.
     * @return The root element of the XML file, or a null node on failure.
     */
    pugi::xml_node read_xml() {
        pugi::xml_parse_result result = doc.load_file(file_name.c_str());
        if (result) {
            root = doc.document_element();
        } else {
            root = pugi::xml_node(); // null node
        }
        return root;
    }

    /**
     * Writes the XML data to the specified file.
     * @param file_name The name of the file to write the XML data.
     * @return True if the write operation is successful, False otherwise.
     */
    bool write_xml(const std::string& file_name) {
        if (!root) {
            // Mimics Python's AttributeError when root is None
            throw std::runtime_error("XMLProcessor: root is not initialized, call read_xml first");
        }
        return doc.save_file(file_name.c_str());
    }

    /**
     * Modifies the data in XML elements and writes the updated XML data to a new file.
     * @param file_name The name of the file to write the modified XML data.
     * @return True if the write operation is successful, False otherwise.
     */
    bool process_xml_data(const std::string& file_name) {
        if (!root) {
            // Mimics Python's AttributeError when root is None
            throw std::runtime_error("XMLProcessor: root is not initialized, call read_xml first");
        }
        // XPath to find all descendant elements named "item" (like Python's iter('item'))
        pugi::xpath_node_set items = doc.select_nodes("//item");
        for (auto& node : items) {
            pugi::xml_node item_node = node.node();
            std::string text = item_node.text().as_string();
            // Convert to uppercase
            std::transform(text.begin(), text.end(), text.begin(),
                           [](unsigned char c) { return static_cast<unsigned char>(std::toupper(c)); });
            item_node.text().set(text.c_str());
        }
        return write_xml(file_name);
    }

    /**
     * Finds the XML elements with the specified name (all descendants).
     * @param element_name The name of the elements to find.
     * @return A list of found elements with the specified name.
     */
    std::vector<pugi::xml_node> find_element(const std::string& element_name) {
        if (!root) {
            // Mimics Python's AttributeError when root is None
            throw std::runtime_error("XMLProcessor: root is not initialized, call read_xml first");
        }
        std::vector<pugi::xml_node> result;
        // XPath to find all descendant elements with the given tag name
        pugi::xpath_node_set nodes = doc.select_nodes(("//" + element_name).c_str());
        for (auto& node : nodes) {
            result.push_back(node.node());
        }
        return result;
    }
};