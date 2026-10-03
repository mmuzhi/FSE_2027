#include <deque>
#include <stack>
#include <string>
#include <cctype>
#include <cmath>
#include <algorithm>
#include <sstream>
#include <vector>
#include <regex>
#include <set>
#include <stdexcept>

class ExpressionCalculator {
private:
    std::deque<std::string> postfix_stack;
    static const std::vector<int> operat_priority;
    static const std::set<char> operators;

    static int get_precedence_index(const std::string& op) {
        if (op == "%") {
            return 7; // Map '%' to '/'
        }
        char c = op[0];
        int index = c - 40;
        return index;
    }

    bool compare(const std::string& cur, const std::string& peek) {
        if (cur == "%") {
            cur = "/";
        }
        if (peek == "%") {
            peek = "/";
        }
        int cur_index = get_precedence_index(cur);
        int peek_index = get_precedence_index(peek);

        return operat_priority[cur_index] >= operat_priority[peek_index];
    }

    static bool is_operator(const std::string& c) {
        return operators.find(c[0]) != operators.end();
    }

    static double _calculate(const std::string& first_value, const std::string& second_value, const std::string& current_op) {
        if (current_op == "+") {
            return std::stod(first_value) + std::stod(second_value);
        } else if (current_op == "-") {
            return std::stod(first_value) - std::stod(second_value);
        } else if (current_op == "*") {
            return std::stod(first_value) * std::stod(second_value);
        } else if (current_op == "/") {
            return std::stod(first_value) / std::stod(second_value);
        } else if (current_op == "%") {
            return fmod(std::stod(first_value), std::stod(second_value));
        } else {
            throw std::runtime_error("Unexpected operator: " + current_op);
        }
    }

    std::string transform(const std::string& expression) {
        std::regex space_regex("\\s+");
        std::regex equal_regex("=$");
        std::string expr = std::regex_replace(expression, space_regex, "");
        expr = std::regex_replace(expr, equal_regex, "");

        std::vector<char> arr(expr.begin(), expr.end());

        for (size_t i = 0; i < arr.size(); i++) {
            if (arr[i] == '-') {
                if (i == 0) {
                    arr[i] = '~';
                } else {
                    char prev_c = arr[i-1];
                    if (prev_c == '+' || prev_c == '-' || prev_c == '*' || prev_c == '/' || prev_c == '(' || prev_c == 'E' || prev_c == 'e') {
                        arr[i] = '~';
                    }
                }
            }
        }

        if (arr[0] == '~' && (arr.size() > 1 && arr[1] == '(')) {
            arr[0] = '-';
            std::string result(arr.begin(), arr.end());
            return "0" + result;
        } else {
            return std::string(arr.begin(), arr.end());
        }
    }

    void prepare(std::string expression) {
        std::vector<char> arr(expression.begin(), expression.end());
        int current_index = 0;
        int count = 0;
        std::stack<char> op_stack;
        op_stack.push(',');

        for (size_t i = 0; i < arr.size(); i++) {
            if (is_operator(std::string(1, arr[i]))) {
                if (count > 0) {
                    std::string num;
                    for (int j = 0; j < count; j++) {
                        num += arr[current_index + j];
                    }
                    postfix_stack.push_back(num);
                }
                char peek_op = op_stack.top();
                if (arr[i] == ')') {
                    while (peek_op != '(') {
                        postfix_stack.push_back(peek_op);
                        op_stack.pop();
                        if (op_stack.empty()) break;
                        peek_op = op_stack.top();
                    }
                    if (!op_stack.empty()) op_stack.pop();
                } else {
                    while (arr[i] != '(' && peek_op != ',' && compare(std::string(1, arr[i]), std::string(1, peek_op))) {
                        postfix_stack.push_back(peek_op);
                        op_stack.pop();
                        if (op_stack.empty()) break;
                        peek_op = op_stack.top();
                    }
                    op_stack.push(arr[i]);
                }
                count = 0;
                current_index = i + 1;
            } else {
                count++;
            }
        }

        if (count > 1 || (count == 1 && !is_operator(std::string(1, arr[current_index])))) {
            std::string num;
            for (int j = 0; j < count; j++) {
                num += arr[current_index + j];
            }
            postfix_stack.push_back(num);
        }

        while (!op_stack.empty() && op_stack.top() != ',') {
            postfix_stack.push_back(op_stack.top());
            op_stack.pop();
        }
    }

public:
    ExpressionCalculator() {}

    double calculate(std::string expression) {
        prepare(transform(expression));

        std::deque<std::string> result_stack;
        std::deque<std::string> temp;
        for (auto it = postfix_stack.rbegin(); it != postfix_stack.rend(); ++it) {
            temp.push_back(*it);
        }
        postfix_stack = temp;

        while (!postfix_stack.empty()) {
            std::string current_op = postfix_stack.front();
            postfix_stack.pop_front();

            if (!is_operator(current_op)) {
                if (current_op[0] == '~') {
                    current_op[0] = '-';
                }
                result_stack.push_back(current_op);
            } else {
                if (result_stack.size() < 2) {
                    throw std::runtime_error("Not enough operands");
                }
                std::string second_value = result_stack.back();
                result_stack.pop_back();
                std::string first_value = result_stack.back();
                result_stack.pop_back();

                if (first_value[0] == '~') {
                    first_value[0] = '-';
                }
                if (second_value[0] == '~') {
                    second_value[0] = '-';
                }

                double temp_result = _calculate(first_value, second_value, current_op);
                result_stack.push_back(std::to_string(temp_result));
            }
        }

        if (result_stack.empty()) {
            throw std::runtime_error("Empty result stack");
        }

        std::string result_str;
        for (size_t i = 0; i < result_stack.size(); i++) {
            if (i > 0) {
                result_str += "*";
            }
            result_str += result_stack[i];
        }

        return std::stod(result_str);
    }
};

const std::vector<int> ExpressionCalculator::operat_priority = {0, 3, 2, 1, -1, 1, 0, 2};
const std::set<char> ExpressionCalculator::operators = {'+', '-', '*', '/', '(', ')', '%'};