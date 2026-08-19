#include <algorithm>
#include <cassert>
#include <cctype>
#include <map>
#include <random>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

/*
 * This is a game of twenty-four points, which provides to generate four
 * numbers and check whether player's expression is equal to 24.
 */

class TwentyFourPointGame {
public:
    std::vector<int> nums;

    TwentyFourPointGame() : nums(), rng(std::random_device{}()) {}

    // Generate random numbers between 1 and 9 for the cards.
    void _generate_cards() {
        for (int i = 0; i < 4; ++i) {
            std::uniform_int_distribution<int> dist(1, 9);  // randint(1, 9) inclusive
            nums.push_back(dist(rng));
        }
        assert(nums.size() == 4);
    }

    // Get a list of four random numbers between 1 and 9 representing the
    // player's cards. Returns list of integers.
    std::vector<int> get_my_cards() {
        nums.clear();
        _generate_cards();
        return nums;
    }

    // Check if a given mathematical expression using the cards can evaluate
    // to 24. If expression == "pass", returns the newly generated cards
    // (mirroring Python's mixed return type); otherwise returns bool.
    std::variant<bool, std::vector<int>> answer(const std::string& expression) {
        if (expression == "pass") {
            return get_my_cards();
        }

        std::map<std::string, int> statistic;
        for (char c : expression) {
            if (std::isdigit(static_cast<unsigned char>(c))) {
                int digit = c - '0';
                if (std::find(nums.begin(), nums.end(), digit) != nums.end()) {
                    statistic[std::string(1, c)] += 1;  // get(c, 0) + 1
                }
            }
        }

        std::map<std::string, int> nums_used = statistic;  // .copy()

        for (int num : nums) {
            auto it = nums_used.find(std::to_string(num));
            if (it != nums_used.end() && it->second > 0) {  // get(k, -100) != -100 and value > 0
                it->second -= 1;
            } else {
                return false;
            }
        }

        bool all_zero = true;  // all(count == 0 ...)
        for (const auto& kv : nums_used) {
            if (kv.second != 0) {
                all_zero = false;
                break;
            }
        }
        if (all_zero) {
            return evaluate_expression(expression);
        }
        return false;
    }

    // Evaluate a mathematical expression and check if the result is 24.
    bool evaluate_expression(const std::string& expression) {
        try {
            ExprParser parser(expression);
            return parser.parse() == 24.0;
        } catch (...) {  // except Exception -> False
            return false;
        }
    }

private:
    std::mt19937 rng;

    // Recursive-descent evaluator covering the arithmetic subset of Python's
    // eval() used by this game: int/float literals, + - * / (true division),
    // parentheses, unary +/-, and whitespace. Double arithmetic matches
    // Python's semantics; malformed input throws (caught above -> false).
    struct ExprParser {
        const std::string& s;
        std::size_t pos;

        explicit ExprParser(const std::string& str) : s(str), pos(0) {}

        void skip_ws() {
            while (pos < s.size() && std::isspace(static_cast<unsigned char>(s[pos]))) {
                ++pos;
            }
        }

        double parse() {
            double value = expression();
            skip_ws();
            if (pos != s.size()) {
                throw std::runtime_error("unexpected trailing characters");
            }
            return value;
        }

        double expression() {
            double value = term();
            while (true) {
                skip_ws();
                if (pos < s.size() && (s[pos] == '+' || s[pos] == '-')) {
                    char op = s[pos++];
                    double rhs = term();
                    value = (op == '+') ? value + rhs : value - rhs;
                } else {
                    break;
                }
            }
            return value;
        }

        double term() {
            double value = factor();
            while (true) {
                skip_ws();
                if (pos < s.size() && (s[pos] == '*' || s[pos] == '/')) {
                    char op = s[pos++];
                    double rhs = factor();
                    value = (op == '*') ? value * rhs : value / rhs;
                } else {
                    break;
                }
            }
            return value;
        }

        double factor() {
            skip_ws();
            if (pos < s.size() && (s[pos] == '+' || s[pos] == '-')) {
                char sign = s[pos++];
                double value = factor();
                return (sign == '-') ? -value : value;
            }
            if (pos < s.size() && s[pos] == '(') {
                ++pos;
                double value = expression();
                skip_ws();
                if (pos >= s.size() || s[pos] != ')') {
                    throw std::runtime_error("expected ')'");
                }
                ++pos;
                return value;
            }
            return number();
        }

        double number() {
            skip_ws();
            std::size_t start = pos;
            while (pos < s.size() &&
                   (std::isdigit(static_cast<unsigned char>(s[pos])) || s[pos] == '.')) {
                ++pos;
            }
            if (start == pos) {
                throw std::runtime_error("expected a number");
            }
            return std::stod(s.substr(start, pos - start));
        }
    };
};