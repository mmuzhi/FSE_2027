#include <algorithm>
#include <cstdint>
#include <stdexcept>
#include <string>

class BinaryDataProcessor {
public:
    // Equivalent of the Python dict {'Zeroes': ..., 'Ones': ..., 'Bit length': ...}
    struct BinaryInfo {
        double zeroes;          // 'Zeroes'
        double ones;            // 'Ones'
        long long bit_length;   // 'Bit length' (int in Python)
    };

    explicit BinaryDataProcessor(const std::string& binary_string)
        : binary_string_(binary_string) {
        clean_non_binary_chars();
    }

    // Remove all characters other than '0' and '1'.
    void clean_non_binary_chars() {
        std::string cleaned;
        for (char c : binary_string_) {
            if (c == '0' || c == '1') {
                cleaned.push_back(c);
            }
        }
        binary_string_.swap(cleaned);
    }

    // Python uses true division; empty string raises ZeroDivisionError.
    BinaryInfo calculate_binary_info() const {
        long long zeroes_count = 0;
        long long ones_count = 0;
        for (char c : binary_string_) {
            if (c == '0') {
                ++zeroes_count;
            } else if (c == '1') {
                ++ones_count;
            }
        }
        long long total_length = static_cast<long long>(binary_string_.size());
        if (total_length == 0) {
            throw std::runtime_error("ZeroDivisionError: division by zero");
        }
        return BinaryInfo{
            static_cast<double>(zeroes_count) / static_cast<double>(total_length),
            static_cast<double>(ones_count) / static_cast<double>(total_length),
            total_length};
    }

    // decode('ascii'): any byte >= 128 raises UnicodeDecodeError in Python.
    std::string convert_to_ascii() const {
        std::string bytes = build_bytes();
        for (char ch : bytes) {
            if (static_cast<unsigned char>(ch) >= 128) {
                throw std::runtime_error(
                    "UnicodeDecodeError: 'ascii' codec can't decode byte");
            }
        }
        return bytes;
    }

    // decode('utf-8'): invalid sequences raise UnicodeDecodeError in Python.
    std::string convert_to_utf8() const {
        std::string bytes = build_bytes();
        validate_utf8(bytes);
        return bytes;
    }

    const std::string& binary_string() const { return binary_string_; }

private:
    std::string binary_string_;

    // Same chunking as Python: int(byte, 2) per chunk; the last chunk may be
    // shorter than 8 bits and is still parsed (e.g. "011" -> 3).
    std::string build_bytes() const {
        std::string bytes;
        for (std::size_t i = 0; i < binary_string_.size(); i += 8) {
            unsigned int decimal = 0;
            const std::size_t end = std::min(i + 8, binary_string_.size());
            for (std::size_t j = i; j < end; ++j) {
                decimal = decimal * 2 + static_cast<unsigned int>(binary_string_[j] - '0');
            }
            bytes.push_back(static_cast<char>(decimal));
        }
        return bytes;
    }

    static void validate_utf8(const std::string& s) {
        std::size_t i = 0;
        const std::size_t n = s.size();
        while (i < n) {
            const unsigned char b = static_cast<unsigned char>(s[i]);
            std::size_t len;
            std::uint32_t cp;
            if (b < 0x80) {
                i += 1;
                continue;
            } else if ((b & 0xE0) == 0xC0) {
                len = 2;
                cp = b & 0x1Fu;
            } else if ((b & 0xF0) == 0xE0) {
                len = 3;
                cp = b & 0x0Fu;
            } else if ((b & 0xF8) == 0xF0) {
                len = 4;
                cp = b & 0x07u;
            } else {
                throw std::runtime_error("UnicodeDecodeError: invalid start byte");
            }
            if (i + len > n) {
                throw std::runtime_error(
                    "UnicodeDecodeError: unexpected end of data");
            }
            for (std::size_t j = 1; j < len; ++j) {
                const unsigned char c = static_cast<unsigned char>(s[i + j]);
                if ((c & 0xC0) != 0x80) {
                    throw std::runtime_error(
                        "UnicodeDecodeError: invalid continuation byte");
                }
                cp = (cp << 6) | (c & 0x3Fu);
            }
            if ((len == 2 && cp < 0x80) || (len == 3 && cp < 0x800) ||
                (len == 4 && cp < 0x10000)) {
                throw std::runtime_error(
                    "UnicodeDecodeError: overlong encoding");
            }
            if (cp >= 0xD800 && cp <= 0xDFFF) {
                throw std::runtime_error(
                    "UnicodeDecodeError: surrogates not allowed");
            }
            if (cp > 0x10FFFF) {
                throw std::runtime_error(
                    "UnicodeDecodeError: code point out of range");
            }
            i += len;
        }
    }
};