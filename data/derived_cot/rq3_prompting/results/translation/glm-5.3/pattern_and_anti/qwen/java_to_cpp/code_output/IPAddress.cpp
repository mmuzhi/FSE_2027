#include <bitset>
#include <cstddef>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

class IPAddress {
private:
    std::string ipAddress;

    // Mimics Java String.split("\\."): trailing empty tokens are removed.
    static std::vector<std::string> splitOnDot(const std::string& s) {
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

    // Mimics Integer.parseInt: optional leading '+'/'-', digits only, no whitespace,
    // no partial parses. Returns false where Java throws NumberFormatException.
    static bool parseIntJava(const std::string& s, int& out) {
        if (s.empty()) {
            return false;
        }
        std::size_t i = 0;
        bool negative = false;
        if (s[0] == '+' || s[0] == '-') {
            negative = (s[0] == '-');
            i = 1;
        }
        if (i == s.size()) { // sign only
            return false;
        }
        long long value = 0;
        for (; i < s.size(); ++i) {
            char c = s[i];
            if (c < '0' || c > '9') {
                return false;
            }
            // Capped accumulation: anything >= 256 is rejected by the caller anyway,
            // so precision beyond this bound (incl. int overflow cases) is irrelevant.
            if (value < 1000000) {
                value = value * 10 + (c - '0');
            }
        }
        if (negative) {
            value = -value;
        }
        out = static_cast<int>(value);
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
            int num;
            if (!parseIntJava(octet, num)) {
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
            std::vector<std::string> octets = splitOnDot(ipAddress);
            for (const std::string& octet : octets) {
                octetsList.push_back(octet);
            }
        }
        return octetsList;
    }

    std::string getBinary() const {
        if (isValid()) {
            std::string binaryString;
            std::vector<std::string> octets = splitOnDot(ipAddress);
            for (std::size_t i = 0; i < octets.size(); ++i) {
                int num = 0;
                parseIntJava(octets[i], num);
                // Equivalent to String.format("%08d", parseInt(toBinaryString(num)))
                // for values 0..255: 8-char zero-padded binary representation.
                binaryString += std::bitset<8>(static_cast<unsigned long long>(num)).to_string();
                if (i + 1 < octets.size()) {
                    binaryString += '.';
                }
            }
            return binaryString;
        }
        return "";
    }
};

} // namespace org::example