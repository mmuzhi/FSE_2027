#include <string>
#include <vector>
#include <sstream>
#include <cctype>
#include <stdexcept>

class IPAddress {
private:
    std::string ipAddress;

    bool isParsable(const std::string& octet) const {
        if (octet.empty()) return false;
        size_t start = 0;
        if (octet[0] == '-') {
            start = 1;
        }
        if (start == octet.size()) return false;
        for (size_t i = start; i < octet.size(); ++i) {
            if (!std::isdigit(static_cast<unsigned char>(octet[i]))) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> splitByDot() const {
        std::vector<std::string> tokens;
        std::stringstream ss(ipAddress);
        std::string token;
        while (std::getline(ss, token, '.')) {
            tokens.push_back(token);
        }
        while (!tokens.empty() && tokens.back().empty()) {
            tokens.pop_back();
        }
        return tokens;
    }

public:
    IPAddress(const std::string& ipAddress) : ipAddress(ipAddress) {}

    bool isValid() const {
        std::vector<std::string> octets = splitByDot();
        if (octets.size() != 4) {
            return false;
        }
        for (const std::string& octet : octets) {
            if (!isParsable(octet)) return false;
            try {
                int num = std::stoi(octet);
                if (num < 0 || num > 255) {
                    return false;
                }
            } catch (const std::exception&) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> getOctets() const {
        std::vector<std::string> octetsList;
        if (isValid()) {
            octetsList = splitByDot();
        }
        return octetsList;
    }

    std::string getBinary() const {
        if (isValid()) {
            std::string binaryString;
            std::vector<std::string> octets = splitByDot();
            for (size_t i = 0; i < octets.size(); ++i) {
                int num = std::stoi(octets[i]);
                for (int j = 7; j >= 0; --j) {
                    binaryString += ((num >> j) & 1) ? '1' : '0';
                }
                if (i < octets.size() - 1) {
                    binaryString += ".";
                }
            }
            return binaryString;
        }
        return "";
    }
};