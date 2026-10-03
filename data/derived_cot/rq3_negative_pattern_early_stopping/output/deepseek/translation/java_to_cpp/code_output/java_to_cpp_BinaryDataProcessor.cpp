#include <iostream>
#include <string>
#include <regex>
#include <iomanip>
#include <sstream>

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

    friend std::ostream& operator<<(std::ostream& os, const BinaryInfo& info) {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(3);
        oss << "{Zeroes: " << info.zeroes
            << ", Ones: " << info.ones
            << ", Bit length: " << info.bitLength << "}";
        return os << oss.str();
    }
};

class BinaryDataProcessor {
private:
    std::string binaryString;

    void cleanNonBinaryChars() {
        std::regex nonBinary("[^01]");
        binaryString = std::regex_replace(binaryString, nonBinary, "");
    }

public:
    BinaryDataProcessor(const std::string& binaryString)
        : binaryString(binaryString) {
        cleanNonBinaryChars();
    }

    BinaryInfo calculateBinaryInfo() const {
        int totalLength = binaryString.length();
        int zeroesCount = std::count(binaryString.begin(), binaryString.end(), '0');
        int onesCount = totalLength - zeroesCount; // since only '0' and '1' remain

        double zeroesPercentage = static_cast<double>(zeroesCount) / totalLength;
        double onesPercentage = static_cast<double>(onesCount) / totalLength;

        return BinaryInfo(zeroesPercentage, onesPercentage, totalLength);
    }

    std::string convertToAscii() const {
        std::string result;
        for (size_t i = 0; i < binaryString.length(); i += 8) {
            std::string byteString = binaryString.substr(i, 8);
            int decimal = std::stoi(byteString, nullptr, 2);
            result.push_back(static_cast<char>(decimal));
        }
        return result;
    }

    std::string convertToUtf8() const {
        return convertToAscii(); // identical behavior to convertToAscii
    }

    const std::string& getBinaryString() const {
        return binaryString;
    }
};

int main() {
    BinaryDataProcessor bdp("0110100001100101011011000110110001101111");
    std::cout << bdp.getBinaryString() << std::endl;
    std::cout << bdp.calculateBinaryInfo() << std::endl;
    std::cout << bdp.convertToAscii() << std::endl;
    std::cout << bdp.convertToUtf8() << std::endl;
    return 0;
}