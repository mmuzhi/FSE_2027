#include <string>
#include <vector>

/**
 * # This is a class to process IP Address, including validating, getting the
 * octets and obtaining the binary representation of a valid IP address.
 */
class IPAddress {
public:
    /**
     * Initialize the IP address to the specified address
     * :param ip_address: string
     */
    explicit IPAddress(const std::string& ip_address)
        : ip_address(ip_address) {}

    /**
     * Judge whether the IP address is valid, that is, whether the IP address
     * is composed of four decimal digits separated by '.'. Each digit is
     * greater than or equal to 0 and less than or equal to 255.
     * :return: bool
     */
    bool is_valid() const {
        std::vector<std::string> octets = split(ip_address, '.');
        if (octets.size() != 4) {
            return false;
        }
        for (const std::string& octet : octets) {
            // Equivalent of str.isdigit(): non-empty, ASCII digits only
            if (octet.empty()) {
                return false;
            }
            for (char c : octet) {
                if (c < '0' || c > '9') {
                    return false;
                }
            }
            // Numeric value; early exit keeps value bounded (no overflow,
            // and leading zeros like "0000" remain valid, matching Python)
            long long value = 0;
            for (char c : octet) {
                value = value * 10 + (c - '0');
                if (value > 255) {
                    break;
                }
            }
            if (value < 0 || value > 255) {
                return false;
            }
        }
        return true;
    }

    /**
     * If the IP address is valid, return the list of four decimal numbers
     * separated by "." constituting the IP address; otherwise return an
     * empty list.
     * :return: list of strings
     */
    std::vector<std::string> get_octets() const {
        if (is_valid()) {
            return split(ip_address, '.');
        }
        return {};
    }

    /**
     * If the IP address is valid, return the binary form of the IP address;
     * otherwise return "".
     * :return: string
     */
    std::string get_binary() const {
        if (is_valid()) {
            std::string result;
            const std::vector<std::string> octets = get_octets();
            for (std::size_t i = 0; i < octets.size(); ++i) {
                if (i > 0) {
                    result += '.';
                }
                result += format_binary_octet(std::stoi(octets[i]));
            }
            return result;
        }
        return "";
    }

private:
    std::string ip_address;

    // Mimics Python's str.split(sep): keeps empty tokens, e.g.
    // "10..10.10" -> ["10", "", "10", "10"]
    static std::vector<std::string> split(const std::string& s, char delimiter) {
        std::vector<std::string> tokens;
        std::string current;
        for (char c : s) {
            if (c == delimiter) {
                tokens.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        tokens.push_back(current);
        return tokens;
    }

    // Equivalent of Python's format(int(octet), '08b') for 0..255
    static std::string format_binary_octet(int value) {
        std::string bits(8, '0');
        for (int i = 7; i >= 0; --i) {
            bits[static_cast<std::size_t>(i)] =
                static_cast<char>('0' + (value & 1));
            value >>= 1;
        }
        return bits;
    }
};