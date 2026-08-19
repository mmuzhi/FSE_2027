#include <cerrno>
#include <cstdlib>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

class TwentyFourPointGame {
private:
    std::vector<int> nums;

    // Equivalent of Java's Double.parseDouble: throws if the whole string
    // is not consumed (e.g. "1.2.3" or "." -> exception -> answer false).
    static double parseDoubleExact(const std::string& s) {
        const char* cstr = s.c_str();
        char* end = nullptr;
        errno = 0;
        double value = std::strtod(cstr, &end);
        if (end != cstr + s.size()) {
            throw std::runtime_error("For input string: \"" + s + "\"");
        }
        return value;
    }

    std::vector<int> getMyCards() {
        std::vector<int> cards;
        std::mt19937 random(std::random_device{}());
        std::uniform_int_distribution<int> dist(1, 9);
        cards.reserve(4);
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
        try {
            struct Parser {
                const std::string& expression;
                int pos = -1;
                int ch = 0;

                explicit Parser(const std::string& expr) : expression(expr) {}

                void nextChar() {
                    ch = (++pos < static_cast<int>(expression.size()))
                             ? static_cast<unsigned char>(expression[static_cast<size_t>(pos)])
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
                        x = parseDoubleExact(expression.substr(static_cast<size_t>(startPos),
                                                               static_cast<size_t>(this->pos - startPos)));
                    } else {
                        throw std::runtime_error("Unexpected: " + std::string(1, static_cast<char>(ch)));
                    }

                    return x;
                }
            } parser(expression);

            return parser.parse() == 24;
        } catch (const std::exception&) {
            return false;
        }
    }

    std::vector<int> getNums() const {
        return nums;
    }
};