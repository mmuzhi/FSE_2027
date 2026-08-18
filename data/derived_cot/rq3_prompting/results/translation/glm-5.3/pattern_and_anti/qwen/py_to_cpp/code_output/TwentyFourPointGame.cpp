#include <cassert>
#include <cctype>
#include <random>
#include <map>
#include <string>
#include <variant>
#include <vector>
#include <stdexcept>

// This is a game of twenty-four points, which provides to generate four numbers
// and check whether player's expression is equal to 24.

class TwentyFourPointGame {
public:
    TwentyFourPointGame() : nums() {}

    // Generate random numbers between 1 and 9 for the cards.
    void _generate_cards() {
        for (int i = 0; i < 4; ++i) {
            std::uniform_int_distribution<int> dist(1, 9);
            nums.push_back(dist(rng));
        }
        assert(nums.size() == 4);
    }

    // Get a list of four random numbers between 1 and 9 representing the player's cards.
    std::vector<int> get_my_cards() {
        nums.clear();
        _generate_cards();
        return nums;
    }

    // Check if a given mathematical expression using the cards can evaluate to 24.
    // Returns either the new card list (when expression == "pass") or a bool.
    std::variant<bool, std::vector<int>> answer(const std::string& expression) {
        if (expression == "pass") {
            return get_my_cards();
        }

        std::map<char, int> statistic;
        for (char c : expression) {
            if (std::isdigit(static_cast<unsigned char>(c))) {
                int digit = c - '0';
                for (int n : nums) {
                    if (n == digit) {
                        statistic[c] = statistic.count(c) ? statistic[c] + 1 : 1;
                        break;
                    }
                }
            }
        }

        std::map<char, int> nums_used = statistic;

        for (int num : nums) {
            char key = static_cast<char>('0' + num);
            auto it = nums_used.find(key);
            if (it != nums_used.end() && it->second > 0) {
                it->second -= 1;
            } else {
                return false;
            }
        }

        bool all_zero = true;
        for (const auto& kv : nums_used) {
            if (kv.second != 0) {
                all_zero = false;
                break;
            }
        }

        if (all_zero) {
            return evaluate_expression(expression);
        } else {
            return false;
        }
    }

    // Evaluate a mathematical expression and check if the result is 24.
    bool evaluate_expression(const std::string& expression) {
        try {
            return Parser(expression).run() == 24.0;
        } catch (...) {
            return false;
        }
    }

private:
    std::vector<int> nums;
    std::mt19937 rng{std::random_device{}()};

    // Recursive-descent evaluator covering the eval() subset used by this game:
    // +, -, *, /, parentheses, unary +/-, integer/decimal literals.
    // Invalid input throws (mirrors Python's eval exception -> return False).
    struct Parser {
        const std::string& s;
        size_t pos = 0;

        explicit Parser(const std::string& str) : s(str) {}

        void skip_ws() {
            while (pos < s.size() && std::isspace(static_cast<unsigned char>(s[pos]))) ++pos;
        }

        bool eat(char ch) {
            skip_ws();
            if (pos < s.size() && s[pos] == ch) {
                ++pos;
                return true;
            }
            return false;
        }

        double parse_expr() {
            double v = parse_term();
            while (true) {
                if (eat('+')) v += parse_term();
                else if (eat('-')) v -= parse_term();
                else return v;
            }
        }

        double parse_term() {
            double v = parse_unary();
            while (true) {
                if (eat('*')) v *= parse_unary();
                else if (eat('/')) v /= parse_unary(); // div by zero -> inf/nan, never == 24, same as Python's exception -> False
                else return v;
            }
        }

        double parse_unary() {
            skip_ws();
            if (eat('+')) return parse_unary();
            if (eat('-')) return -parse_unary();
            skip_ws();
            if (pos < s.size() && s[pos] == '(') {
                ++pos;
                double v = parse_expr();
                if (!eat(')')) throw std::runtime_error("expected )");
                return v;
            }
            return parse_number();
        }

        double parse_number() {
            skip_ws();
            size_t start = pos;
            while (pos < s.size() &&
                   (std::isdigit(static_cast<unsigned char>(s[pos])) || s[pos] == '.')) {
                ++pos;
            }
            if (start == pos) throw std::runtime_error("expected number");
            try {
                return std::stod(s.substr(start, pos - start));
            } catch (...) {
                throw std::runtime_error("bad number");
            }
        }

        double run() {
            double v = parse_expr();
            skip_ws();
            if (pos != s.size()) throw std::runtime_error("trailing characters");
            return v;
        }
    };
};