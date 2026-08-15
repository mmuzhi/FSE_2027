#include <vector>
#include <string>
#include <variant>
#include <map>
#include <random>
#include <cctype>
#include <stdexcept>
#include <cassert>
#include <algorithm>
#include <cmath>

class ExprParser {
public:
    explicit ExprParser(const std::string& s) : expr(s), pos(0) {}

    double parse() {
        double val = parseExpression();
        skipWhitespace();
        if (pos != expr.size()) throw std::runtime_error("Unexpected character");
        return val;
    }

private:
    const std::string& expr;
    size_t pos;

    void skipWhitespace() {
        while (pos < expr.size() && std::isspace(static_cast<unsigned char>(expr[pos]))) pos++;
    }

    double parseExpression() {
        double val = parseTerm();
        while (true) {
            skipWhitespace();
            if (pos < expr.size() && (expr[pos] == '+' || expr[pos] == '-')) {
                char op = expr[pos++];
                double rhs = parseTerm();
                if (op == '+') val += rhs;
                else val -= rhs;
            } else {
                break;
            }
        }
        return val;
    }

    double parseTerm() {
        double val = parseFactor();
        while (true) {
            skipWhitespace();
            if (pos >= expr.size()) break;
            char c = expr[pos];
            if (c == '*') {
                pos++;
                double rhs = parseFactor();
                val *= rhs;
            } else if (c == '/') {
                if (pos + 1 < expr.size() && expr[pos + 1] == '/') {
                    pos += 2;
                    double rhs = parseFactor();
                    if (rhs == 0) throw std::runtime_error("Division by zero");
                    val = std::floor(val / rhs);
                } else {
                    pos++;
                    double rhs = parseFactor();
                    if (rhs == 0) throw std::runtime_error("Division by zero");
                    val /= rhs;
                }
            } else if (c == '%') {
                pos++;
                double rhs = parseFactor();
                if (rhs == 0) throw std::runtime_error("Modulo by zero");
                val = val - std::floor(val / rhs) * rhs;
            } else {
                break;
            }
        }
        return val;
    }

    double parseFactor() {
        skipWhitespace();
        if (pos >= expr.size()) throw std::runtime_error("Unexpected end");
        char c = expr[pos];
        if (c == '+' || c == '-') {
            pos++;
            double val = parsePower();
            return c == '-' ? -val : val;
        }
        return parsePower();
    }

    double parsePower() {
        double base = parsePrimary();
        skipWhitespace();
        if (pos + 1 < expr.size() && expr[pos] == '*' && expr[pos + 1] == '*') {
            pos += 2;
            double exponent = parseFactor();
            return std::pow(base, exponent);
        }
        return base;
    }

    double parsePrimary() {
        skipWhitespace();
        if (pos >= expr.size()) throw std::runtime_error("Unexpected end");
        char c = expr[pos];
        if (c == '(') {
            pos++;
            double val = parseExpression();
            skipWhitespace();
            if (pos >= expr.size() || expr[pos] != ')') throw std::runtime_error("Missing closing parenthesis");
            pos++;
            return val;
        }
        if (std::isdigit(static_cast<unsigned char>(c)) || c == '.') {
            return parseNumber();
        }
        throw std::runtime_error("Unexpected character");
    }

    double parseNumber() {
        skipWhitespace();
        size_t start = pos;
        bool hasDecimal = false;
        bool hasExponent = false;

        while (pos < expr.size() && std::isdigit(static_cast<unsigned char>(expr[pos]))) pos++;
        if (pos < expr.size() && expr[pos] == '.') {
            hasDecimal = true;
            pos++;
            while (pos < expr.size() && std::isdigit(static_cast<unsigned char>(expr[pos]))) pos++;
        }
        if (pos < expr.size() && (expr[pos] == 'e' || expr[pos] == 'E')) {
            hasExponent = true;
            pos++;
            if (pos < expr.size() && (expr[pos] == '+' || expr[pos] == '-')) pos++;
            if (pos >= expr.size() || !std::isdigit(static_cast<unsigned char>(expr[pos]))) {
                throw std::runtime_error("Invalid exponent");
            }
            while (pos < expr.size() && std::isdigit(static_cast<unsigned char>(expr[pos]))) pos++;
        }

        std::string numStr = expr.substr(start, pos - start);
        if (numStr.empty()) throw std::runtime_error("Invalid number");

        if (!hasDecimal && !hasExponent) {
            size_t intLen = 0;
            while (intLen < numStr.size() && std::isdigit(static_cast<unsigned char>(numStr[intLen]))) intLen++;
            if (intLen > 1 && numStr[0] == '0') {
                throw std::runtime_error("Leading zeros in integer literals");
            }
        }

        size_t processed = 0;
        double val = std::stod(numStr, &processed);
        if (processed != numStr.size()) throw std::runtime_error("Invalid number");
        return val;
    }
};

class TwentyFourPointGame {
public:
    TwentyFourPointGame() = default;

    std::vector<int> get_my_cards() {
        nums.clear();
        _generate_cards();
        return nums;
    }

    std::variant<bool, std::vector<int>> answer(const std::string& expression) {
        if (expression == "pass") {
            return get_my_cards();
        }

        std::map<char, int> statistic;
        for (char c : expression) {
            if (std::isdigit(static_cast<unsigned char>(c))) {
                int val = c - '0';
                if (std::find(nums.begin(), nums.end(), val) != nums.end()) {
                    statistic[c]++;
                }
            }
        }

        std::map<char, int> nums_used = statistic;
        for (int num : nums) {
            char key = static_cast<char>('0' + num);
            auto it = nums_used.find(key);
            if (it == nums_used.end() || it->second <= 0) {
                return false;
            }
            it->second--;
        }

        for (const auto& kv : nums_used) {
            if (kv.second != 0) {
                return false;
            }
        }

        return evaluate_expression(expression);
    }

    bool evaluate_expression(const std::string& expression) {
        try {
            ExprParser parser(expression);
            double result = parser.parse();
            return result == 24.0;
        } catch (...) {
            return false;
        }
    }

private:
    std::vector<int> nums;

    void _generate_cards() {
        static std::mt19937 rng{std::random_device{}()};
        std::uniform_int_distribution<int> dist(1, 9);
        for (int i = 0; i < 4; ++i) {
            nums.push_back(dist(rng));
        }
        assert(nums.size() == 4);
    }
};