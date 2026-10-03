#include <string>
#include <vector>
#include <cctype>
#include <stdexcept>

struct BinaryInfo {
    double zeroes;
    double ones;
    int bit_length;
};

class BinaryDataProcessor {
private:
    std::string binary_string;

    void cleanNonBinaryChars() {
        binary_string = "";
        for (char c : binary_string) {
            if (c == '0' || c == '1') {
                binary_string += c;
            }
        }
    }

public:
    BinaryDataProcessor(const std::string& binary_string) : binary_string(binary_string) {
        cleanNonBinaryChars();
    }

    BinaryInfo calculateBinaryInfo() const {
        if (binary_string.empty()) {
            throw std::runtime_error("Binary string is empty");
        }

        int zeroes_count = 0;
        int ones_count = 0;
        for (char c : binary_string) {
            if (c == '0') zeroes_count++;
            else if (c == '1') ones_count++;
        }
        int total_length = binary_string.length();

        double zeroes_percentage = static_cast<double>(zeroes_count) / total_length;
        double ones_percentage = static_cast<double>(ones_count) / total_length;

        return { zeroes_percentage, ones_percentage, total_length };
    }

    std::string convertToAscii() const {
        if (binary_string.empty()) {
            return "";
        }

        std::vector<char> byte_array;
        for (size_t i = 0; i < binary_string.length(); i += 8) {
            if (i + 8 > binary_string.length()) {
                break;
            }
            std::string byte_str = binary_string.substr(i, 8);
            int value = std::stoi(byte_str, nullptr, 2);
            byte_array.push_back(static_cast<char>(value));
        }

        return std::string(byte_array.begin(), byte_array.end());
    }

    std::string convertToUtf8() const {
        if (binary_string.empty()) {
            return "";
        }

        std::vector<char> byte_array;
        for (size_t i = 0; i < binary_string.length(); i += 8) {
            if (i + 8 > binary_string.length()) {
                break;
            }
            std::string byte_str = binary_string.substr(i, 8);
            int value = std::stoi(byte_str, nullptr, 2);
            byte_array.push_back(static_cast<char>(value));
        }

        return std::string(byte_array.begin(), byte_array.end());
    }
};