#include <cctype>
#include <cstdlib>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

namespace org::example {

class TwentyFourPointGame {
private:
    std::vector<int> nums;

    std::vector<int> getMyCards() {
        std::vector<int> cards;
        static thread_local std::mt19937 rng(std::random_device{}());
        std::uniform_int_distribution<int> dist(0, 8);
        for (int i = 0; i < 4; i++) {
            cards.push_back(dist(rng) + 1);
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

        std::vector<int> counts(10, 0);
        for (char c : expression) {
            if (std::isdigit(static_cast<unsigned char>(c))) {
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

    bool evaluateExpression(const std::string& expression) const {
        try {
            struct Parser {
                const std::string& expression;
                int pos = -1;
                int ch = 0;

                explicit Parser(const std::string& expr) : expression(expr) {}

                void nextChar() {
                    ch = (++pos < static_cast<int>(expression.size()))
                             ? static_cast<int>(static_cast<unsigned char>(expression[pos]))
                             : -1;
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
                    if (pos < static_cast<int>(expression.size()))
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
                        // Equivalent of Double.parseDouble: must consume the whole token
                        // (rejects ".", "1.2.3", etc., which Java rejects with NumberFormatException).
                        std::string token = expression.substr(startPos, this->pos - startPos);
                        const char* begin = token.c_str();
                        char* end = nullptr;
                        x = std::strtod(begin, &end);
                        if (end != begin + token.size()) {
                            throw std::runtime_error("For input string: \"" + token + "\"");
                        }
                    } else {
                        throw std::runtime_error("Unexpected: " + std::string(1, static_cast<char>(ch)));
                    }

                    return x;
                }
            } parser(expression);

            return parser.parse() == 24;
        } catch (...) {
            return false;
        }
    }

    const std::vector<int>& getNums() const {
        return nums;
    }
};

} // namespace org::example