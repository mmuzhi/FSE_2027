#include <string>
#include <vector>
#include <sstream>
#include <bitset>
#include <stdexcept>

class IPAddress {
private:
    std::string ipAddress;

    // Helper to split the IP string by '.'
    std::vector<std::string> splitOctets() const {
        std::vector<std::string> octets;
        std::istringstream ss(ipAddress);
        std::string token;
        while (std::getline(ss, token, '.')) {
            octets.push_back(token);
        }
        return octets;
    }

public:
    IPAddress(const std::string& ip) : ipAddress(ip) {}

    // Return true if the IP has exactly four octets, each in [0,255] and
    // parseable as a base-10 integer (no extra characters, no leading/trailing whitespace).
    bool isValid() const {
        std::vector<std::string> octets = splitOctets();
        if (octets.size() != 4) {
            return false;
        }
        for (const std::string& octet : octets) {
            try {
                size_t pos;
                int num = std::stoi(octet, &pos, 10);
                // Whole string must be consumed (no extra whitespace or non‑digit characters)
                if (pos != octet.length()) {
                    return false;
                }
                if (num < 0 || num > 255) {
                    return false;
                }
            } catch (const std::invalid_argument&) {
                return false;
            } catch (const std::out_of_range&) {
                return false;
            }
        }
        return true;
    }

    // Returns the octets as strings (original formatting, e.g., leading zeros are kept).
    // Returns an empty vector if the IP is invalid.
    std::vector<std::string> getOctets() const {
        if (isValid()) {
            return splitOctets();
        }
        return {};
    }

    // Returns the binary representation of the IP address, each octet as 8 bits,
    // separated by dots.  Returns empty string if the IP is invalid.
    std::string getBinary() const {
        if (!isValid()) {
            return "";
        }
        std::vector<std::string> octets = splitOctets();
        std::string result;
        for (const std::string& octet : octets) {
            int num = std::stoi(octet);   // safe because isValid() already checked
            result += std::bitset<8>(num).to_string() + ".";
        }
        if (!result.empty()) {
            result.pop_back();   // remove trailing dot
        }
        return result;
    }
};