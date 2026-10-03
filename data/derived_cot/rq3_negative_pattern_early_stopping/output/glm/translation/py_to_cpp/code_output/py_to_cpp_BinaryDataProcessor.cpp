#include <string>
#include <map>
#include <algorithm>
#include <stdexcept>

class BinaryDataProcessor {
public:
    std::string binary_string;

    BinaryDataProcessor(std::string binary_string) : binary_string(std::move(binary_string)) {
        clean_non_binary_chars();
    }

    void clean_non_binary_chars() {
        binary_string.erase(std::remove_if(binary_string.begin(), binary_string.end(),
                                           [](char c) { return c != '0' && c != '1'; }),
                            binary_string.end());
    }

    std::map<std::string, double> calculate_binary_info() const {
        int zeroes_count = std::count(binary_string.begin(), binary_string.end(), '0');
        int ones_count = std::count(binary_string.begin(), binary_string.end(), '1');
        int total_length = binary_string.length();

        if (total_length == 0) {
            throw std::overflow_error("division by zero");
        }

        double zeroes_percentage = static_cast<double>(zeroes_count) / total_length;
        double ones_percentage = static_cast<double>(ones_count) / total_length;

        return {
            {"Zeroes", zeroes_percentage},
            {"Ones", ones_percentage},
            {"Bit length", static_cast<double>(total_length)}
        };
    }

    std::string convert_to_ascii() const {
        std::string bytes = get_bytes();
        for (unsigned char c : bytes) {
            if (c > 127) {
                throw std::runtime_error("UnicodeDecodeError: 'ascii' codec can't decode byte");
            }
        }
        return bytes;
    }

    std::string convert_to_utf8() const {
        std::string bytes = get_bytes();
        if (!is_valid_utf8(bytes)) {
            throw std::runtime_error("UnicodeDecodeError: 'utf-8' codec can't decode byte");
        }
        return bytes;
    }

private:
    std::string get_bytes() const {
        std::string bytes;
        for (size_t i = 0; i < binary_string.length(); i += 8) {
            std::string byte_str = binary_string.substr(i, 8);
            unsigned char decimal = 0;
            for (char c : byte_str) {
                decimal = (decimal << 1) | (c - '0');
            }
            bytes += static_cast<char>(decimal);
        }
        return bytes;
    }

    bool is_valid_utf8(const std::string& str) const {
        size_t i = 0;
        while (i < str.size()) {
            unsigned char c = static_cast<unsigned char>(str[i]);
            size_t num_bytes = 0;
            if ((c & 0x80) == 0x00) num_bytes = 1;
            else if ((c & 0xE0) == 0xC0) num_bytes = 2;
            else if ((c & 0xF0) == 0xE0) num_bytes = 3;
            else if ((c & 0xF8) == 0xF0) num_bytes = 4;
            else return false;

            if (i + num_bytes > str.size()) return false;

            for (size_t j = 1; j < num_bytes; ++j) {
                if ((static_cast<unsigned char>(str[i + j]) & 0xC0) != 0x80) return false;
            }
            i += num_bytes;
        }
        return true;
    }
};