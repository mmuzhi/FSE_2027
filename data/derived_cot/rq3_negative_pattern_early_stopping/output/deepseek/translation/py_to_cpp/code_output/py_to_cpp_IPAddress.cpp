#include <string>
#include <vector>
#include <sstream>
#include <bitset>
#include <cctype>

class IPAddress {
private:
    std::string ip_address;

    // Helper: split a string by a delimiter, returning a vector of substrings
    static std::vector<std::string> split(const std::string& str, char delimiter) {
        std::vector<std::string> tokens;
        std::stringstream ss(str);
        std::string token;
        while (std::getline(ss, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

public:
    // Constructor
    IPAddress(const std::string& ip_addr) : ip_address(ip_addr) {}

    // Check if the IP address is valid (four decimal octets, each 0-255)
    bool is_valid() const {
        auto octets = split(ip_address, '.');
        if (octets.size() != 4) return false;

        for (const auto& octet : octets) {
            // Check that the octet is non-empty and contains only digits
            if (octet.empty()) return false;
            for (char ch : octet) {
                if (!std::isdigit(ch)) return false;
            }
            // Convert to integer and check range
            int value = std::stoi(octet);
            if (value < 0 || value > 255) return false;
        }
        return true;
    }

    // Return the four octets as strings if valid, else empty vector
    std::vector<std::string> get_octets() const {
        if (is_valid()) {
            return split(ip_address, '.');
        }
        return {};
    }

    // Return binary representation (e.g., "00001010.00001010.00001010.00001010") if valid, else empty string
    std::string get_binary() const {
        if (!is_valid()) return "";
        std::vector<std::string> binary_octets;
        auto octets = split(ip_address, '.');
        for (const auto& octet : octets) {
            int value = std::stoi(octet);
            std::bitset<8> bits(value);
            binary_octets.push_back(bits.to_string());
        }
        // Join with '.'
        std::string result;
        for (size_t i = 0; i < binary_octets.size(); ++i) {
            if (i > 0) result += ".";
            result += binary_octets[i];
        }
        return result;
    }
};