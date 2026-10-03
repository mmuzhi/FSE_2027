#include <iostream>
#include <stack>
#include <map>
#include <cctype>
#include <stdexcept>
#include <string>

class Calculator {
private:
    // Map of operators to their lambda functions
    std::map<char, std::function<double(double, double)>> operators;

    // Helper function to get precedence of an operator
    int precedence(char operator_char) {
        static const std::map<char, int> prec_map = {
            {'+', 1},
            {'-', 1},
            {'*', 2},
            {'/', 2},
            {'^', 3}
        };
        auto it = prec_map.find(operator_char);
        if (it != prec_map.end()) {
            return it->second;
        }
        return 0;
    }

    // Helper function to apply an operator to two operands
    void apply_operator(std::stack<double>& operand_stack, std::stack<char>& operator_stack) {
        if (operator_stack.empty()) {
            return;
        }

        char op = operator_stack.top();
        operator_stack.pop();

        if (operand_stack.size() < 2) {
            throw std::runtime_error("Not enough operands for operator");
        }

        double operand2 = operand_stack.top();
        operand_stack.pop();
        double operand1 = operand_stack.top();
        operand_stack.pop();

        if (op == '^') {
            // Exponentiation: note the order (operand1 ** operand2)
            operand_stack.push(std::pow(operand1, operand2));
        } else {
            switch (op) {
                case '+': operand_stack.push(operand1 + operand2); break;
                case '-': operand_stack.push(operand1 - operand2); break;
                case '*': operand_stack.push(operand1 * operand2); break;
                case '/': 
                    if (operand2 == 0) {
                        throw std::runtime_error("Division by zero");
                    }
                    operand_stack.push(operand1 / operand2);
                    break;
                default:
                    throw std::runtime_error("Unknown operator");
            }
        }
    }

public:
    Calculator() {
        operators['+'] = [](double x, double y) { return x + y; };
        operators['-'] = [](double x, double y) { return x - y; };
        operators['*'] = [](double x, double y) { return x * y; };
        operators['/'] = [](double x, double y) { return x / y; };
        operators['^'] = [](double x, double y) { return std::pow(x, y); };
    }

    double calculate(const std::string& expression) {
        std::stack<double> operand_stack;
        std::stack<char> operator_stack;
        std::string num_buffer = "";

        for (char c : expression) {
            if (std::isdigit(c) || c == '.') {
                num_buffer += c;
            } else {
                if (!num_buffer.empty()) {
                    operand_stack.push(std::stod(num_buffer));
                    num_buffer = "";
                }

                if (c == '(') {
                    operator_stack.push(c);
                } else if (c == ')') {
                    // Apply all operators until '(' is found
                    while (!operator_stack.empty() && operator_stack.top() != '(') {
                        apply_operator(operand_stack, operator_stack);
                    }
                    if (!operator_stack.empty() && operator_stack.top() == '(') {
                        operator_stack.pop(); // Remove '('
                    }
                } else if (c == '+' || c == '-' || c == '*' || c == '/' || c == '^') {
                    // Apply operators at the top of the stack with higher or equal precedence (except for left associativity of '^')
                    while (!operator_stack.empty() && operator_stack.top() != '(') {
                        char top_op = operator_stack.top();
                        if (precedence(top_op) >= precedence(c)) {
                            apply_operator(operand_stack, operator_stack);
                        } else {
                            break;
                        }
                    }
                    operator_stack.push(c);
                }
            }
        }

        if (!num_buffer.empty()) {
            operand_stack.push(std::stod(num_buffer));
        }

        while (!operator_stack.empty()) {
            apply_operator(operand_stack, operator_stack);
        }

        if (operand_stack.empty()) {
            throw std::runtime_error("Invalid expression");
        }

        return operand_stack.top();
    }
};

int main() {
    Calculator calc;
    // Example usage
    try {
        std::cout << calc.calculate("1+2-3") << std::endl; // Should output 0.0
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    return 0;
}