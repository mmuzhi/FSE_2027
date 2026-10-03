#include <vector>
#include <string>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <stdexcept>

class IPAddress {
private:
    std::string ip_address;

    // Helper function to split the string by delimiter and return vector of strings
    std::vector<std::string> split(const std::string& s, char delimiter) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(s);
        while (std::getline(tokenStream, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

public:
    IPAddress(const std::string& ip_address) : ip_address(ip_address) {}

    bool is_valid() {
        // Split the IP address by '.'
        std::vector<std::string> parts = split(ip_address, '.');

        // Check if there are exactly 4 parts
        if (parts.size() != 4) {
            return false;
        }

        // Check each part
        for (const auto& part : parts) {
            // Check if the part is empty
            if (part.empty()) {
                return false;
            }

            // Check if all characters in the part are digits
            for (char c : part) {
                if (!std::isdigit(static_cast<unsigned char>(c))) {
                    return false;
                }
            }

            // Convert the string to integer
            // We can use std::stoi, but note: stoi throws if the string is empty, but we already checked empty.
            try {
                int value = std::stoi(part);
                if (value < 0 || value > 255) {
                    return false;
                }
            } catch (const std::exception& e) {
                // This should not happen because we checked digits, but just in case
                return false;
            }
        }

        return true;
    }

    std::vector<std::string> get_octets() {
        if (is_valid()) {
            return split(ip_address, '.');
        } else {
            return {};
        }
    }

    std::string get_binary() {
        if (is_valid()) {
            std::vector<std::string> octets = get_octets();
            std::vector<std::string> binary_octets;
            for (const auto& octet : octets) {
                int value = std::stoi(octet);
                // Format the integer as an 8-bit binary string
                char buffer[9]; // 8 bits + null terminator
                std::sprintf(buffer, "%08d", value);
                binary_octets.push_back(buffer);
            }
            // Join the binary octets with '.'
            std::string result;
            for (size_t i = 0; i < binary_octets.size(); ++i) {
                if (i > 0) {
                    result += '.';
                }
                result += binary_octets[i];
            }
            return result;
        } else {
            return "";
        }
    }
};