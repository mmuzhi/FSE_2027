#include <string>
#include <map>
#include <algorithm>
#include <stdexcept>
#include <cstddef>

class ZeroDivisionError : public std::runtime_error {
public:
    explicit ZeroDivisionError(const std::string& msg) : std::runtime_error(msg) {}
};

class UnicodeDecodeError : public std::runtime_error {
public:
    explicit UnicodeDecodeError(const std::string& msg) : std::runtime_error(msg) {}
};

class BinaryDataProcessor {
public:
    std::string binary_string;

    BinaryDataProcessor(const std::string& binary_string) : binary_string(binary_string) {
        clean_non_binary_chars();
    }

    void clean_non_binary_chars() {
        std::string cleaned;
        cleaned.reserve(binary_string.size());
        for (char c : binary_string) {
            if (c == '0' || c == '1') {
                cleaned += c;
            }
        }
        binary_string = cleaned;
    }

    std::map<std::string, double> calculate_binary_info() const {
        std::ptrdiff_t zeroes_count = std::count(binary_string.begin(), binary_string.end(), '0');
        std::ptrdiff_t ones_count = std::count(binary_string.begin(), binary_string.end(), '1');
        std::ptrdiff_t total_length = static_cast<std::ptrdiff_t>(binary_string.size());

        if (total_length == 0) {
            throw ZeroDivisionError("division by zero");
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
        std::string result;
        for (std::size_t i = 0; i < binary_string.size(); i += 8) {
            std::string byte = binary_string.substr(i, 8);
            int decimal = std::stoi(byte, nullptr, 2);

            if (decimal > 127) {
                throw UnicodeDecodeError(
                    "'ascii' codec can't decode byte 0x" + to_hex(decimal) +
                    " in position " + std::to_string(static_cast<unsigned long long>(i)) +
                    ": ordinal not in range(128)"
                );
            }

            result += static_cast<char>(decimal);
        }
        return result;
    }

    std::string convert_to_utf8() const {
        std::string result;
        for (std::size_t i = 0; i < binary_string.size(); i += 8) {
            std::string byte = binary_string.substr(i, 8);
            int decimal = std::stoi(byte, nullptr, 2);
            result += static_cast<char>(decimal);
        }

        if (!is_valid_utf8(result)) {
            throw UnicodeDecodeError("'utf-8' codec can't decode byte in position ...");
        }

        return result;
    }

private:
    static std::string to_hex(int value) {
        const char* digits = "0123456789abcdef";
        if (value == 0) return "00";

        std::string hex;
        while (value > 0) {
            hex = digits[value % 16] + hex;
            value /= 16;
        }
        if (hex.size() == 1) hex = "0" + hex;
        return hex;
    }

    static bool is_valid_utf8(const std::string& s) {
        std::size_t i = 0;
        while (i < s.size()) {
            unsigned char c = static_cast<unsigned char>(s[i]);

            if (c < 0x80) {
                i++;
            } else if ((c & 0xE0) == 0xC0) {
                if (i + 1 >= s.size()) return false;
                unsigned char c2 = static_cast<unsigned char>(s[i + 1]);
                if ((c2 & 0xC0) != 0x80) return false;
                int cp = ((c & 0x1F) << 6) | (c2 & 0x3F);
                if (cp < 0x80) return false;
                i += 2;
            } else if ((c & 0xF0) == 0xE0) {
                if (i + 2 >= s.size()) return false;
                unsigned char c2 = static_cast<unsigned char>(s[i + 1]);
                unsigned char c3 = static_cast<unsigned char>(s[i + 2]);
                if ((c2 & 0xC0) != 0x80 || (c3 & 0xC0) != 0x80) return false;
                int cp = ((c & 0x0F) << 12) | ((c2 & 0x3F) << 6) | (c3 & 0x3F);
                if (cp < 0x800) return false;
                if (cp >= 0xD800 && cp <= 0xDFFF) return false;
                i += 3;
            } else if ((c & 0xF8) == 0xF0) {
                if (i + 3 >= s.size()) return false;
                unsigned char c2 = static_cast<unsigned char>(s[i + 1]);
                unsigned char c3 = static_cast<unsigned char>(s[i + 2]);
                unsigned char c4 = static_cast<unsigned char>(s[i + 3]);
                if ((c2 & 0xC0) != 0x80 || (c3 & 0xC0) != 0x80 || (c4 & 0xC0) != 0x80) return false;
                int cp = ((c & 0x07) << 18) | ((c2 & 0x3F) << 12) | ((c3 & 0x3F) << 6) | (c4 & 0x3F);
                if (cp < 0x10000) return false;
                if (cp > 0x10FFFF) return false;
                i += 4;
            } else {
                return false;
            }
        }
        return true;
    }
};