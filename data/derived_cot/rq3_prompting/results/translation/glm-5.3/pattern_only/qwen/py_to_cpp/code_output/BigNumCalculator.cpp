#include <algorithm>
#include <stdexcept>
#include <string>
#include <vector>

class BigNumCalculator {
public:
    static std::string add(const std::string& num1, const std::string& num2) {
        std::size_t maxLength = std::max(num1.size(), num2.size());
        std::string a = padLeft(num1, maxLength);
        std::string b = padLeft(num2, maxLength);

        int carry = 0;
        std::string result;
        for (std::size_t k = maxLength; k-- > 0;) {
            int digitSum = digit(a[k]) + digit(b[k]) + carry;
            carry = digitSum / 10;
            int d = digitSum % 10;
            result.push_back(static_cast<char>('0' + d));
        }

        if (carry > 0) {
            result.push_back(static_cast<char>('0' + carry));
        }

        std::reverse(result.begin(), result.end());
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

        std::size_t maxLength = std::max(num1.size(), num2.size());
        num1 = padLeft(num1, maxLength);
        num2 = padLeft(num2, maxLength);

        int borrow = 0;
        std::string result;
        for (std::size_t k = maxLength; k-- > 0;) {
            int digitDiff = digit(num1[k]) - digit(num2[k]) - borrow;

            if (digitDiff < 0) {
                digitDiff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }

            result.push_back(static_cast<char>('0' + digitDiff));
        }

        std::reverse(result.begin(), result.end());

        while (result.size() > 1 && result[0] == '0') {
            result.erase(result.begin());
        }

        if (negative) {
            result.insert(result.begin(), '-');
        }

        return result;
    }

    static std::string multiply(const std::string& num1, const std::string& num2) {
        std::size_t len1 = num1.size(), len2 = num2.size();
        std::vector<int> result(len1 + len2, 0);

        for (std::size_t i = len1; i-- > 0;) {
            for (std::size_t j = len2; j-- > 0;) {
                int mul = digit(num1[i]) * digit(num2[j]);
                std::size_t p1 = i + j, p2 = i + j + 1;
                int total = mul + result[p2];

                result[p1] += total / 10;
                result[p2] = total % 10;
            }
        }

        std::size_t start = 0;
        while (start + 1 < result.size() && result[start] == 0) {
            start++;
        }

        std::string out;
        for (std::size_t k = start; k < result.size(); ++k) {
            out.push_back(static_cast<char>('0' + result[k]));
        }
        return out;
    }

private:
    // Mirrors Python's int(char): raises ValueError-equivalent on non-digit.
    static int digit(char c) {
        if (c < '0' || c > '9') {
            throw std::invalid_argument("invalid literal for int() with base 10");
        }
        return c - '0';
    }

    // Mirrors Python's str.zfill for non-negative digit strings.
    static std::string padLeft(const std::string& s, std::size_t width) {
        if (s.size() >= width) return s;
        return std::string(width - s.size(), '0') + s;
    }
};