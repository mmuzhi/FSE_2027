#include <bitset>
#include <cstddef>
#include <string>
#include <vector>

// A class to process an IP address: validating it, getting its octets, and
// obtaining the binary representation of a valid IP address.
class IPAddress {
public:
    // Initialize the IP address to the specified address.
    explicit IPAddress(const std::string& ip_address) : ip_address(ip_address) {}

    // Judge whether the IP address is valid, i.e. whether it is composed of
    // four decimal numbers separated by '.', each in the range [0, 255].
    bool is_valid() const {
        std::vector<std::string> octets = split(ip_address, '.');
        if (octets.size() != 4) {
            return false;
        }
        for (const std::string& octet : octets) {
            int value = 0;
            if (!parse_octet(octet, value) || value < 0 || value > 255) {
                return false;
            }
        }
        return true;
    }

    // If the IP address is valid, return the four dot-separated parts
    // constituting it; otherwise return an empty list.
    std::vector<std::string> get_octets() const {
        if (is_valid()) {
            return split(ip_address, '.');
        }
        return {};
    }

    // If the IP address is valid, return its binary form; otherwise return "".
    std::string get_binary() const {
        if (is_valid()) {
            std::vector<std::string> binary_octets;
            for (const std::string& octet : get_octets()) {
                int value = 0;
                parse_octet(octet, value);  // already known to succeed here
                binary_octets.push_back(std::bitset<8>(value).to_string());
            }
            std::string result;
            for (std::size_t i = 0; i < binary_octets.size(); ++i) {
                if (i > 0) {
                    result += '.';
                }
                result += binary_octets[i];
            }
            return result;
        }
        return "";
    }

    std::string ip_address;

private:
    // Behaves like Python's str.split(sep) for a single-character separator:
    // every separator occurrence starts a new (possibly empty) piece, and the
    // trailing piece (possibly empty) is always included.
    static std::vector<std::string> split(const std::string& s, char delimiter) {
        std::vector<std::string> parts;
        std::string current;
        for (char c : s) {
            if (c == delimiter) {
                parts.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        parts.push_back(current);
        return parts;
    }

    // Mirrors Python's `octet.isdigit() and int(octet)` check for ASCII input:
    // returns false for empty or non-digit strings; otherwise returns true and
    // stores the numeric value. The value is capped so arbitrarily long digit
    // strings (which Python's arbitrary-precision int would compare against
    // 255) never overflow -- anything above 255 stays above 255.
    static bool parse_octet(const std::string& octet, int& value) {
        if (octet.empty()) {
            return false;
        }
        long long val = 0;
        for (char c : octet) {
            if (c < '0' || c > '9') {
                return false;
            }
            if (val <= 255) {
                val = val * 10 + (c - '0');
            }
        }
        value = static_cast<int>(val);
        return true;
    }
};