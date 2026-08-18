#include <string>
#include <vector>
#include <algorithm>

class BigNumCalculator {
public:
    static std::string add(const std::string& num1, const std::string& num2) {
        std::size_t max_length = std::max(num1.size(), num2.size());
        std::string n1 = zfill(num1, max_length);
        std::string n2 = zfill(num2, max_length);

        int carry = 0;
        std::string result;
        for (int i = static_cast<int>(max_length) - 1; i >= 0; --i) {
            int digit_sum = digit(n1[i]) + digit(n2[i]) + carry;
            carry = digit_sum / 10;
            int d = digit_sum % 10;
            result.insert(result.begin(), static_cast<char>('0' + d));
        }

        if (carry > 0) {
            result.insert(result.begin(), static_cast<char>('0' + carry));
        }

        return result;
    }

    static std::string subtract(std::string num1, std::string num2) {
        bool negative;
        if (num1.size() < num2.size()) {
            std::swap(num1, num2);
            negative = true;
        } else if (num1.size() > num2.size()) {
            negative = false;
        } else {
            if (num1 < num2) {
                std::swap(num1, num2);
                negative = true;
            } else {
                negative = false;
            }
        }

        std::size_t max_length = std::max(num1.size(), num2.size());
        num1 = zfill(num1, max_length);
        num2 = zfill(num2, max_length);

        int borrow = 0;
        std::string result;
        for (int i = static_cast<int>(max_length) - 1; i >= 0; --i) {
            int digit_diff = digit(num1[i]) - digit(num2[i]) - borrow;

            if (digit_diff < 0) {
                digit_diff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }

            result.insert(result.begin(), static_cast<char>('0' + digit_diff));
        }

        while (result.size() > 1 && result[0] == '0') {
            result.erase(result.begin());
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
                int mul = digit(num1[i]) * digit(num2[j]);
                int p1 = i + j, p2 = i + j + 1;
                int total = mul + result[p2];

                result[p1] += total / 10;
                result[p2] = total % 10;
            }
        }

        int start = 0;
        while (start < static_cast<int>(result.size()) - 1 && result[start] == 0) {
            ++start;
        }

        std::string out;
        for (int k = start; k < static_cast<int>(result.size()); ++k) {
            out += static_cast<char>('0' + result[k]);
        }
        return out;
    }

private:
    static std::string zfill(const std::string& s, std::size_t width) {
        if (s.size() >= width) return s;
        return std::string(width - s.size(), '0') + s;
    }

    static int digit(char c) {
        return c - '0';
    }
};