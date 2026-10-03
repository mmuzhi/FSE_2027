#include <string>
#include <vector>
#include <unordered_map>
#include <functional>
#include <cmath>
#include <cctype>
#include <optional>
#include <stdexcept>

class Calculator {
private:
    std::unordered_map<char, std::function<double(double, double)>> operators;

public:
    Calculator() {
        operators['+'] = [](double x, double y) { return x + y; };
        operators['-'] = [](double x, double y) { return x - y; };
        operators['*'] = [](double x, double y) { return x * y; };
        operators['/'] = [](double x, double y) {
            if (y == 0.0) throw std::runtime_error("division by zero");
            return x / y;
        };
        operators['^'] = [](double x, double y) { return std::pow(x, y); };
    }

    std::optional<double> calculate(const std::string& expression) {
        std::vector<double> operand_stack;
        std::vector<char> operator_stack;
        std::string num_buffer;

        for (char c : expression) {
            if (std::isdigit(static_cast<unsigned char>(c)) || c == '.') {
                num_buffer += c;
            } else {
                if (!num_buffer.empty()) {
                    operand_stack.push_back(std::stod(num_buffer));
                    num_buffer.clear();
                }

                if (c == '+' || c == '-' || c == '*' || c == '/' || c == '^') {
                    while (!operator_stack.empty() && operator_stack.back() != '(' &&
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
                    if (!operator_stack.empty()) {
                        operator_stack.pop_back(); // Remove the '('
                    }
                }
            }
        }

        if (!num_buffer.empty()) {
            operand_stack.push_back(std::stod(num_buffer));
        }

        while (!operator_stack.empty()) {
            apply_operator(operand_stack, operator_stack);
        }

        if (!operand_stack.empty()) {
            return operand_stack.back();
        }
        return std::nullopt;
    }

    int precedence(char op) const {
        if (op == '+' || op == '-') return 1;
        if (op == '*' || op == '/') return 2;
        if (op == '^') return 3;
        return 0;
    }

    void apply_operator(std::vector<double>& operand_stack, std::vector<char>& operator_stack) {
        char op = operator_stack.back();
        operator_stack.pop_back();

        double operand2 = operand_stack.back();
        operand_stack.pop_back();

        double operand1 = operand_stack.back();
        operand_stack.pop_back();

        double result = operators[op](operand1, operand2);
        operand_stack.push_back(result);
    }
};