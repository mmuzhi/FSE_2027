#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <cmath>
#include <stdexcept>
#include <algorithm>
#include <locale>

class BinaryInfo {
private:
    double zeroes;
    double ones;
    int bitLength;

    static std::string formatDouble(double value) {
        if (std::isnan(value)) return "NaN";
        if (std::isinf(value)) return value > 0 ? "Infinity" : "-Infinity";
        std::ostringstream oss;
        oss.imbue(std::locale::classic());
        oss << std::fixed << std::setprecision(3) << value;
        return oss.str();
    }

public:
    BinaryInfo(double zeroes, double ones, int bitLength)
        : zeroes(zeroes), ones(ones), bitLength(bitLength) {}

    double getZeroes() const { return zeroes; }
    double getOnes() const { return ones; }
    int getBitLength() const { return bitLength; }

    std::string toString() const {
        std::ostringstream oss;
        oss.imbue(std::locale::classic());
        oss << "{Zeroes: " << formatDouble(zeroes)
            << ", Ones: " << formatDouble(ones)
            << ", Bit length: " << bitLength << "}";
        return oss.str();
    }
};

class BinaryDataProcessor {
private:
    std::string binaryString;

    static void appendUtf8(std::string& out, int codepoint) {
        if (codepoint < 0x80) {
            out.push_back(static_cast<char>(codepoint));
        } else if (codepoint < 0x800) {
            out.push_back(static_cast<char>(0xC0 | (codepoint >> 6)));
            out.push_back(static_cast<char>(0x80 | (codepoint & 0x3F)));
        } else if (codepoint < 0x10000) {
            out.push_back(static_cast<char>(0xE0 | (codepoint >> 12)));
            out.push_back(static_cast<char>(0x80 | ((codepoint >> 6) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | (codepoint & 0x3F)));
        } else {
            out.push_back(static_cast<char>(0xF0 | (codepoint >> 18)));
            out.push_back(static_cast<char>(0x80 | ((codepoint >> 12) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | ((codepoint >> 6) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | (codepoint & 0x3F)));
        }
    }

public:
    BinaryDataProcessor(const std::string& binaryString)
        : binaryString(binaryString) {
        cleanNonBinaryChars();
    }

    void cleanNonBinaryChars() {
        std::string cleaned;
        cleaned.reserve(binaryString.size());
        for (char c : binaryString) {
            if (c == '0' || c == '1') {
                cleaned.push_back(c);
            }
        }
        binaryString = cleaned;
    }

    BinaryInfo calculateBinaryInfo() const {
        int totalLength = static_cast<int>(binaryString.size());
        int onesCount = static_cast<int>(std::count(binaryString.begin(), binaryString.end(), '1'));
        int zeroesCount = totalLength - onesCount;

        double zeroesPercentage = static_cast<double>(zeroesCount) / totalLength;
        double onesPercentage = static_cast<double>(onesCount) / totalLength;

        return BinaryInfo(zeroesPercentage, onesPercentage, totalLength);
    }

    std::string convertToAscii() const {
        std::string asciiString;
        for (std::size_t i = 0; i < binaryString.size(); i += 8) {
            if (i + 8 > binaryString.size()) {
                throw std::out_of_range("substring");
            }
            std::string byteString = binaryString.substr(i, 8);
            int decimal = std::stoi(byteString, nullptr, 2);
            appendUtf8(asciiString, decimal);
        }
        return asciiString;
    }

    std::string convertToUtf8() const {
        return convertToAscii();
    }

    std::string getBinaryString() const {
        return binaryString;
    }
};

int main() {
    BinaryDataProcessor bdp("0110100001100101011011000110110001101111");
    std::cout << bdp.getBinaryString() << std::endl;
    std::cout << bdp.calculateBinaryInfo().toString() << std::endl;
    std::cout << bdp.convertToAscii() << std::endl;
    std::cout << bdp.convertToUtf8() << std::endl;
    return 0;
}