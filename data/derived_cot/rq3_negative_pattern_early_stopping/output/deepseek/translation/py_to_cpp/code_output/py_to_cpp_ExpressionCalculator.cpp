// Translation of the provided Python code to C++.
// Behavior (including edge cases and the final eval trick) is preserved as closely as possible.
// For the Decimal arithmetic, we use double in C++ (the Python version uses Decimal then converts to float).
// The transform() method uses std::regex to mimic re.sub.
// The prepare() method implements the shunting-yard algorithm with a stack.
// The calculate() method uses a deque for postfix evaluation and returns the result as double.
// Note: The final line in Python does eval("*".join(result_stack)) which,
//       when result_stack has one element, is equivalent to std::stod.

#include <iostream>
#include <string>
#include <vector>
#include <deque>
#include <stack>
#include <regex>
#include <cctype>
#include <sstream>
#include <stdexcept>

class ExpressionCalculator {
private:
    std::deque<std::string> postfix_stack;
    std::vector<int> operat_priority; // size 8

public:
    ExpressionCalculator() {
        // Initialize operat_priority: [0, 3, 2, 1, -1, 1, 0, 2]
        operat_priority = {0, 3, 2, 1, -1, 1, 0, 2};
    }

    double calculate(const std::string& expression) {
        prepare(transform(expression));

        std::deque<std::string> result_stack;
        // We need to reverse postfix_stack for processing (like Python's reverse)
        std::deque<std::string> reversed_stack(postfix_stack.rbegin(), postfix_stack.rend());
        postfix_stack.clear();

        while (!reversed_stack.empty()) {
            std::string current_op = reversed_stack.front();
            reversed_stack.pop_front();

            if (!is_operator(current_op)) {
                // replace '~' with '-'
                for (auto& ch : current_op) {
                    if (ch == '~') ch = '-';
                }
                result_stack.push_back(current_op);
            } else {
                if (result_stack.size() < 2) {
                    throw std::runtime_error("Insufficient operands");
                }
                std::string second_value = result_stack.back();
                result_stack.pop_back();
                std::string first_value = result_stack.back();
                result_stack.pop_back();

                // replace '~' with '-'
                for (auto& ch : first_value) if (ch == '~') ch = '-';
                for (auto& ch : second_value) if (ch == '~') ch = '-';

                double temp_result = _calculate(first_value, second_value, current_op);
                std::ostringstream oss;
                oss << temp_result;
                result_stack.push_back(oss.str());
            }
        }

        // In the Python code: float(eval("*".join(result_stack)))
        // If result_stack has exactly one element, this simply converts that string to float.
        if (result_stack.empty()) {
            return 0.0;
        }
        std::string joined = result_stack.front();
        // Multiply all? Actually eval("*".join(...)) would multiply numbers if multiple,
        // but normally result_stack has one element. We mimic exactly:
        double res = 1.0;
        for (size_t i = 0; i < result_stack.size(); ++i) {
            res *= std::stod(result_stack[i]);
        }
        return res;
    }

    void prepare(const std::string& expression) {
        // clear postfix_stack
        postfix_stack.clear();
        std::stack<std::string> op_stack;
        op_stack.push(","); // sentinel

        std::string expr = expression;
        size_t current_index = 0;
        size_t count = 0;

        for (size_t i = 0; i < expr.size(); ++i) {
            std::string current_op(1, expr[i]);
            if (is_operator(current_op)) {
                if (count > 0) {
                    postfix_stack.push_back(expr.substr(current_index, count));
                }
                std::string peek_op = op_stack.top();
                if (current_op == ")") {
                    while (op_stack.top() != "(") {
                        postfix_stack.push_back(op_stack.top());
                        op_stack.pop();
                    }
                    op_stack.pop(); // remove '('
                } else {
                    while (current_op != "(" && peek_op != "," && compare(current_op, peek_op)) {
                        postfix_stack.push_back(op_stack.top());
                        op_stack.pop();
                        peek_op = op_stack.top();
                    }
                    op_stack.push(current_op);
                }
                count = 0;
                current_index = i + 1;
            } else {
                count++;
            }
        }

        // After loop, if there's a pending token
        if (count > 1 || (count == 1 && !is_operator(std::string(1, expr[current_index])))) {
            postfix_stack.push_back(expr.substr(current_index, count));
        }

        // Pop remaining operators except sentinel
        while (op_stack.top() != ",") {
            postfix_stack.push_back(op_stack.top());
            op_stack.pop();
        }
    }

    static bool is_operator(const std::string& c) {
        if (c.size() != 1) return false;
        char ch = c[0];
        return ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '(' || ch == ')' || ch == '%';
    }

    bool compare(const std::string& cur, const std::string& peek) const {
        // The Python code treats '%' as '/' for precedence comparison
        char cur_c = cur[0];
        char peek_c = peek[0];
        if (cur_c == '%') cur_c = '/';
        if (peek_c == '%') peek_c = '/';
        // Index: ord(char) - 40. '(', ')', '*', '+', ',', '-', '.', '/' have ASCII 40-47, etc.
        // But our operat_priority size 8. The code uses ord(peek)-40 and ord(cur)-40.
        // However the Python code uses ord(peek)-40 and ord(cur)-40.
        // We'll compute index accordingly.
        int peek_idx = static_cast<int>(peek_c) - 40;
        int cur_idx = static_cast<int>(cur_c) - 40;
        // Ensure indices are within bounds (0..7)
        if (peek_idx < 0 || peek_idx >= 8 || cur_idx < 0 || cur_idx >= 8) {
            throw std::out_of_range("Operator index out of range");
        }
        return operat_priority[peek_idx] >= operat_priority[cur_idx];
    }

    static double _calculate(const std::string& first_value, const std::string& second_value, const std::string& current_op) {
        double fv = std::stod(first_value);
        double sv = std::stod(second_value);
        char op = current_op[0];
        switch (op) {
            case '+': return fv