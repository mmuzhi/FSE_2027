#include <string>
#include <algorithm>
#include <iostream>

std::string add(const std::string& num1, const std::string& num2) {
    int maxLength = std::max(num1.size(), num2.size());
    std::string a = std::string(maxLength - num1.size(), '0') + num1;
    std::string b = std::string(maxLength - num2.size(), '0') + num2;

    int carry = 0;
    std::string result;
    result.reserve(maxLength + 1);
    for (int i = maxLength - 1; i >= 0; --i) {
        int digitSum = (a[i] - '0') + (b[i] - '0') + carry;
        carry = digitSum / 10;
        digitSum %= 10;
        result.push_back('0' + digitSum);
    }
    if (carry > 0) {
        result.push_back('0' + carry);
    }
    std::reverse(result.begin(), result.end());
    return result;
}

std::string subtract(const std::string& num1, const std::string& num2) {
    // Ensure num1 >= num2
    std::string a = num1;
    std::string b = num2;
    bool negative = false;
    if (a.size() < b.size() || (a.size() == b.size() && a < b)) {
        std::swap(a, b);
        negative = true;
    }

    int maxLength = a.size();
    a = std::string(maxLength - a.size(), '0') + a;  // a already at maxLength
    b = std::string(maxLength - b.size(), '0') + b;

    int borrow = 0;
    std::string result;
    result.reserve(maxLength);
    for (int i = maxLength - 1; i >= 0; --i) {
        int digitDiff = (a[i] - '0') - (b[i] - '0') - borrow;
        if (digitDiff < 0) {
            digitDiff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        result.push_back('0' + digitDiff);
    }
    while (result.size() > 1 && result.back() == '0') {
        result.pop_back();
    }
    if (negative) {
        result.push_back('-');
    }
    std::reverse(result.begin(), result.end());
    return result;
}

std::string multiply(const std::string& num1, const std::string& num2) {
    int len1 = num1.size();
    int len2 = num2.size();
    int* result = new int[len1 + len2]();  // zero-initialized

    for (int i = len1 - 1; i >= 0; --i) {
        for (int j = len2 - 1; j >= 0; --j) {
            int mul = (num1[i] - '0') * (num2[j] - '0');
            int p1 = i + j;
            int p2 = i + j + 1;
            int total = mul + result[p2];

            result[p1] += total / 10;
            result[p2] = total % 10;
        }
    }

    std::string sb;
    sb.reserve(len1 + len2);
    int start = 0;
    while (start < len1 + len2 - 1 && result[start] == 0) {
        ++start;
    }
    for (int i = start; i < len1 + len2; ++i) {
        sb.push_back('0' + result[i]);
    }

    delete[] result;
    return sb;
}

int main() {
    std::cout << add("12345678901234567890", "98765432109876543210") << std::endl;
    std::cout << subtract("12345678901234567890", "98765432109876543210") << std::endl;
    std::cout << multiply("12345678901234567890", "98765432109876543210") << std::endl;
    return 0;
}