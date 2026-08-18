#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

class BigNumCalculator {
public:
    static std::string add(std::string num1, std::string num2) {
        size_t maxLength = std::max(num1.length(), num2.length());
        num1 = padLeftZeros(num1, maxLength);
        num2 = padLeftZeros(num2, maxLength);

        int carry = 0;
        std::string result;
        for (int i = static_cast<int>(maxLength) - 1; i >= 0; i--) {
            int digitSum = (num1[i] - '0') + (num2[i] - '0') + carry;
            carry = digitSum / 10;
            int digit = digitSum % 10;
            result.insert(0, std::to_string(digit));
        }

        if (carry > 0) {
            result.insert(0, std::to_string(carry));
        }

        return result;
    }

    static std::string subtract(std::string num1, std::string num2) {
        bool negative = false;
        if (num1.length() < num2.length() ||
            (num1.length() == num2.length() && num1 < num2)) {
            std::swap(num1, num2);
            negative = true;
        }

        size_t maxLength = std::max(num1.length(), num2.length());
        num1 = padLeftZeros(num1, maxLength);
        num2 = padLeftZeros(num2, maxLength);

        int borrow = 0;
        std::string result;
        for (int i = static_cast<int>(maxLength) - 1; i >= 0; i--) {
            int digitDiff = (num1[i] - '0') - (num2[i] - '0') - borrow;

            if (digitDiff < 0) {
                digitDiff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }

            result.insert(0, std::to_string(digitDiff));
        }

        while (result.length() > 1 && result[0] == '0') {
            result.erase(0, 1);
        }

        if (negative) {
            result.insert(0, "-");
        }

        return result;
    }

    static std::string multiply(const std::string& num1, const std::string& num2) {
        int len1 = static_cast<int>(num1.length());
        int len2 = static_cast<int>(num2.length());
        std::vector<int> result(len1 + len2, 0);

        for (int i = len1 - 1; i >= 0; i--) {
            for (int j = len2 - 1; j >= 0; j--) {
                int mul = (num1[i] - '0') * (num2[j] - '0');
                int p1 = i + j;
                int p2 = i + j + 1;
                int total = mul + result[p2];

                result[p1] += total / 10;
                result[p2] = total % 10;
            }
        }

        std::string sb;
        int start = 0;
        while (start < len1 + len2 - 1 && result[start] == 0) {
            start++;
        }

        for (int i = start; i < len1 + len2; i++) {
            sb += std::to_string(result[i]);
        }

        return sb;
    }

private:
    // Equivalent of String.format("%" + maxLength + "s", s).replace(' ', '0')
    // for digit strings: right-align in width maxLength, pad with '0'.
    static std::string padLeftZeros(const std::string& s, size_t maxLength) {
        if (s.length() >= maxLength) return s;
        return std::string(maxLength - s.length(), '0') + s;
    }
};

int main() {
    std::cout << BigNumCalculator::add("12345678901234567890", "98765432109876543210") << std::endl;
    std::cout << BigNumCalculator::subtract("12345678901234567890", "98765432109876543210") << std::endl;
    std::cout << BigNumCalculator::multiply("12345678901234567890", "98765432109876543210") << std::endl;
    return 0;
}