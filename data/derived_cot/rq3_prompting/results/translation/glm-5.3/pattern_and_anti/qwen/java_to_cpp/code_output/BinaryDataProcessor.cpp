#include <iostream>
#include <string>
#include <stdexcept>
#include <cstdio>

class BinaryInfo {
private:
    double zeroes;
    double ones;
    int bitLength;

public:
    BinaryInfo(double zeroes, double ones, int bitLength)
        : zeroes(zeroes), ones(ones), bitLength(bitLength) {}

    double getZeroes() const { return zeroes; }
    double getOnes() const { return ones; }
    int getBitLength() const { return bitLength; }

    std::string toString() const {
        char buf[128];
        std::snprintf(buf, sizeof(buf),
                      "{Zeroes: %.3f, Ones: %.3f, Bit length: %d}",
                      zeroes, ones, bitLength);
        return std::string(buf);
    }
};

class BinaryDataProcessor {
private:
    std::string binaryString;

public:
    explicit BinaryDataProcessor(const std::string& binaryString)
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
        int zeroesCount = 0;
        int onesCount = 0;
        for (char c : binaryString) {
            if (c == '0') {
                ++zeroesCount;
            } else if (c == '1') {
                ++onesCount;
            }
        }
        int totalLength = static_cast<int>(binaryString.length());

        double zeroesPercentage = static_cast<double>(zeroesCount) / totalLength;
        double onesPercentage = static_cast<double>(onesCount) / totalLength;

        return BinaryInfo(zeroesPercentage, onesPercentage, totalLength);
    }

    std::string convertToAscii() const {
        std::string asciiString;
        for (std::size_t i = 0; i < binaryString.length(); i += 8) {
            if (i + 8 > binaryString.length()) {
                throw std::out_of_range("begin " + std::to_string(i) +
                                        ", end " + std::to_string(i + 8) +
                                        ", length " + std::to_string(binaryString.length()));
            }
            std::string byteString = binaryString.substr(i, 8);
            int decimal = 0;
            for (char c : byteString) {
                decimal = decimal * 2 + (c - '0');
            }
            asciiString.push_back(static_cast<char>(decimal));
        }
        return asciiString;
    }

    std::string convertToUtf8() const {
        std::string utf8String;
        for (std::size_t i = 0; i < binaryString.length(); i += 8) {
            if (i + 8 > binaryString.length()) {
                throw std::out_of_range("begin " + std::to_string(i) +
                                        ", end " + std::to_string(i + 8) +
                                        ", length " + std::to_string(binaryString.length()));
            }
            std::string byteString = binaryString.substr(i, 8);
            int decimal = 0;
            for (char c : byteString) {
                decimal = decimal * 2 + (c - '0');
            }
            utf8String.push_back(static_cast<char>(decimal));
        }
        return utf8String;
    }

    std::string getBinaryString() const {
        return binaryString;
    }
};

int main() {
    BinaryDataProcessor bdp("0110100001100101011011000110110001101111");
    std::cout << bdp.getBinaryString() << "\n";
    std::cout << bdp.calculateBinaryInfo().toString() << "\n";
    std::cout << bdp.convertToAscii() << "\n";
    std::cout << bdp.convertToUtf8() << "\n";
    return 0;
}