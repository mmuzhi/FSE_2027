#include <string>
#include <vector>
#include <cctype>
#include <climits>
#include <sstream>
#include <iomanip>

class IPAddress {
private:
    std::string ipAddress;

    // Mimics Java's String.split("\\."), which drops trailing empty tokens.
    static std::vector<std::string> splitOnDots(const std::string& s) {
        std::vector<std::string> tokens;
        std::string current;
        for (char c : s) {
            if (c == '.') {
                tokens.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        tokens.push_back(current);
        while (!tokens.empty() && tokens.back().empty()) {
            tokens.pop_back();
        }
        return tokens;
    }

    // Mimics Integer.parseInt: optional sign, ASCII digits only,
    // must fit in a 32-bit int; otherwise NumberFormatException -> false here.
    static bool tryParseInt(const std::string& s, int& out) {
        if (s.empty()) return false;
        size_t i = 0;
        bool negative = false;
        if (s[0] == '+' || s[0] == '-') {
            negative = (s[0] == '-');
            i = 1;
        }
        if (i == s.size()) return false;
        long long value = 0;
        for (; i < s.size(); ++i) {
            if (!std::isdigit(static_cast<unsigned char>(s[i]))) return false;
            value = value * 10 + (s[i] - '0');
            if (value > static_cast<long long>(INT_MAX) + 1) return false;
        }
        if (negative) value = -value;
        if (value < INT_MIN || value > INT_MAX) return false;
        out = static_cast<int>(value);
        return true;
    }

public:
    IPAddress(const std::string& ipAddress) : ipAddress(ipAddress) {}

    bool isValid() const {
        std::vector<std::string> octets = splitOnDots(ipAddress);
        if (octets.size() != 4) {
            return false;
        }
        for (const std::string& octet : octets) {
            int num;
            if (!tryParseInt(octet, num)) {
                return false;
            }
            if (num < 0 || num > 255) {
                return false;
            }
        }
        return true;
    }

    std::vector<std::string> getOctets() const {
        std::vector<std::string> octetsList;
        if (isValid()) {
            std::vector<std::string> octets = splitOnDots(ipAddress);
            for (const std::string& octet : octets) {
                octetsList.push_back(octet);
            }
        }
        return octetsList;
    }

    std::string getBinary() const {
        if (isValid()) {
            std::ostringstream binaryString;
            std::vector<std::string> octets = splitOnDots(ipAddress);
            for (size_t i = 0; i < octets.size(); ++i) {
                int num = 0;
                tryParseInt(octets[i], num);
                // Equivalent to String.format("%08d", parseInt(toBinaryString(num)))
                // for values 0..255: the zero-padded decimal form of the binary digits.
                binaryString << std::setw(8) << std::setfill('0') << num;
                if (i + 1 < octets.size()) {
                    binaryString << '.';
                }
            }
            return binaryString.str();
        }
        return "";
    }
};