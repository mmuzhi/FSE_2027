#include <string>
#include <algorithm>

class BigNumCalculator {
public:
    static std::string add(const std::string& num1, const std::string& num2) {
        size_t max_len = std::max(num1.size(), num2.size());
        std::string n1 = std::string(max_len - num1.size(), '0') + num1;
        std::string n2 = std::string(max_len - num2.size(), '0') + num2;

        int carry = 0;
        std::string result;
        result.reserve(max_len + 1);

        for (int i = static_cast<int>(max_len) - 1; i >= 0; --i) {
            int digit_sum = (n1[i] - '0') + (n2[i] - '0') + carry;
            carry = digit_sum / 10;
            result.push_back(static_cast<char>((digit_sum % 10) + '0'));
        }
        if (carry > 0) {
            result.push_back(static_cast<char>(carry + '0'));
        }

        std::reverse(result.begin(), result.end());
        return result;
    }

    static std::string subtract(const std::string& num1, const std::string& num2) {
        std::string n1 = num1, n2 = num2;
        bool negative = false;

        if (n1.size() < n2.size()) {
            std::swap(n1, n2);
            negative = true;
        } else if (n1.size() > n2.size()) {
            negative = false;
        } else {
            if (n1 < n2) {
                std::swap(n1, n2);
                negative = true;
            } else {
                negative = false;
            }
        }

        size_t max_len = std::max(n1.size(), n2.size());
        n1 = std::string(max_len - n1.size(), '0') + n1;
        n2 = std::string(max_len - n2.size(), '0') + n2;

        int borrow = 0;
        std::string result;
        result.reserve(max_len);

        for (int i = static_cast<int>(max_len) - 1; i >= 0; --i) {
            int digit_diff = (n1[i] - '0') - (n2[i] - '0') - borrow;
            if (digit_diff < 0) {
                digit_diff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }
            result.push_back(static_cast<char>(digit_diff + '0'));
        }

        std::reverse(result.begin(), result.end());

        // Remove leading zeros
        size_t start = 0;
        while (start < result.size() - 1 && result[start] == '0') {
            ++start;
        }
        result = result.substr(start);

        if (negative) {
            result.insert(result.begin(), '-');
        }
        return result;
    }

    static std::string multiply(const std::string& num1, const std::string& num2) {
        size_t len1 = num1.size(), len2 = num2.size();
        std::string result(len1 + len2, '0');

        for (int i = static_cast<int>(len1) - 1; i >= 0; --i) {
            for (int j = static_cast<int>(len2) - 1; j >= 0; --j) {
                int mul = (num1[i] - '0') * (num2[j] - '0');
                int p1 = i + j;
                int p2 = i + j + 1;

                int total = mul + (result[p2] - '0');
                result[p1] = static_cast<char>((result[p1] - '0') + total / 10 + '0');
                result[p2] = static_cast<char>((total % 10) + '0');
            }
        }

        size_t start = 0;
        while (start < result.size() - 1 && result[start] == '0') {
            ++start;
        }
        return result.substr(start);
    }
};