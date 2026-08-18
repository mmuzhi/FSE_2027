#include <string>
#include <vector>

class IPAddress {
public:
    explicit IPAddress(const std::string& ip_address)
        : ip_address_(ip_address) {}

    bool is_valid() const {
        std::vector<std::string> octets = split(ip_address_, '.');
        if (octets.size() != 4) {
            return false;
        }
        for (const std::string& octet : octets) {
            if (!all_digits(octet) || octet_value(octet) > 255) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> get_octets() const {
        if (is_valid()) {
            return split(ip_address_, '.');
        } else {
            return {};
        }
    }

    std::string get_binary() const {
        if (is_valid()) {
            std::string binary;
            const std::vector<std::string> octets = get_octets();
            for (std::size_t i = 0; i < octets.size(); ++i) {
                if (i > 0) {
                    binary += '.';
                }
                unsigned long long value = octet_value(octets[i]);
                for (int bit = 7; bit >= 0; --bit) {
                    binary += ((value >> bit) & 1ULL) ? '1' : '0';
                }
            }
            return binary;
        } else {
            return "";
        }
    }

private:
    std::string ip_address_;

    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> parts;
        std::string current;
        for (char c : s) {
            if (c == delim) {
                parts.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        parts.push_back(current);
        return parts;
    }

    // Equivalent of Python's str.isdigit(): non-empty, all decimal digits.
    // Rejects "", signs ("+10"), whitespace, and non-digit characters.
    static bool all_digits(const std::string& s) {
        if (s.empty()) {
            return false;
        }
        for (char c : s) {
            if (c < '0' || c > '9') {
                return false;
            }
        }
        return true;
    }

    // Parses a decimal digit string. Leading zeros are accepted (like Python int()).
    // Clamps accumulation once the value exceeds 255 so arbitrarily long
    // zero-padded inputs cannot overflow (mirrors Python's big-int behavior:
    // value > 255 is invalid either way).
    static unsigned long long octet_value(const std::string& s) {
        unsigned long long value = 0;
        for (char c : s) {
            value = value * 10 + static_cast<unsigned long long>(c - '0');
            if (value > 255) {
                break;
            }
        }
        return value;
    }
};