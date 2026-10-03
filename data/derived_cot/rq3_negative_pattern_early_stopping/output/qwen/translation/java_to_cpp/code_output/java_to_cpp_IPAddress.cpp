#include <string>
#include <vector>
#include <sstream>
#include <stdexcept>
#include <cctype> // for isspace, but we don't need it here

class IPAddress {
private:
    std::string ipAddress;

    // Helper function to split the string by '.'
    std::vector<std::string> split(const std::string& s) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(s);
        while (tokenStream >> token) {
            tokens.push_back(token);
        }
        return tokens;
    }

public:
    IPAddress(const std::string& ipAddress) : ipAddress(ipAddress) {}

    bool isValid() {
        // Split the ipAddress by '.'
        std::vector<std::string> octets = split(ipAddress);
        if (octets.size() != 4) {
            return false;
        }
        for (const auto& octet : octets) {
            try {
                int num = std::stoi(octet);
                if (num < 0 || num > 255) {
                    return false;
                }
            } catch (const std::invalid_argument& e) {
                return false;
            } catch (const std::out_of_range& e) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> getOctets() {
        if (!isValid()) {
            return {};
        }
        std::vector<std::string> octets;
        std::vector<std::string> parts = split(ipAddress);
        for (const auto& part : parts) {
            octets.push_back(part);
        }
        return octets;
    }

    std::string getBinary() {
        if (!isValid()) {
            return "";
        }
        std::vector<std::string> octets = split(ipAddress);
        std::string binaryString;
        for (size_t i = 0; i < octets.size(); i++) {
            int num;
            try {
                num = std::stoi(octets[i]);
            } catch (const std::invalid_argument& e) {
                return "";
            } catch (const std::out_of_range& e) {
                return "";
            }
            // Convert the number to binary string and pad to 8 digits
            char buffer[9];
            snprintf(buffer, sizeof(buffer), "%08d", num);
            binaryString += buffer;
            if (i < octets.size() - 1) {
                binaryString += ".";
            }
        }
        return binaryString;
    }
};