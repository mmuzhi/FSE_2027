#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <cstdint>
#include <stdexcept>

class BinaryDataProcessor {
private:
    std::string binary_string;

public:
    BinaryDataProcessor(const std::string& input) : binary_string(input) {
        clean_non_binary_chars();
    }

    void clean_non_binary_chars() {
        binary_string.erase(
            std::remove_if(binary_string.begin(), binary_string.end(),
                           [](char c) { return c != '0' && c != '1'; }),
            binary_string.end());
    }

    std::map<std::string, double> calculate_binary_info() const {
        size_t zeroes = 0, ones = 0;
        for (char c : binary_string) {
            if (c == '0')
                ++zeroes;
            else if (c == '1')
                ++ones;
        }
        double total = static_cast<double>(binary_string.length());
        return {
            {"Zeroes", zeroes / total},
            {"Ones", ones / total},
            {"Bit length", static_cast<double>(binary_string.length())}
        };
    }

    std::string convert_to_ascii() const {
        std::vector<uint8_t> bytes;
        for (size_t i = 0; i < binary_string.length(); i += 8) {
            std::string byte_str = binary_string.substr(i, 8);
            int val = std::stoi(byte_str, nullptr, 2);
            if (val > 127) {
                throw std::runtime_error("'ascii' codec can't decode byte at position " + std::to_string(bytes.size()));
            }
            bytes.push_back(static_cast<uint8_t>(val));
        }
        return std::string(bytes.begin(), bytes.end());
    }

    std::string convert_to_utf8() const {
        std::vector<uint8_t> bytes;
        for (size_t i = 0; i < binary_string.length(); i += 8) {
            std::string byte_str = binary_string.substr(i, 8);
            int val = std::stoi(byte_str, nullptr, 2);
            bytes.push_back(static_cast<uint8_t>(val));
        }
        return std::string(bytes.begin(), bytes.end());
    }
};