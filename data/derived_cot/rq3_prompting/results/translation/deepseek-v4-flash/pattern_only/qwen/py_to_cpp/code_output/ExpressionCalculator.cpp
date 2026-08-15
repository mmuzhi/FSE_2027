#include <deque>
#include <string>
#include <vector>
#include <cctype>
#include <sstream>
#include <stdexcept>
#include <algorithm>
#include <boost/multiprecision/cpp_dec_float.hpp>

using Decimal = boost::multiprecision::number<boost::multiprecision::cpp_dec_float<28>>;

class ExpressionCalculator {
public:
    ExpressionCalculator() : operat_priority({0, 3, 2, 1, -1, 1, 0, 2}) {}

    double calculate(const std::string& expression) {
        prepare(transform(expression));

        std::deque<std::string> result_stack;
        while (!postfix_stack.empty()) {
            std::string current_op = postfix_stack.front();
            postfix_stack.pop_front();

            if (!(current_op.size() == 1 && is_operator(current_op[0]))) {
                std::replace(current_op.begin(), current_op.end(), '~', '-');
                result_stack.push_back(current_op);
            } else {
                std::string second_value = result_stack.back();
                result_stack.pop_back();
                std::string first_value = result_stack.back();
                result_stack.pop_back();

                std::replace(first_value.begin(), first_value.end(), '~', '-');
                std::replace(second_value.begin(), second_value.end(), '~', '-');

                Decimal temp_result = _calculate(first_value, second_value, current_op[0]);
                result_stack.push_back(temp_result.str());
            }
        }

        if (result_stack.empty()) {
            throw std::runtime_error("Empty expression");
        }

        double result = 1.0;
        for (const auto& s : result_stack) {
            double val = std::stod(s);
            if (s == "-0") val = 0.0;  // Python eval("-0") yields int 0, then float 0.0
            result *= val;
        }
        return result;
    }

    void prepare(const std::string& expression) {
        std::deque<char> op_stack;
        op_stack.push_back(',');

        const std::string& arr = expression;
        size_t current_index = 0;
        size_t count = 0;

        for (size_t i = 0; i < arr.size(); ++i) {
            char current_op = arr[i];
            if (is_operator(current_op)) {
                if (count > 0) {
                    postfix_stack.push_back(arr.substr(current_index, count));
                }

                char peek_op = op_stack.back();
                if (current_op == ')') {
                    while (op_stack.back() != '(') {
                        postfix_stack.push_back(std::string(1, op_stack.back()));
                        op_stack.pop_back();
                    }
                    op_stack.pop_back(); // remove '('
                } else {
                    while (current_op != '(' && peek_op != ',' && compare(current_op, peek_op)) {
                        postfix_stack.push_back(std::string(1, op_stack.back()));
                        op_stack.pop_back();
                        peek_op = op_stack.back();
                    }
                    op_stack.push_back(current_op);
                }

                count = 0;
                current_index = i + 1;
            } else {
                ++count;
            }
        }

        if (count > 0) {
            postfix_stack.push_back(arr.substr(current_index, count));
        }

        while (op_stack.back() != ',') {
            postfix_stack.push_back(std::string(1, op_stack.back()));
            op_stack.pop_back();
        }
    }

    static bool is_operator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/' || c == '(' || c == ')' || c == '%';
    }

    bool compare(char cur, char peek) {
        if (cur == '%') cur = '/';
        if (peek == '%') peek = '/';
        return operat_priority[peek - 40] >= operat_priority[cur - 40];
    }

    static Decimal _calculate(const std::string& first_value, const std::string& second_value, char current_op) {
        Decimal first(first_value);
        Decimal second(second_value);

        switch (current_op) {
            case '+':
                return first + second;
            case '-':
                return first - second;
            case '*':
                return first * second;
            case '/':
                if (second == 0) {
                    throw std::runtime_error("DivisionByZero");
                }
                return first / second;
            case '%':
                if (second == 0) {
                    throw std::runtime_error("DivisionByZero");
                }
                {
                    Decimal quotient = boost::multiprecision::floor(first / second);
                    return first - quotient * second;
                }
            default:
                throw std::invalid_argument(std::string("Unexpected operator: ") + current_op);
        }
    }

    static std::string transform(const std::string& expression) {
        std::string s;
        for (char c : expression) {
            if (!std::isspace(static_cast<unsigned char>(c))) {
                s += c;
            }
        }

        if (!s.empty() && s.back() == '=') {
            s.pop_back();
        }

        for (size_t i = 0; i < s.size(); ++i) {
            if (s[i] == '-') {
                if (i == 0) {
                    s[i] = '~';
                } else {
                    char prev_c = s[i - 1];
                    if (prev_c == '+' || prev_c == '-' || prev_c == '*' || prev_c == '/' ||
                        prev_c == '(' || prev_c == 'E' || prev_c == 'e') {
                        s[i] = '~';
                    }
                }
            }
        }

        if (!s.empty() && s[0] == '~' && s.size() > 1 && s[1] == '(') {
            s[0] = '-';
            return "0" + s;
        }
        return s;
    }

private:
    std::deque<std::string> postfix_stack;
    std::vector<int> operat_priority;
};