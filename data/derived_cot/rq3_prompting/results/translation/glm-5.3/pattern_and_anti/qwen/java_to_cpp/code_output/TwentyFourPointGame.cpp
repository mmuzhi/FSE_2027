#include <cstdlib>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

class TwentyFourPointGame {
private:
    std::vector<int> nums;

    std::vector<int> getMyCards() {
        std::vector<int> cards;
        std::random_device rd;
        std::mt19937 random(rd());
        std::uniform_int_distribution<int> dist(1, 9);
        for (int i = 0; i < 4; i++) {
            cards.push_back(dist(random));
        }
        return cards;
    }

public:
    TwentyFourPointGame() : nums(getMyCards()) {}

    bool answer(const std::string& expression) {
        if (expression == "pass") {
            this->nums = getMyCards();
            return false;
        }

        int counts[10] = {0};
        for (char c : expression) {
            if (c >= '0' && c <= '9') {
                counts[c - '0']++;
            }
        }

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

        return evaluateExpression(expression);
    }

    bool evaluateExpression(const std::string& expression) {
        struct Parser {
            const std::string& expression;
            int pos = -1;
            int ch = 0;

            explicit Parser(const std::string& expr) : expression(expr) {}

            void nextChar() {
                ch = (++pos < static_cast<int>(expression.length()))
                         ? static_cast<unsigned char>(expression[pos]) : -1;
            }

            bool eat(int charToEat) {
                while (ch == ' ') nextChar();
                if (ch == charToEat) {
                    nextChar();
                    return true;
                }
                return false;
            }

            double parse() {
                nextChar();
                double x = parseExpression();
                if (pos < static_cast<int>(expression.length()))
                    throw std::runtime_error("Unexpected: " + std::string(1, static_cast<char>(ch)));
                return x;
            }

            double parseExpression() {
                double x = parseTerm();
                for (;;) {
                    if (eat('+')) x += parseTerm();
                    else if (eat('-')) x -= parseTerm();
                    else return x;
                }
            }

            double parseTerm() {
                double x = parseFactor();
                for (;;) {
                    if (eat('*')) x *= parseFactor();
                    else if (eat('/')) x /= parseFactor();
                    else return x;
                }
            }

            double parseFactor() {
                if (eat('+')) return parseFactor();
                if (eat('-')) return -parseFactor();

                double x;
                int startPos = this->pos;
                if (eat('(')) {
                    x = parseExpression();
                    eat(')');
                } else if ((ch >= '0' && ch <= '9') || ch == '.') {
                    while ((ch >= '0' && ch <= '9') || ch == '.') nextChar();
                    std::string token = expression.substr(startPos, this->pos - startPos);
                    x = parseDouble(token);
                } else {
                    throw std::runtime_error("Unexpected: " + std::string(1, static_cast<char>(ch)));
                }

                return x;
            }

            // Mimics Java's Double.parseDouble strictness for tokens made of
            // digits and dots (e.g. "1.2.3" or "." must throw).
            static double parseDouble(const std::string& token) {
                int dots = 0;
                int digits = 0;
                for (char c : token) {
                    if (c == '.') dots++;
                    else digits++;
                }
                if (dots > 1 || digits == 0)
                    throw std::runtime_error("For input string: \"" + token + "\"");
                // strtod never throws; overflow yields HUGE_VAL (like Java's Infinity)
                return std::strtod(token.c_str(), nullptr);
            }
        };

        try {
            Parser parser(expression);
            return parser.parse() == 24;
        } catch (...) {
            return false;
        }
    }

    const std::vector<int>& getNums() const {
        return nums;
    }
};