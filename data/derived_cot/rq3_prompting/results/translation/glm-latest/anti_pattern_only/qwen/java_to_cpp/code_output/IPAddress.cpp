#include <string>
#include <utility>
#include <vector>

namespace org {
namespace example {

class IPAddress {
private:
    std::string ipAddress;

    // Mimics Java's String.split("\\."):
    // splits on '.', dropping trailing empty strings (Java semantics).
    static std::vector<std::string> splitOnDot(const std::string& s) {
        std::vector<std::string> parts;
        std::string current;
        for (char c : s) {
            if (c == '.') {
                parts.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        parts.push_back(current);
        // Java's split removes trailing empty strings
        // (e.g. "1.2.3.4." splits into 4 parts and is therefore valid).
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

    // Mimics Java's Integer.parseInt: optional leading '+'/'-' sign,
    // ASCII decimal digits only, must fit in a 32-bit signed int.
    // Returns false instead of throwing NumberFormatException.
    static bool parseInt(const std::string& s, int& out) {
        std::size_t i = 0;
        bool negative = false;
        if (!s.empty() && (s[0] == '+' || s[0] == '-')) {
            negative = (s[0] == '-');
            i = 1;
        }
        if (i >= s.size()) {
            return false;
        }
        long long magnitude = 0;
        for (; i < s.size(); ++i) {
            char c = s[i];
            if (c < '0' || c > '9') {
                return false;
            }
            if (magnitude > 214748364LL) {
                return false; // overflow -> NumberFormatException in Java
            }
            magnitude = magnitude * 10 + (c - '0');
        }
        if (negative) {
            if (magnitude > 2147483648LL) {
                return false;
            }
            out = (magnitude == 2147483648LL) ? (-2147483647 - 1)
                                              : static_cast<int>(-magnitude);
        } else {
            if (magnitude > 2147483647LL) {
                return false;
            }
            out = static_cast<int>(magnitude);
        }
        return true;
    }

public:
    explicit IPAddress(std::string ipAddress_) : ipAddress(std::move(ipAddress_)) {}

    bool isValid() const {
        std::vector<std::string> octets = splitOnDot(ipAddress);
        if (octets.size() != 4) {
            return false;
        }
        for (const std::string& octet : octets) {
            int num = 0;
            if (!parseInt(octet, num)) {
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
            for (const std::string& octet : splitOnDot(ipAddress)) {
                octetsList.push_back(octet);
            }
        }
        return octetsList;
    }

    std::string getBinary() const {
        if (isValid()) {
            std::string binaryString;
            for (const std::string& octet : splitOnDot(ipAddress)) {
                int num = 0;
                parseInt(octet, num);
                // Equivalent to Java's:
                // String.format("%08d", Integer.parseInt(Integer.toBinaryString(num)))
                // (num is guaranteed 0..255, so 8 zero-padded bits are identical)
                for (int bit = 7; bit >= 0; --bit) {
                    binaryString += ((num >> bit) & 1) ? '1' : '0';
                }
                binaryString += '.';
            }
            return binaryString.substr(0, binaryString.size() - 1);
        }
        return "";
    }
};

} // namespace example
} // namespace org