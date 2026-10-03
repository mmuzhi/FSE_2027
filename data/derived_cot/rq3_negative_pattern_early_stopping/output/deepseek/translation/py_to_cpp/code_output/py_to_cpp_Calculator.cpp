#include <optional>
#include <string>
#include <vector>
#include <functional>
#include <unordered_map>
#include <cctype>
#include <cmath>

class Calculator {
public:
    Calculator() {
        operators = {
            {'+', std::plus<double>()},
            {'-', std::minus<double>()},
            {'*', std::multiplies<double>()},
            {'/', std::divides<double>()},
            {'^', [](double x, double y) { return std::pow(x, y); }}
        };
    }

    std::optional<double> calculate(const std::string& expression) {
        std::vector<double> operand_stack;
        std::vector<char> operator_stack;
        std::string num_buffer;

        for (char ch : expression) {
            if (std::isdigit(ch) || ch == '.') {
                num_buffer += ch;
            } else {
                if (!num_buffer.empty()) {
                    operand_stack.push_back(std::stod(num_buffer));
                    num_buffer.clear();
                }

                if (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '^') {
                    while (!operator_stack.empty() &&
                           operator_stack.back() != '(' &&
                           precedence(operator_stack.back()) >= precedence(ch)) {
                        apply_operator(operand_stack, operator_stack);
                    }
                    operator_stack.push_back(ch);
                } else if (ch == '(') {
                    operator_stack.push_back(ch);
                } else if (ch == ')') {
                    while (!operator_stack.empty() && operator_stack.back() != '(') {
                        apply_operator(operand_stack, operator_stack);
                    }
                    if (!operator_stack.empty() && operator_stack.back() == '(') {
                        operator_stack.pop_back();
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

        if (operand_stack.empty()) {
            return std::nullopt;
        }
        return operand_stack.back();
    }

    int precedence(char op) const {
        static const std::unordered_map<char, int> prec = {
            {'+', 1}, {'-', 1},
            {'*', 2}, {'/', 2},
            {'^', 3}
        };
        auto it = prec.find(op);
        return (it != prec.end()) ? it->second : 0;
    }

private:
    std::unordered_map<char, std::function<double(double, double)>> operators;

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