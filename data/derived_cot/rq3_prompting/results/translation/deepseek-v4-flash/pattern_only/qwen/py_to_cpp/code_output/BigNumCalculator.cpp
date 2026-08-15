#include <string>
#include <vector>
#include <algorithm>
#include <utility>

class BigNumCalculator {
public:
    static std::string add(const std::string& num1, const std::string& num2) {
        size_t max_length = std::max(num1.size(), num2.size());
        std::string a = num1;
        std::string b = num2;

        if (a.size() < max_length) a.insert(0, max_length - a.size(), '0');
        if (b.size() < max_length) b.insert(0, max_length - b.size(), '0');

        int carry = 0;
        std::string result;
        result.reserve(max_length + 1);

        for (int i = static_cast<int>(max_length) - 1; i >= 0; --i) {
            int digit_sum = (a[i] - '0') + (b[i] - '0') + carry;
            carry = digit_sum / 10;
            result.push_back(static_cast<char>('0' + digit_sum % 10));
        }

        if (carry > 0) {
            result.push_back(static_cast<char>('0' + carry));
        }

        std::reverse(result.begin(), result.end());
        return result;
    }

    static std::string subtract(const std::string& num1, const std::string& num2) {
        std::string a = num1;
        std::string b = num2;
        bool negative = false;

        if (a.size() < b.size()) {
            std::swap(a, b);
            negative = true;
        } else if (a.size() > b.size()) {
            negative = false;
        } else {
            if (a < b) {
                std::swap(a, b);
                negative = true;
            } else {
                negative = false;
            }
        }

        size_t max_length = std::max(a.size(), b.size());
        if (a.size() < max_length) a.insert(0, max_length - a.size(), '0');
        if (b.size() < max_length) b.insert(0, max_length - b.size(), '0');

        int borrow = 0;
        std::string result;
        result.reserve(max_length + 1);

        for (int i = static_cast<int>(max_length) - 1; i >= 0; --i) {
            int digit_diff = (a[i] - '0') - (b[i] - '0') - borrow;
            if (digit_diff < 0) {
                digit_diff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }
            result.push_back(static_cast<char>('0' + digit_diff));
        }

        std::reverse(result.begin(), result.end());

        if (result.empty()) {
            return "";
        }

        size_t pos = result.find_first_not_of('0');
        if (pos == std::string::npos) {
            result = "0";
        } else if (pos > 0) {
            result.erase(0, pos);
        }

        if (negative) {
            result.insert(result.begin(), '-');
        }

        return result;
    }

    static std::string multiply(const std::string& num1, const std::string& num2) {
        int len1 = static_cast<int>(num1.size());
        int len2 = static_cast<int>(num2.size());
        std::vector<int> result(len1 + len2, 0);

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

        if (result.empty()) {
            return "";
        }

        int start = 0;
        while (start < static_cast<int>(result.size()) - 1 && result[start] == 0) {
            ++start;
        }

        std::string out;
        out.reserve(static_cast<size_t>(result.size() - start));
        for (int i = start; i < static_cast<int>(result.size()); ++i) {
            out.push_back(static_cast<char>('0' + result[i]));
        }

        return out;
    }
};