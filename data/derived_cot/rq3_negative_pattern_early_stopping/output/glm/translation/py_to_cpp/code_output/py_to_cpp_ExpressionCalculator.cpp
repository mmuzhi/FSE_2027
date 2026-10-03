#include <string>
#include <deque>
#include <algorithm>
#include <cctype>
#include <cmath>
#include <stdexcept>

class ExpressionCalculator {
public:
    std::deque<std::string> postfix_stack;
    int operat_priority[8] = {0, 3, 2, 1, -1, 1, 0, 2};

    ExpressionCalculator() = default;

    double calculate(const std::string& expression) {
        prepare(transform(expression));

        std::deque<double> result_stack;
        std::reverse(postfix_stack.begin(), postfix_stack.end());

        while (!postfix_stack.empty()) {
            std::string current_op = postfix_stack.back();
            postfix_stack.pop_back();

            bool is_op = current_op.size() == 1 && is_operator(current_op[0]);

            if (!is_op) {
                std::string temp = current_op;
                size_t pos;
                while ((pos = temp.find("~")) != std::string::npos) {
                    temp.replace(pos, 1, "-");
                }
                result_stack.push_back(std::stod(temp));
            } else {
                double second_value = result_stack.back();
                result_stack.pop_back();
                double first_value = result_stack.back();
                result_stack.pop_back();

                double temp_result = _calculate(first_value, second_value, current_op[0]);
                result_stack.push_back(temp_result);
            }
        }

        double final_result = 1.0;
        for (double val : result_stack) {
            final_result *= val;
        }
        return final_result;
    }

    void prepare(const std::string& expression) {
        std::deque<char> op_stack;
        op_stack.push_back(',');

        int current_index = 0;
        int count = 0;

        for (int i = 0; i < (int)expression.size(); ++i) {
            char current_op = expression[i];
            if (is_operator(current_op)) {
                if (count > 0) {
                    postfix_stack.push_back(expression.substr(current_index, count));
                }
                char peek_op = op_stack.back();
                if (current_op == ')') {
                    while (op_stack.back() != '(') {
                        postfix_stack.push_back(std::string(1, op_stack.back()));
                        op_stack.pop_back();
                    }
                    op_stack.pop_back();
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
                count += 1;
            }
        }

        if (count > 1 || (count == 1 && !is_operator(expression[current_index]))) {
            postfix_stack.push_back(expression.substr(current_index, count));
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

    static double _calculate(double first_value, double second_value, char current_op) {
        if (current_op == '+') {
            return first_value + second_value;
        } else if (current_op == '-') {
            return first_value - second_value;
        } else if (current_op == '*') {
            return first_value * second_value;
        } else if (current_op == '/') {
            return first_value / second_value;
        } else if (current_op == '%') {
            double mod = std::fmod(first_value, second_value);
            if (mod != 0 && ((first_value < 0) != (second_value < 0))) {
                mod += second_value;
            }
            return mod;
        } else {
            throw std::invalid_argument("Unexpected operator: " + std::string(1, current_op));
        }
    }

    static std::string transform(std::string expression) {
        std::string result;
        result.reserve(expression.size());
        for (char c : expression) {
            if (!std::isspace(static_cast<unsigned char>(c))) {
                result += c;
            }
        }
        if (!result.empty() && result.back() == '=') {
            result.pop_back();
        }

        std::string arr = result;
        for (size_t i = 0; i < arr.size(); ++i) {
            if (arr[i] == '-') {
                if (i == 0) {
                    arr[i] = '~';
                } else {
                    char prev_c = arr[i - 1];
                    if (prev_c == '+' || prev_c == '-' || prev_c == '*' || prev_c == '/' || prev_c == '(' || prev_c == 'E' || prev_c == 'e') {
                        arr[i] = '~';
                    }
                }
            }
        }

        if (arr[0] == '~' && arr.size() > 1 && arr[1] == '(') {
            arr[0] = '-';
            return "0" + arr;
        } else {
            return arr;
        }
    }
};