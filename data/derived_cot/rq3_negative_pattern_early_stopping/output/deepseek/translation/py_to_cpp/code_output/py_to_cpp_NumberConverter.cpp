#include <string>
#include <sstream>
#include <bitset>
#include <algorithm>

class NumberConverter {
public:
    static std::string decimal_to_binary(int decimal_num) {
        if (decimal_num == 0) return "0";
        std::string bin;
        while (decimal_num > 0) {
            bin += (decimal_num % 2) ? '1' : '0';
            decimal_num /= 2;
        }
        std::reverse(bin.begin(), bin.end());
        return bin;
    }

    static int binary_to_decimal(const std::string& binary_num) {
        return std::stoi(binary_num, nullptr, 2);
    }

    static std::string decimal_to_octal(int decimal_num) {
        std::ostringstream oss;
        oss << std::oct << decimal_num;
        return oss.str();
    }

    static int octal_to_decimal(const std::string& octal_num) {
        return std::stoi(octal_num, nullptr, 8);
    }

    static std::string decimal_to_hex(int decimal_num) {
        std::ostringstream oss;
        oss << std::hex << decimal_num;
        return oss.str();
    }

    static int hex_to_decimal(const std::string& hex_num) {
        return std::stoi(hex_num, nullptr, 16);
    }
};