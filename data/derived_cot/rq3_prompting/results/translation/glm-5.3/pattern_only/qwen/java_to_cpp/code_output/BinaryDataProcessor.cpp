#include <cstdio>
#include <stdexcept>
#include <string>

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
        char buffer[128];
        std::snprintf(buffer, sizeof(buffer),
                      "{Zeroes: %.3f, Ones: %.3f, Bit length: %d}",
                      zeroes, ones, bitLength);
        return std::string(buffer);
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
        return convertBytes();
    }

    std::string convertToUtf8() const {
        return convertBytes();
    }

    std::string getBinaryString() const {
        return binaryString;
    }

private:
    // Mirrors Java substring(i, i + 8), which throws when i + 8 exceeds length.
    std::string convertBytes() const {
        std::string result;
        for (std::size_t i = 0; i < binaryString.length(); i += 8) {
            if (i + 8 > binaryString.length()) {
                throw std::out_of_range(
                    "begin " + std::to_string(i) + ", end " + std::to_string(i + 8) +
                    ", length " + std::to_string(binaryString.length()));
            }
            std::string byteString = binaryString.substr(i, 8);
            int decimal = std::stoi(byteString, nullptr, 2);
            result.push_back(static_cast<char>(decimal));
        }
        return result;
    }
};

int main() {
    BinaryDataProcessor bdp("0110100001100101011011000110110001101111");
    std::printf("%s\n", bdp.getBinaryString().c_str());
    std::printf("%s\n", bdp.calculateBinaryInfo().toString().c_str());
    std::printf("%s\n", bdp.convertToAscii().c_str());
    std::printf("%s\n", bdp.convertToUtf8().c_str());
    return 0;
}