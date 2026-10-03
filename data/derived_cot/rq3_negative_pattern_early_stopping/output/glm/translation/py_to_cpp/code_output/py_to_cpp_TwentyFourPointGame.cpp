#include <vector>
#include <string>
#include <random>
#include <map>
#include <variant>
#include <stdexcept>
#include <cctype>

class TwentyFourPointGame {
public:
    std::vector<int> nums;

    TwentyFourPointGame() {}

    void _generate_cards() {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> distrib(1, 9);
        for (int i = 0; i < 4; ++i) {
            nums.push_back(distrib(gen));
        }
        if (nums.size() != 4) {
            throw std::runtime_error("Assertion failed");
        }
    }

    std::vector<int> get_my_cards() {
        nums.clear();
        _generate_cards();
        return nums;
    }

    std::variant<std::vector<int>, bool> answer(const std::string& expression) {
        if (expression == "pass") {
            return get_my_cards();
        }
        std::map<char, int> statistic;
        for (char c : expression) {
            if (std::isdigit(c)) {
                int num = c - '0';
                bool in_nums = false;
                for (int n : nums) {
                    if (n == num) {
                        in_nums = true;
                        break;
                    }
                }
                if (in_nums) {
                    statistic[c]++;
                }
            }
        }

        std::map<char, int> nums_used = statistic;

        for (int num : nums) {
            char c = std::to_string(num)[0];
            if (nums_used.count(c) && nums_used[c] > 0) {
                nums_used[c]--;
            } else {
                return false;
            }
        }

        bool all_zero = true;
        for (auto const& [key, val] : nums_used) {
            if (val != 0) {
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

    bool evaluate_expression(const std::string& expression) {
        try {
            int pos = 0;
            double result = parse_expression(expression, pos);
            while (pos < expression.length() && std::isspace(expression[pos])) pos++;
            if (pos != expression.length()) return false;
            return result == 24.0;
        } catch (...) {
            return false;
        }
    }

private:
    double parse_expression(const std::string& s, int& pos) {
        double result = parse_term(s, pos);
        while (pos < s.length() && (s[pos] == '+' || s[pos] == '-')) {
            char op = s[pos++];
            double term = parse_term(s, pos);
            if (op == '+') result += term;
            else result -= term;
        }
        return result;
    }

    double parse_term(const std::string& s, int& pos) {
        double result = parse_factor(s, pos);
        while (pos < s.length() && (s[pos] == '*' || s[pos] == '/')) {
            char op = s[pos++];
            double factor = parse_factor(s, pos);
            if (op == '*') result *= factor;
            else {
                if (factor == 0.0) throw std::runtime_error("Division by zero");
                result /= factor;
            }
        }
        return result;
    }

    double parse_factor(const std::string& s, int& pos) {
        while (pos < s.length() && std::isspace(s[pos])) pos++;
        if (pos < s.length() && s[pos] == '-') {
            pos++;
            return -parse_factor(s, pos);
        }
        if (pos < s.length() && s[pos] == '+') {
            pos++;
            return parse_factor(s, pos);
        }
        if (pos < s.length() && s[pos] == '(') {
            pos++;
            double result = parse_expression(s, pos);
            while (pos < s.length() && std::isspace(s[pos])) pos++;
            if (pos < s.length() && s[pos] == ')') {
                pos++;
            } else {
                throw std::runtime_error("Mismatched parentheses");
            }
            return result;
        }
        return parse_number(s, pos);
    }

    double parse_number(const std::string& s, int& pos) {
        while (pos < s.length() && std::isspace(s[pos])) pos++;
        int start = pos;
        while (pos < s.length() && std::isdigit(s[pos])) pos++;
        if (pos < s.length() && s[pos] == '.') {
            pos++;
            while (pos < s.length() && std::isdigit(s[pos])) pos++;
        }
        if (pos < s.length() && (s[pos] == 'e' || s[pos] == 'E')) {
            pos++;
            if (pos < s.length() && (s[pos] == '+' || s[pos] == '-')) pos++;
            while (pos < s.length() && std::isdigit(s[pos])) pos++;
        }
        if (pos == start) throw std::runtime_error("Invalid number");
        return std::stod(s.substr(start, pos - start));
    }
};