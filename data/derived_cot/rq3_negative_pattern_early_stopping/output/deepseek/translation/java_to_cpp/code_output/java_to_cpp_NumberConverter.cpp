#include <string>
#include <bitset>
#include <sstream>
#include <cstdlib>
#include <climits>
#include <stdexcept>

class NumberConverter {
public:
    static std::string decimalToBinary(int decimalNum) {
        if (decimalNum >= 0) {
            if (decimalNum == 0) return "0";
            std::string bin;
            int num = decimalNum;
            while (num > 0) {
                bin = (num % 2 == 0 ? "0" : "1") + bin;
                num /= 2;
            }
            return bin;
        } else {
            unsigned int u = static_cast<unsigned int>(decimalNum);
            std::bitset<32> bits(u);
            return bits.to_string();
        }
    }

    static int binaryToDecimal(const std::string& binaryNum) {
        if (binaryNum.empty()) throw std::invalid_argument("For input string: \"" + binaryNum + "\"");
        char* end;
        long val = strtol(binaryNum.c_str(), &end, 2);
        if (*end != '\0' || end == binaryNum.c_str()) {
            throw std::invalid_argument("For input string: \"" + binaryNum + "\"");
        }
        if (val > static_cast<long>(INT_MAX) || val < static_cast<long>(INT_MIN)) {
            throw std::invalid_argument("For input string: \"" + binaryNum + "\"");
        }
        return static_cast<int>(val);
    }

    static std::string decimalToOctal(int decimalNum) {
        if (decimalNum >= 0) {
            if (decimalNum == 0) return "0";
            std::string oct;
            int num = decimalNum;
            while (num > 0) {
                oct = std::to_string(num % 8) + oct;
                num /= 8;
            }
            return oct;
        } else {
            unsigned int u = static_cast<unsigned int>(decimalNum);
            std::ostringstream ss;
            ss << std::oct << u;
            return ss.str();
        }
    }

    static int octalToDecimal(const std::string& octalNum) {
        if (octalNum.empty()) throw std::invalid_argument("For input string: \"" + octalNum + "\"");
        char* end;
        long val = strtol(octalNum.c_str(), &end, 8);
        if (*end != '\0' || end == octalNum.c_str()) {
            throw std::invalid_argument("For input string: \"" + octalNum + "\"");
        }
        if (val > static_cast<long>(INT_MAX) || val < static_cast<long>(INT_MIN)) {
            throw std::invalid_argument("For input string: \"" + octalNum + "\"");
        }
        return static_cast<int>(val);
    }

    static std::string decimalToHex(int decimalNum) {
        std::ostringstream ss;
        if (decimalNum >= 0) {
            if (decimalNum == 0) return "0";
            ss << std::hex << decimalNum;
            return ss.str();
        } else {
            unsigned int u = static_cast<unsigned int>(decimalNum);
            ss << std::hex << u;
            return ss.str();
        }
    }

    static int hexToDecimal(const std::string& hexNum) {
        if (hexNum.empty()) throw std::invalid_argument("For input string: \"" + hexNum + "\"");
        char* end;
        long val = strtol(hexNum.c_str(), &end, 16);
        if (*end != '\0' || end == hexNum.c_str()) {
            throw std::invalid_argument("For input string: \"" + hexNum + "\"");
        }
        if (val > static_cast<long>(INT_MAX) || val < static_cast<long>(INT_MIN)) {
            throw std::invalid_argument("For input string: \"" + hexNum + "\"");
        }
        return static_cast<int>(val);
    }
};