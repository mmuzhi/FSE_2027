#include <string>
#include <vector>
#include <algorithm>

std::string add(const std::string& num1, const std::string& num2) {
    int maxLength = std::max(num1.length(), num2.length());
    std::string padded1 = std::string(maxLength - num1.length(), '0') + num1;
    std::string padded2 = std::string(maxLength - num2.length(), '0') + num2;

    int carry = 0;
    std::string result;
    for (int i = maxLength - 1; i >= 0; i--) {
        int digitSum = (padded1[i] - '0') + (padded2[i] - '0') + carry;
        carry = digitSum / 10;
        int digit = digitSum % 10;
        result = char(digit + '0') + result;
    }

    if (carry) {
        result = char(carry + '0') + result;
    }

    return result;
}

std::string subtract(const std::string& num1, const std::string& num2) {
    bool negative = false;
    if ((num1.length() < num2.length()) || (num1.length() == num2.length() && num1 < num2)) {
        std::swap(num1, num2);
        negative = true;
    }

    int maxLength = std::max(num1.length(), num2.length());
    std::string padded1 = std::string(maxLength - num1.length(), '0') + num1;
    std::string padded2 = std::string(maxLength - num2.length(), '0') + num2;

    int borrow = 0;
    std::string result;
    for (int i = maxLength - 1; i >= 0; i--) {
        int digitDiff = (padded1[i] - '0') - (padded2[i] - '0') - borrow;
        if (digitDiff < 0) {
            digitDiff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        result = char(digitDiff + '0') + result;
    }

    while (result.length() > 1 && result[0] == '0') {
        result.erase(0, 1);
    }

    if (negative && !result.empty()) {
        result = '-' + result;
    }

    return result;
}

std::string multiply(const std::string& num1, const std::string& num2) {
    if (num1.empty() || num2.empty()) {
        return "0";
    }

    int len1 = num1.length();
    int len2 = num2.length();
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

    int start = 0;
    while (start < result.size() && result[start] == 0) {
        start++;
    }

    if (start == result.size()) {
        return "0";
    }

    std::string res;
    for (int i = start; i < result.size(); i++) {
        res += char(result[i] + '0');
    }

    return res;
}

int main() {
    std::cout << add("12345678901234567890", "98765432109876543210") << std::endl;
    std::cout << subtract("12345678901234567890", "98765432109876543210") << std::endl;
    std::cout << multiply("12345678901234567890", "98765432109876543210") << std::endl;
    return 0;
}