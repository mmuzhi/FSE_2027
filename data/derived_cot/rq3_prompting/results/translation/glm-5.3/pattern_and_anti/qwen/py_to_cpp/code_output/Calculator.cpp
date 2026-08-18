#include <cmath>
#include <functional>
#include <optional>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

class Calculator {
public:
    Calculator() {
        operators_ = {
            {'+', [](double x, double y) { return x + y; }},
            {'-', [](double x, double y) { return x - y; }},
            {'*', [](double x, double y) { return x * y; }},
            {'/', [](double x, double y) {
                 if (y == 0.0) throw std::runtime_error("float division by zero");
                 return x / y;
             }},
            {'^', [](double x, double y) { return std::pow(x, y); }}
        };
    }

    // Returns the value of the expression, or nullopt (None) if none.
    std::optional<double> calculate(const std::string& expression) {
        std::vector<double> operand_stack;
        std::vector<char> operator_stack;
        std::string num_buffer;

        for (char c : expression) {
            if ((c >= '0' && c <= '9') || c == '.') {
                num_buffer += c;
            } else {
                if (!num_buffer.empty()) {
                    operand_stack.push_back(to_float(num_buffer));
                    num_buffer.clear();
                }

                if (c == '+' || c == '-' || c == '*' || c == '/' || c == '^') {
                    while (!operator_stack.empty() &&
                           operator_stack.back() != '(' &&
                           precedence(operator_stack.back()) >= precedence(c)) {
                        apply_operator(operand_stack, operator_stack);
                    }
                    operator_stack.push_back(c);
                } else if (c == '(') {
                    operator_stack.push_back(c);
                } else if (c == ')') {
                    while (!operator_stack.empty() && operator_stack.back() != '(') {
                        apply_operator(operand_stack, operator_stack);
                    }
                    // Python: operator_stack.pop() raises IndexError on empty
                    if (operator_stack.empty())
                        throw std::runtime_error("pop from empty list");
                    operator_stack.pop_back();
                }
            }
        }

        if (!num_buffer.empty()) {
            operand_stack.push_back(to_float(num_buffer));
        }

        while (!operator_stack.empty()) {
            apply_operator(operand_stack, operator_stack);
        }

        if (operand_stack.empty()) return std::nullopt;
        return operand_stack.back();
    }

    int precedence(char op) const {
        switch (op) {
            case '+': case '-': return 1;
            case '*': case '/': return 2;
            case '^': return 3;
            default: return 0;
        }
    }

    // Python mutates the passed lists and returns them; here we mutate in place.
    void apply_operator(std::vector<double>& operand_stack,
                        std::vector<char>& operator_stack) {
        if (operator_stack.empty())
            throw std::runtime_error("pop from empty list");
        char op = operator_stack.back();
        operator_stack.pop_back();

        double operand2 = pop_operand(operand_stack);
        double operand1 = pop_operand(operand_stack);
        double result = operators_.at(op)(operand1, operand2);  // .at() mirrors KeyError for '('
        operand_stack.push_back(result);
    }

private:
    static double pop_operand(std::vector<double>& stack) {
        if (stack.empty())
            throw std::runtime_error("pop from empty list");
        double v = stack.back();
        stack.pop_back();
        return v;
    }

    // Mirrors Python float(str): raises on empty/invalid/incomplete buffers.
    static double to_float(const std::string& buffer) {
        std::size_t pos = 0;
        double value;
        try {
            value = std::stod(buffer, &pos);
        } catch (const std::exception&) {
            throw std::runtime_error("could not convert string to float: '" + buffer + "'");
        }
        if (pos != buffer.size())
            throw std::runtime_error("could not convert string to float: '" + buffer + "'");
        return value;
    }

    std::unordered_map<char, std::function<double(double, double)>> operators_;
};