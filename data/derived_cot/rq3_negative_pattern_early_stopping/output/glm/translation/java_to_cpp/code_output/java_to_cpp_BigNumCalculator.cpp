#include <iostream>
#include <string>
#include <algorithm>
#include <vector>

class BigNumCalculator {
public:
    static std::string add(std::string num1, std::string num2) {
        int maxLength = std::max(static_cast<int>(num1.length()), static_cast<int>(num2.length()));
        if (static_cast<int>(num1.length()) < maxLength) {
            num1 = std::string(maxLength - num1.length(), '0') + num1;
        }
        if (static_cast<int>(num2.length()) < maxLength) {
            num2 = std::string(maxLength - num2.length(), '0') + num2;
        }

        int carry = 0;
        std::string result;
        for (int i = maxLength - 1; i >= 0; i--) {
            int digitSum = (num1[i] - '0') + (num2[i] - '0') + carry;
            carry = digitSum / 10;
            int digit = digitSum % 10;
            result.insert(0, 1, digit + '0');
        }

        if (carry > 0) {
            result.insert(0, 1, carry + '0');
        }

        return result;
    }

    static std::string subtract(std::string num1, std::string num2) {
        bool negative = false;
        if (static_cast<int>(num1.length()) < static_cast<int>(num2.length()) || (static_cast<int>(num1.length()) == static_cast<int>(num2.length()) && num1 < num2)) {
            std::swap(num1, num2);
            negative = true;
        }

        int maxLength = std::max(static_cast<int>(num1.length()), static_cast<int>(num2.length()));
        if (static_cast<int>(num1.length()) < maxLength) {
            num1 = std::string(maxLength - num1.length(), '0') + num1;
        }
        if (static_cast<int>(num2.length()) < maxLength) {
            num2 = std::string(maxLength - num2.length(), '0') + num2;
        }

        int borrow = 0;
        std::string result;
        for (int i = maxLength - 1; i >= 0; i--) {
            int digitDiff = (num1[i] - '0') - (num2[i] - '0') - borrow;

            if (digitDiff < 0) {
                digitDiff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }

            result.insert(0, 1, digitDiff + '0');
        }

        while (static_cast<int>(result.length()) > 1 && result[0] == '0') {
            result.erase(0, 1);
        }

        if (negative) {
            result.insert(0, 1, '-');
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
        while (start < static_cast<int>(result.size()) - 1 && result[start] == 0) {
            start++;
        }

        for (int i = start; i < static_cast<int>(result.size()); i++) {
            sb += (result[i] + '0');
        }

        return sb;
    }
};

int main() {
    std::cout << BigNumCalculator::add("12345678901234567890", "98765432109876543210") << std::endl;
    std::cout << BigNumCalculator::subtract("12345678901234567890", "98765432109876543210") << std::endl;
    std::cout << BigNumCalculator::multiply("12345678901234567890", "98765432109876543210") << std::endl;
    return 0;
}