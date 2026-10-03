#include <string>
#include <algorithm>
#include <vector>

class BigNumCalculator {
public:
    static std::string add(std::string num1, std::string num2) {
        size_t max_length = std::max(num1.length(), num2.length());
        num1 = std::string(max_length - num1.length(), '0') + num1;
        num2 = std::string(max_length - num2.length(), '0') + num2;

        int carry = 0;
        std::string result;
        for (int i = max_length - 1; i >= 0; --i) {
            int digit_sum = (num1[i] - '0') + (num2[i] - '0') + carry;
            carry = digit_sum / 10;
            result += ('0' + (digit_sum % 10));
        }

        if (carry > 0) {
            result += ('0' + carry);
        }

        std::reverse(result.begin(), result.end());
        return result;
    }

    static std::string subtract(std::string num1, std::string num2) {
        bool negative;
        if (num1.length() < num2.length()) {
            std::swap(num1, num2);
            negative = true;
        } else if (num1.length() > num2.length()) {
            negative = false;
        } else {
            if (num1 < num2) {
                std::swap(num1, num2);
                negative = true;
            } else {
                negative = false;
            }
        }

        size_t max_length = std::max(num1.length(), num2.length());
        num1 = std::string(max_length - num1.length(), '0') + num1;
        num2 = std::string(max_length - num2.length(), '0') + num2;

        int borrow = 0;
        std::string result;
        for (int i = max_length - 1; i >= 0; --i) {
            int digit_diff = (num1[i] - '0') - (num2[i] - '0') - borrow;

            if (digit_diff < 0) {
                digit_diff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }

            result += ('0' + digit_diff);
        }

        std::reverse(result.begin(), result.end());

        size_t start = 0;
        while (result.length() > 1 && result[start] == '0') {
            start++;
        }
        result = result.substr(start);

        if (negative) {
            result.insert(result.begin(), '-');
        }

        return result;
    }

    static std::string multiply(std::string num1, std::string num2) {
        int len1 = num1.length();
        int len2 = num2.length();
        std::vector<int> result(len1 + len2, 0);

        for (int i = len1 - 1; i >= 0; --i) {
            for (int j = len2 - 1; j >= 0; --j) {
                int mul = (num1[i] - '0') * (num2[j] - '0');
                int p1 = i + j, p2 = i + j + 1;
                int total = mul + result[p2];

                result[p1] += total / 10;
                result[p2] = total % 10;
            }
        }

        int start = 0;
        while (start < (int)result.size() - 1 && result[start] == 0) {
            start++;
        }

        std::string res_str;
        for (int i = start; i < (int)result.size(); ++i) {
            res_str += ('0' + result[i]);
        }

        return res_str;
    }
};