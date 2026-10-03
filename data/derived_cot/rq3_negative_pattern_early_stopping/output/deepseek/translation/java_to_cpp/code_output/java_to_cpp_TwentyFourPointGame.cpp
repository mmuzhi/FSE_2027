#include <vector>
#include <string>
#include <random>
#include <cctype>
#include <stdexcept>
#include <cmath>

class TwentyFourPointGame {
private:
    std::vector<int> nums;

    // Generates 4 random numbers between 1 and 9 (inclusive)
    std::vector<int> getMyCards() {
        std::vector<int> cards;
        cards.reserve(4);
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<int> dist(1, 9);
        for (int i = 0; i < 4; ++i) {
            cards.push_back(dist(gen));
        }
        return cards;
    }

    // Evaluates a mathematical expression and returns true if the result is exactly 24.
    // The parser supports +, -, *, /, parentheses, and unary +/-.
    bool evaluateExpression(const std::string& expression) {
        try {
            // Local struct to mimic the anonymous inner class from Java
            struct Parser {
                const std::string& expr;
                int pos;
                int ch;

                Parser(const std::string& s) : expr(s), pos(-1), ch(0) {}

                void nextChar() {
                    ch = (++pos < static_cast<int>(expr.length())) ? expr[pos] : -1;
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
                    if (pos < static_cast<int>(expr.length())) {
                        throw std::runtime_error("Unexpected: " + std::string(1, static_cast<char>(ch)));
                    }
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
                    int startPos = pos;
                    if (eat('(')) {
                        x = parseExpression();
                        eat(')');
                    } else if ((ch >= '0' && ch <= '9') || ch == '.') {
                        while ((ch >= '0' && ch <= '9') || ch == '.') nextChar();
                        x = std::stod(expr.substr(startPos, pos - startPos));
                    } else {
                        throw std::runtime_error("Unexpected: " + std::string(1, static_cast<char>(ch)));
                    }
                    return x;
                }
            };

            Parser parser(expression);
            double result = parser.parse();
            return result == 24.0;
        } catch (const std::exception&) {
            return false;
        } catch (...) {
            return false;
        }
    }

public:
    TwentyFourPointGame() {
        nums = getMyCards();
    }

    // Processes an answer (expression or "pass").
    // Returns true if the expression is valid and evaluates to 24.
    bool answer(const std::string& expression) {
        if (expression == "pass") {
            nums = getMyCards();
            return false;
        }

        // Count digit occurrences in the expression
        int counts[10] = {0};
        for (char c : expression) {
            if (std::isdigit(static_cast<unsigned char>(c))) {
                counts[c - '0']++;
            }
        }

        // Check that each number in nums appears exactly once
        for (int num : nums) {
            if (counts[num] > 0) {
                counts[num]--;
            } else {
                return false;
            }
        }

        // Ensure no extra digits remain
        for (int count : counts) {
            if (count != 0) {
                return false;
            }
        }

        // Evaluate the expression
        return evaluateExpression(expression);
    }

    // Returns a copy of the current numbers
    std::vector<int> getNums() const {
        return nums;
    }
};