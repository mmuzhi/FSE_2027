#include <string>
#include <map>
#include <algorithm>
#include <stdexcept>
#include <cstdint>

class BinaryDataProcessor {
public:
    std::string binary_string;

    explicit BinaryDataProcessor(const std::string& binary_string_)
        : binary_string(binary_string_) {
        clean_non_binary_chars();
    }

    void clean_non_binary_chars() {
        std::string cleaned;
        for (char c : binary_string) {
            if (c == '0' || c == '1') {
                cleaned += c;
            }
        }
        binary_string = std::move(cleaned);
    }

    std::map<std::string, double> calculate_binary_info() const {
        size_t zeroes_count = static_cast<size_t>(std::count(binary_string.begin(), binary_string.end(), '0'));
        size_t ones_count = static_cast<size_t>(std::count(binary_string.begin(), binary_string.end(), '1'));
        size_t total_length = binary_string.size();

        // Python raises ZeroDivisionError when total_length == 0
        if (total_length == 0) {
            throw std::runtime_error("ZeroDivisionError: division by zero");
        }

        return {
            {"Zeroes", static_cast<double>(zeroes_count) / static_cast<double>(total_length)},
            {"Ones",   static_cast<double>(ones_count) / static_cast<double>(total_length)},
            {"Bit length", static_cast<double>(total_length)}
        };
    }

    std::string convert_to_ascii() const {
        std::string byte_array;
        for (size_t i = 0; i < binary_string.size(); i += 8) {
            std::string byte = binary_string.substr(i, 8);
            unsigned long decimal = std::stoul(byte, nullptr, 2);
            // Python 'ascii' codec rejects bytes > 127
            if (decimal > 127) {
                throw std::runtime_error("UnicodeDecodeError: 'ascii' codec can't decode byte");
            }
            byte_array += static_cast<char>(decimal);
        }
        return byte_array;
    }

    std::string convert_to_utf8() const {
        std::string byte_array;
        for (size_t i = 0; i < binary_string.size(); i += 8) {
            std::string byte = binary_string.substr(i, 8);
            unsigned long decimal = std::stoul(byte, nullptr, 2);
            byte_array += static_cast<char>(decimal);
        }
        // Python 'utf-8' codec is strict; mirror that behavior
        if (!is_valid_utf8(byte_array)) {
            throw std::runtime_error("UnicodeDecodeError: 'utf-8' codec can't decode bytes");
        }
        return byte_array;
    }

private:
    static bool is_valid_utf8(const std::string& s) {
        size_t i = 0;
        while (i < s.size()) {
            unsigned char c = static_cast<unsigned char>(s[i]);
            size_t len;
            uint32_t cp;
            if (c < 0x80) {
                ++i;
                continue;
            } else if ((c & 0xE0) == 0xC0) {
                len = 2;
                cp = c & 0x1F;
            } else if ((c & 0xF0) == 0xE0) {
                len = 3;
                cp = c & 0x0F;
            } else if ((c & 0xF8) == 0xF0) {
                len = 4;
                cp = c & 0x07;
            } else {
                return false;
            }
            if (i + len > s.size()) {
                return false;
            }
            for (size_t j = 1; j < len; ++j) {
                unsigned char cc = static_cast<unsigned char>(s[i + j]);
                if ((cc & 0xC0) != 0x80) {
                    return false;
                }
                cp = (cp << 6) | (cc & 0x3F);
            }
            // Overlong encodings, out-of-range, and surrogates are invalid
            if (len == 2 && cp < 0x80) return false;
            if (len == 3 && cp < 0x800) return false;
            if (len == 4 && cp < 0x10000) return false;
            if (cp > 0x10FFFF) return false;
            if (cp >= 0xD800 && cp <= 0xDFFF) return false;
            i += len;
        }
        return true;
    }
};