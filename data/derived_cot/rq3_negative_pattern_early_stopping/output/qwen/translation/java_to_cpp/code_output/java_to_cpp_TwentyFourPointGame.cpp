#include <vector>
#include <string>
#include <random>
#include <cctype>
#include <stdexcept>
#include <cmath>
#include <iostream>
#include <algorithm>

class TwentyFourPointGame {
private:
    std::vector<int> nums;

    void generateCards() {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> distrib(1, 9);

        nums.clear();
        for (int i = 0; i < 4; i++) {
            nums.push_back(distrib(gen));
        }
    }

public:
    TwentyFourPointGame() {
        generateCards();
    }

    bool answer(const std::string& expression) {
        if (expression == "pass") {
            generateCards();
            return false;
        }

        // Count the digits in the expression
        std::vector<int> counts(10, 0);
        for (char c : expression) {
            if (std::isdigit(c)) {
                int digit = c - '0';
                counts[digit]++;
            }
        }

        // Check if the expression uses exactly the four numbers
        for (int num : nums) {
            if (counts[num] > 0) {
                counts[num]--;
            } else {
                return false;
            }
        }

        for (int count : counts) {
            if (count != 0) {
                return false;
            }
        }

        // Evaluate the expression
        try {
            return evaluateExpression(expression);
        } catch (...) {
            return false;
        }
    }

    bool evaluateExpression(const std::string& expression) {
        // We'll implement a recursive descent parser for the expression
        // The grammar is:
        //   expression  : term ( ('+' | '-') term )*
        //   term        : factor ( ('*' | '/') factor )*
        //   factor      : ('+' | '-') factor | primary
        //   primary     : NUMBER | '(' expression ')'

        // We'll use a simple recursive descent parser with a current position in the string.

        int pos = -1;
        char ch;

        auto nextChar = [&]() {
            ch = (++pos < expression.length()) ? expression[pos] : '\0';
        };

        auto eat = [&](char expected) {
            while (ch == ' ') nextChar();
            if (ch == expected) {
                nextChar();
                return true;
            }
            return false;
        };

        auto parseNumber = [&]() -> double {
            int startPos = pos;
            while (std::isdigit(ch)) {
                nextChar();
            }
            if (pos > startPos) {
                return std::stod(expression.substr(startPos, pos - startPos));
            }
            throw std::runtime_error("Invalid number");
        };

        auto parseFactor = [&]() -> double {
            if (eat('+')) {
                return parseFactor();
            }
            if (eat('-')) {
                return -parseFactor();
            }

            double result;
            if (ch == '(') {
                eat('(');
                result = parseExpression();
                eat(')');
            } else if (std::isdigit(ch)) {
                result = parseNumber();
            } else if (ch == '.') {
                // Handle decimal point? But note: the expression might have a decimal without integer part?
                // However, the problem says the numbers are from 1 to 9, so we don't expect a decimal point alone.
                // We'll treat it as part of a number.
                result = parseNumber();
            } else {
                throw std::runtime_error("Unexpected character");
            }

            return result;
        };

        auto parseTerm = [&]() -> double {
            double result = parseFactor();
            while (true) {
                if (eat('*')) {
                    result *= parseFactor();
                } else if (eat('/')) {
                    if (parseFactor() == 0) {
                        throw std::runtime_error("Division by zero");
                    }
                    result /= parseFactor();
                } else {
                    return result;
                }
            }
        };

        auto parseExpression = [&]() -> double {
            double result = parseTerm();
            while (true) {
                if (eat('+')) {
                    result += parseTerm();
                } else if (eat('-')) {
                    result -= parseTerm();
                } else {
                    return result;
                }
            }
        };

        nextChar(); // Start by getting the first character

        double result = parseExpression();

        // Check if we've consumed the entire string
        if (pos < expression.length()) {
            throw std::runtime_error("Unexpected characters at the end");
        }

        return fabs(result - 24.0) < 1e-6;
    }
};