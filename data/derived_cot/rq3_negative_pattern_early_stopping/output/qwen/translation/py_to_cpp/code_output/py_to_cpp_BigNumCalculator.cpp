#include <string>
#include <vector>
#include <algorithm>

class BigNumCalculator {
public:
    static std::string add(const std::string& num1, const std::string& num2) {
        if (num1.empty() && num2.empty()) return "0";
        if (num1.empty()) return num2;
        if (num2.empty()) return num1;

        std::string num1_rev = num1;
        std::string num2_rev = num2;
        std::reverse(num1_rev.begin(), num1_rev.end());
        std::reverse(num2_rev.begin(), num2_rev.end());

        int carry = 0;
        std::string result;
        int max_len = std::max(num1_rev.size(), num2_rev.size());

        for (int i = 0; i < max_len; ++i) {
            int digit1 = (i < num1_rev.size()) ? (num1_rev[i] - '0') : 0;
            int digit2 = (i < num2_rev.size()) ? (num2_rev[i] - '0') : 0;
            int sum = digit1 + digit2 + carry;
            carry = sum / 10;
            result.push_back((sum % 10) + '0');
        }

        if (carry) {
            result.push_back(carry + '0');
        }

        std::reverse(result.begin(), result.end());
        return result;
    }

    static std::string subtract(const std::string& num1, const std::string& num2) {
        if (num1 == num2) return "0";

        std::string num1_str = num1;
        std::string num2_str = num2;
        std::reverse(num1_str.begin(), num1_str.end());
        std::reverse(num2_str.begin(), num2_str.end());

        bool negative = false;
        if (num1_str.size() < num2_str.size()) {
            std::swap(num1_str, num2_str);
            negative = true;
        } else if (num1_str.size() == num2_str.size()) {
            if (num1_str < num2_str) {
                std::swap(num1_str, num2_str);
                negative = true;
            }
        }

        int borrow = 0;
        std::string result;
        int max_len = std::max(num1_str.size(), num2_str.size());

        for (int i = 0; i < max_len; ++i) {
            int digit1 = (i < num1_str.size()) ? (num1_str[i] - '0') : 0;
            int digit2 = (i < num2_str.size()) ? (num2_str[i] - '0') : 0;
            int diff = digit1 - digit2 - borrow;
            if (diff < 0) {
                diff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }
            result.push_back(diff + '0');
        }

        while (!result.empty() && result.back() == '0') {
            result.pop_back();
        }

        if (negative && !result.empty()) {
            result.push_back('-');
        }

        std::reverse(result.begin(), result.end());
        return result;
    }

    static std::string multiply(const std::string& num1, const std::string& num2) {
        if (num1 == "0" || num2 == "0") return "0";

        std::string num1_rev = num1;
        std::string num2_rev = num2;
        std::reverse(num1_rev.begin(), num1_rev.end());
        std::reverse(num2_rev.begin(), num2_str.end());

        std::vector<int> result(num1.size() + num2.size(), 0);

        for (int i = 0; i < num1_rev.size(); ++i) {
            int digit1 = num1_rev[i] - '0';
            for (int j = 0; j < num2_rev.size(); ++j) {
                int digit2 = num2_rev[j] - '0';
                int mul = digit1 * digit2;
                int p1 = i + j;
                int p2 = i + j + 1;

                result[p2] += mul;
                result[p1] += result[p2] / 10;
                result[p2] %= 10;
            }
        }

        int start = 0;
        while (start < result.size() - 1 && result[start] == 0) {
            ++start;
        }

        std::string res;
        for (int i = start; i < result.size(); ++i) {
            res.push_back(result[i] + '0');
        }

        return res;
    }
};