#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>
#include <vector>
#include <sstream>
#include <iomanip>

class BinaryDataProcessor {
private:
    std::string binaryString;

    // Helper function to remove non-binary characters
    void cleanNonBinaryChars() {
        binaryString.erase(std::remove_if(binaryString.begin(), binaryString.end(),
                                          [](unsigned char c) { return c != '0' && c != '1'; }),
                          binaryString.end());
    }

public:
    explicit BinaryDataProcessor(std::string binaryString) : binaryString(std::move(binaryString)) {
        cleanNonBinaryChars();
    }

    BinaryInfo calculateBinaryInfo() const {
        int zeroesCount = binaryString.length() - std::count(binaryString.begin(), binaryString.end(), '1');
        int onesCount = std::count(binaryString.begin(), binaryString.end(), '1');
        int totalLength = binaryString.length();

        double zeroesPercentage = static_cast<double>(zeroesCount) / totalLength;
        double onesPercentage = static_cast<double>(onesCount) / totalLength;

        return BinaryInfo(zeroesPercentage, onesPercentage, totalLength);
    }

    std::string convertToAscii() const {
        std::string asciiString;
        for (size_t i = 0; i < binaryString.length(); i += 8) {
            if (i + 8 > binaryString.length()) break; // Handle incomplete bytes
            std::string byteString = binaryString.substr(i, 8);
            int decimal = std::stoi(byteString, nullptr, 2);
            asciiString += static_cast<char>(decimal);
        }
        return asciiString;
    }

    std::string convertToUtf8() const {
        std::string utf8String;
        for (size_t i = 0; i < binaryString.length(); i += 8) {
            if (i + 8 > binaryString.length()) break; // Handle incomplete bytes
            std::string byteString = binaryString.substr(i, 8);
            int decimal = std::stoi(byteString, nullptr, 2);
            utf8String += static_cast<char>(decimal);
        }
        return utf8String;
    }

    std::string getBinaryString() const {
        return binaryString;
    }

    // Static helper function to create a BinaryInfo string representation
    static std::string formatBinaryInfo(const BinaryInfo& info) {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(3);
        oss << "{Zeroes: " << info.zeroes << ", Ones: " << info.ones << ", Bit length: " << info.bitLength << "}";
        return oss.str();
    }
};

class BinaryInfo {
public:
    double zeroes;
    double ones;
    int bitLength;

    explicit BinaryInfo(double zeroes, double ones, int bitLength)
        : zeroes(zeroes), ones(ones), bitLength(bitLength) {}

    // Static method to mimic the toString behavior
    std::string toString() const {
        return BinaryDataProcessor::formatBinaryInfo(*this);
    }
};

// Example main function for testing
int main() {
    BinaryDataProcessor bdp("0110100001100101011011000110110001101111");
    std::cout << bdp.getBinaryString() << std::endl;
    std::cout << bdp.calculateBinaryInfo().toString() << std::endl;
    std::cout << bdp.convertToAscii() << std::endl;
    std::cout << bdp.convertToUtf8() << std::endl;
    return 0;
}