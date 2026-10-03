#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <bitset>

class IPAddress {
private:
    std::string ip_address;

    std::vector<std::string> split_by_dot() const {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(ip_address);
        while (std::getline(tokenStream, token, '.')) {
            tokens.push_back(token);
        }
        if (ip_address.empty() || ip_address.back() == '.') {
            tokens.push_back("");
        }
        return tokens;
    }

public:
    IPAddress(const std::string& ip_address) : ip_address(ip_address) {}

    bool is_valid() const {
        std::vector<std::string> octets = split_by_dot();
        if (octets.size() != 4) {
            return false;
        }
        for (const auto& octet : octets) {
            if (octet.empty() || !std::all_of(octet.begin(), octet.end(), [](unsigned char c){ return std::isdigit(c); })) {
                return false;
            }
            if (octet.size() > 3) return false;
            try {
                int val = std::stoi(octet);
                if (val < 0 || val > 255) return false;
            } catch (...) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> get_octets() const {
        if (is_valid()) {
            return split_by_dot();
        } else {
            return {};
        }
    }

    std::string get_binary() const {
        if (is_valid()) {
            std::string result;
            std::vector<std::string> octets = get_octets();
            for (size_t i = 0; i < octets.size(); ++i) {
                if (i > 0) result += ".";
                result += std::bitset<8>(std::stoi(octets[i])).to_string();
            }
            return result;
        } else {
            return "";
        }
    }
};