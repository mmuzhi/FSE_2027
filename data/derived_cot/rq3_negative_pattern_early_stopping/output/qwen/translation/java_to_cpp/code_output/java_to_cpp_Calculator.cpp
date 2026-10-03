#include <iostream>
#include <stack>
#include <unordered_map>
#include <string>
#include <cmath>
#include <optional>

class Calculator {
private:
    std::unordered_map<char, std::function<double(double, double)>> operators;

    int precedence(char operator_char) {
        switch (operator_char) {
            case '+':
            case '-':
                return 1;
            case '*':
            case '/':
                return 2;
            case '^':
                return 3;
            default:
                return 0;
        }
    }

    void applyOperator(std::stack<double>& operandStack, std::stack<char>& operatorStack) {
        char op = operatorStack.top();
        operatorStack.pop();
        double operand2 = operandStack.top();
        operandStack.pop();
        double operand1 = operandStack.top();
        operandStack.pop();
        operandStack.push(operators[op](operand1, operand2));
    }

public:
    Calculator() {
        operators['+'] = [](double x, double y) { return x + y; };
        operators['-'] = [](double x, double y) { return x - y; };
        operators['*'] = [](double x, double y) { return x * y; };
        operators['/'] = [](double x, double y) { return x / y; };
        operators['^'] = [](double x, double y) { return std::pow(x, y); };
    }

    std::optional<double> calculate(const std::string& expression) {
        std::stack<double> operandStack;
        std::stack<char> operatorStack;
        std::string numBuffer;

        for (char ch : expression) {
            if (isdigit(ch) || ch == '.') {
                numBuffer += ch;
            } else {
                if (!numBuffer.empty()) {
                    operandStack.push(std::stod(numBuffer));
                    numBuffer.clear();
                }

                if (operators.find(ch) != operators.end()) {
                    while (!operatorStack.empty() && operatorStack.top() != '(' &&
                           precedence(operatorStack.top()) >= precedence(ch)) {
                        applyOperator(operandStack, operatorStack);
                    }
                    operatorStack.push(ch);
                } else if (ch == '(') {
                    operatorStack.push(ch);
                } else if (ch == ')') {
                    while (!operatorStack.empty() && operatorStack.top() != '(') {
                        applyOperator(operandStack, operatorStack);
                    }
                    operatorStack.pop();
                }
            }
        }

        if (!numBuffer.empty()) {
            operandStack.push(std::stod(numBuffer));
        }

        while (!operatorStack.empty()) {
            applyOperator(operandStack, operatorStack);
        }

        if (operandStack.empty()) {
            return std::nullopt;
        }
        return operandStack.top();
    }
};

int main() {
    Calculator calculator;
    std::cout << calculator.calculate("1+2-3") << std::endl;
    return 0;
}